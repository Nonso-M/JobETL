import requests
import logging
import backoff


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
    search_str = "data engineer"

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

    @staticmethod
    def parse_dict(job_dict: dict):
        """Extracts useful information from a job search result instance
        Args:
            job_dict (dict): A job result gotten from the search query
        """
        job = dict()
        job["PositionTitle"] = job_dict["MatchedObjectDescriptor"]["PositionTitle"]
        job["PositionURI"] = job_dict["MatchedObjectDescriptor"]["PositionURI"]

        location = set(
            [
                location["CityName"]
                for location in job_dict["MatchedObjectDescriptor"]["PositionLocation"]
                if "Chicago" in location["CityName"]
            ]
        )
        job["PositionLocation"] = ", ".join(list(location))

        money_dict = job_dict["MatchedObjectDescriptor"]["PositionRemuneration"][0]
        job["Salary_range"] = " - ".join(
            [money_dict["MinimumRange"], money_dict["MaximumRange"]]
        )

    def search_job(self, page=1):
        """This method
        Args:
            search_term (str): A string containing all the query parameter for the request
        """
        full_url = f"{self.base_url}search?{self.query_param}&Page={page}"
        try:
            response = requests.get(full_url, headers=self.headers)
            data = response.json()
            return data["SearchResult"]["SearchResultItems"]

        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def get_all_jobs(self, query_parameter: str):
        num_pages = self.get_number_pages(query_parameter=query_parameter)
        for page in range(1, num_pages + 1):
            jobs = self.search_job(page=page)
