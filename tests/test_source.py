import pytest
import pandas as pd
from dotenv import load_dotenv
import os
from src.scrape import JobSearch


load_dotenv()
user_agent = os.environ.get("User-Agent")
api_key = os.environ.get("Authorization-Key")

# Wrong header for testing the exceptions
headers2 = {
    "Host": "da.usajobs.go",
    "User-Agent": user_agent,
    "Authorization-Key": api_key,
}

headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": user_agent,
    "Authorization-Key": api_key,
}

results_per_page = 25

job = JobSearch(headers, results_per_page)
job2 = JobSearch(headers2, results_per_page)


def test_class_property():
    """Tests that the query parameter is passed correctly"""

    correct_string = f"Keyword=data engineering&ResultsPerPage={results_per_page}&LocationName=Chicago"

    assert job.query_param == correct_string


@pytest.mark.vcr()
def test_num_of_page_method():
    """Test that the num of pages result is returned succesfully
    Args:
        make_dict_num_pages (_type_):FIxture that gives a sample of the result gotten
    """
    num_pages = job.get_number_pages()
    assert type(num_pages) == int


def test_num_of_page_method_error():
    """Test that the num of pages result is returned succesfully
    Args:
        make_dict_num_pages (_type_):FIxture that gives a sample of the result gotten
    """
    with pytest.raises(Exception) as excinfo:
        num_pages = job.get_number_pages()
