import requests
import logging
import backoff
import pandas as pd
import asyncio
import time
from utils.helper import parse_dict, filter_city
from utils.async_op import AsyncOperations


# Configuring the logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Defining constants
BASE_URL = "https://data.usajobs.gov/api/"


class FetchData:
    """A class that fetches data using the async operations"""

    def __init__(self, headers):
        """Initializes the fetchdataclass"""

        self.headers = headers
        self.base_url = BASE_URL
        self.async_op = AsyncOperations(self.base_url, self.headers)

    def loop_pages(self, start: int, stop: int, step: int) -> tuple:
        """Loops through pages

        Args:
            start (int): Gives where to start extracting the page
            stop (int): Gives where to stop extracting the page
            step (int): Gives the step to take

        Returns:
            tuple: A tuple containing two numbers
        """
        number = range(start, stop, step)
        tuple_num = zip(number[:-1], number[1:])

        return tuple_num

    def gather_tasks(
        self, entity: str, start: int, stop: int, step: int, num_pages
    ) -> list:
        """Gets all the tasks for a particular category and returns a list

        Args:
            entity (str): the remaining part of the link to the API
            start (int): page to start pulling
            stop (int): page to stop pulling
            step (int): steps to take between the two numbers

        Returns:
            all_tasks (list): A list that contains all the tasks.
        """

        responses = asyncio.get_event_loop()
        resultants = responses.run_until_complete(
            self.async_op.get_tasks(
                self.async_op.make_requests, range_num=num_pages, entity=entity
            )
        )

        return resultants


class JobSearch(object):
    base_url = BASE_URL
    location = "Chicago"
    search_str = "data engineering"

    def __init__(
        self,
        header: dict[str, str],
        result_no: int,
    ) -> None:
        self.headers = header
        self.result_no = result_no

    @property
    def query_param(self):
        query_parameter = f"Keyword={self.search_str}&LocationName={self.location}&ResultsPerPage={self.result_no}"
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

    def search_job(self, page=1):
        """This method
        Args:
            search_term (str): A string containing all the query parameter for the request
        """
        full_url = f"{self.base_url}search?{self.query_param}&Page={page}"
        print(full_url)
        try:
            response = requests.get(full_url, headers=self.headers)
            data = response.json()

            # Filters for jobs that has a location in chicago and parse the results
            filtered_list = [
                filter_data
                for filter_data in data["SearchResult"]["SearchResultItems"]
                if filter_city(filter_data, self.location)
            ]
            # result = self.parse_all_jobs(data["SearchResult"]["SearchResultItems"])
            result = self.parse_all_jobs(filtered_list)
            return result

        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            logger.error(f"Response content: {response.content}")

    @backoff.on_exception(
        backoff.expo, (requests.exceptions.HTTPError, KeyError), max_tries=5
    )
    def get_all_jobs(self):
        total_jobs = []
        num_pages = self.get_number_pages()
        for page in range(1, num_pages + 1):
            jobs = self.search_job(page=page)
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

    def format_all_jobs(self, jobs_dict):
        schedule_dict = self.get_position_schedule()
        positional_offering = self.get_position_offering()

        # Generate the dataframe and use the the dictionaries to map
        job_df = pd.DataFrame(jobs_dict)
        job_df["PositionOfferingType"] = job_df["PositionOfferingType"].map(
            positional_offering
        )
        job_df["EmploymentType"] = job_df["EmploymentType"].map(schedule_dict)

        return job_df
