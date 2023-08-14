"""
This module helps to parse the job instance result that comes from the job search query. 
"""
import logging
import pandas as pd

logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_dict(job_dict: dict):
    """Extracts useful information from a job search result instance
    Args:
        job_dict (dict): A job result gotten from the search query
    """
    # Initializes the dictionary for storing the job details
    job = dict()
    job["PositionTitle"] = job_dict["MatchedObjectDescriptor"]["PositionTitle"]
    job["PositionURI"] = job_dict["MatchedObjectDescriptor"]["PositionURI"]

    # gets a lsit of all the location that contains Chicago and parse them to single string
    location = set(
        [
            location["CityName"]
            for location in job_dict["MatchedObjectDescriptor"]["PositionLocation"]
            if "Chicago" in location["CityName"]
        ]
    )
    job["PositionLocation"] = ", ".join(list(location))
    logger.info("Position Name, URI and location has been successfully parsed")

    money_dict = job_dict["MatchedObjectDescriptor"]["PositionRemuneration"][0]
    job["Salary_range"] = " - ".join(
        [money_dict["MinimumRange"], money_dict["MaximumRange"]]
    )
    job["RateIntervalCode"] = job_dict["MatchedObjectDescriptor"][
        "PositionRemuneration"
    ][0]["Description"]
    logger.info("Salary and  range has successfully been parsed")

    # traverses the dictionary to get the all information contained in Details
    contact_info = job_dict["MatchedObjectDescriptor"]["UserArea"]["Details"]
    job["AgencyContactEmail"] = contact_info.get("AgencyContactEmail", " N/A")
    job["AgencyContactPhone"] = contact_info.get("AgencyContactPhone", " N/A")
    job["JobSummary"] = contact_info.get("JobSummary", " N/A")
    job["Grade"] = " - ".join(
        list(set([contact_info["LowGrade"], contact_info["HighGrade"]]))
    )
    job["ApplyOnlineUrl"] = contact_info["ApplyOnlineUrl"]
    logger.info("Salary range has successfully been parsed")

    job["Organization_name"] = job_dict["MatchedObjectDescriptor"]["OrganizationName"]
    job["Organization_dept"] = job_dict["MatchedObjectDescriptor"]["DepartmentName"]
    job["JobCategory"] = job_dict["MatchedObjectDescriptor"]["JobCategory"][0]["Name"]

    job["Payplans"] = job_dict["MatchedObjectDescriptor"]["JobGrade"][0]["Code"]
    job["EmploymentType"] = job_dict["MatchedObjectDescriptor"]["PositionSchedule"][0][
        "Code"
    ]
    job["PositionOfferingType"] = job_dict["MatchedObjectDescriptor"][
        "PositionOfferingType"
    ][0]["Code"]
    job["PositionStartDate"] = job_dict["MatchedObjectDescriptor"]["PositionStartDate"]
    job["ApplicationCloseDate"] = job_dict["MatchedObjectDescriptor"][
        "ApplicationCloseDate"
    ]

    return job


def format_all_jobs(jobs_dict, schedule: dict, pos_offering):
    job_df = pd.DataFrame(jobs_dict)

    job_df["PositionOfferingType"] = job_df["PositionOfferingType"].map(pos_offering)
    job_df["EmploymentType"] = job_df["EmploymentType"].map(schedule)
