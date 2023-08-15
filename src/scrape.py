import requests
import logging
import backoff
import pandas as pd
from utils.helper import parse_dict, filter_city
from utils.async_op import AsyncOperations


# Configuring the logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Defining constants
BASE_URL = "https://data.usajobs.gov/api/"


class JobSearch(object):
    base_url = BASE_URL
    location = "Chicago"
    search_str = "data engineering"

    def __init__(
        self, header: dict[str, str], result_no: int, asyncc: AsyncOperations
    ) -> None:
        self.headers = header
        self.result_no = result_no
        self.asyncc = asyncc

    @property
    def query_param(self):
        # query_parameter = f"Keyword={self.search_str}&LocationName={self.location}&ResultsPerPage={self.result_no}"
        query_parameter = f"Keyword={self.search_str}&ResultsPerPage={self.result_no}"
        return query_parameter

    def get_number_pages(self) -> int:
        """Get the number of pages to loop through for a query
        Args:
            query_parameter (str):A string containing all the query parameter for the request
        Returns:
            _type_: _description_
        """
        full_url = f"{self.base_url}search?{self.query_param}"
        try:
            response = requests.get(full_url, headers=self.headers)
            data = response.json()
            num_pages = int(data["SearchResult"]["UserArea"]["NumberOfPages"])
            return num_pages

        except Exception as e:
            logger.error(f"error:{e}", exc_info=True)
            logger.error(f"Response content: {response.content}")

    def parse_all_jobs(self, job_list: list):
        """Extracts all the information need for a job on a single page

        Args:
            job_list (_type_): List of all job search results
        """
        result = [parse_dict(job, self.location) for job in job_list]

        return result

    def search_job(self, session, page=1):
        """This method
        Args:
            search_term (str): A string containing all the query parameter for the request
        """
        full_url = f"{self.base_url}search?{self.query_param}&Page={page}"
        try:
            response = session.get(full_url, headers=self.headers)
            data = response.json()

            # Filters for jobs that has a location in chicago and parse the results
            filtered_list = [
                filter_data
                for filter_data in data["SearchResult"]["SearchResultItems"]
                if filter_city(filter_data, self.location)
            ]
            result = self.parse_all_jobs(filtered_list)
            return result

        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            logger.error(f"Response content: {response.content}")

    @backoff.on_exception(
        backoff.expo, (requests.exceptions.HTTPError, KeyError), max_tries=5
    )
    def get_all_jobs(self) -> list:
        """Loops through all pages ang gets all the jobs search result
        Returns:
            list: A list of all the jobs extracted
        """
        total_jobs = []
        with requests.Session() as session:
            num_pages = self.get_number_pages()
            for page in range(1, num_pages + 1):
                jobs = self.search_job(session=session, page=page)
                total_jobs += jobs
                logger.info(f"Jobs for Page {page} has successfully been parsed")

            return total_jobs

    def get_position_offering(self):
        """Gets all the Positional offering and their associating codes
        Args:
            endpoint (str): The endpoint added to the base url
        """
        full_url = f"{self.base_url}codelist/positionofferingtypes"
        try:
            response = requests.get(full_url, headers=self.headers)
            position_dict = response.json()

        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)

        final = {
            entry["Code"]: entry["Value"]
            for entry in position_dict["CodeList"][0]["ValidValue"]
        }
        return final

    def get_position_schedule(self) -> dict[str, str]:
        """Gets all the Positional scheduling and their associating codes
        Args:
            endpoint (str): The endpoint added to the base url
        """
        full_url = f"{self.base_url}codelist/positionscheduletypes"
        try:
            response = requests.get(full_url, headers=self.headers)
            position_dict = response.json()

        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)

        final = {
            entry["Code"]: entry["Value"]
            for entry in position_dict["CodeList"][0]["ValidValue"]
        }
        return final

    def get_all_jobs_async(self):
        num_pages = self.get_number_pages()
        data = self.asyncc.gather_tasks(self.query_param, num_pages)

        return data

    def extract_data_async(self, all_jobs):
        filtered_list = [
            filter_data
            for filter_data in all_jobs
            if filter_city(filter_data, self.location)
        ]
        result = self.parse_all_jobs(filtered_list)
        return result

    def format_all_jobs(self, jobs_dict: dict):
        """Receives the extracted dictionary of all jobs and formats it
        Args:
            jobs_dict (dict): _description_
        Returns:
            _type_: _description_
        """
        schedule_dict = self.get_position_schedule()
        positional_offering = self.get_position_offering()

        # Generate the dataframe and use the the dictionaries to map
        job_df = pd.DataFrame(jobs_dict)
        job_df["PositionOfferingType"] = job_df["PositionOfferingType"].map(
            positional_offering
        )
        job_df["EmploymentType"] = job_df["EmploymentType"].map(schedule_dict)

        return job_df
