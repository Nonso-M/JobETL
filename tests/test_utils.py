import pytest
import pandas as pd
from dotenv import load_dotenv
import os
from utils.helper import parse_dict, filter_city
from utils.async_op import AsyncOperations

load_dotenv()
user_agent = os.environ.get("User-Agent")
api_key = os.environ.get("Authorization-Key")

headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": user_agent,
    "Authorization-Key": api_key,
}

BASE_URL = "https://data.usajobs.gov/api/search?"
entity = "Keyword=data engineering&ResultsPerPage=25&LocationName=Chicago"


def test_parse_dict(make_parse_dict):
    """Test the parse dicts function in the helper module"""
    key_list = [
        "PositionTitle",
        "PositionURI",
        "PositionLocation",
        "Salary_range",
        "RateIntervalCode",
        "AgencyContactEmail",
        "AgencyContactPhone",
        "JobSummary",
        "Grade",
        "ApplyOnlineUrl",
        "Organization_name",
        "Organization_dept",
        "JobCategory",
        "Payplans",
        "EmploymentType",
        "PositionOfferingType",
        "                  PositionStartDate",
        "ApplicationCloseDate",
    ]
    data = parse_dict(make_parse_dict)
    assert type(data) == dict
    all(item in list(data.key()) for item in key_list)


def test_filter_city_no_Chicago(make_filter_dict_chicago):
    """Test the filter city function in the helper module"""
    bool_value = filter_city(make_filter_dict_chicago)
    assert type(bool_value) == bool
    assert bool_value


def test_filter_city_Chicago(make_filter_dict_chicago):
    """Test the filter city function in the helper module"""
    bool_value = filter_city(make_filter_dict_chicago)
    assert type(bool_value) == bool
    assert bool_value


def test_filter_city_no_Chicago(make_filter_dict_no_chicago):
    """Test the filter city function in the helper module"""
    bool_value = filter_city(make_filter_dict_no_chicago)
    assert type(bool_value) == bool
    assert ~bool_value


@pytest.mark.vcr()
def test_async_func():
    """Tests the data extraction from msdat"""
    key_list = ["MatchedObjectId", "MatchedObjectDescriptor", "RelevanceRank"]
    asyncc = AsyncOperations(base_url=BASE_URL, headers=headers)
    data = asyncc.gather_tasks(entity, 3)
    assert type(data) == list
    assert type(data[1]) == dict
    all(key in data[0] for key in key_list)
    assert len(data) == 75
