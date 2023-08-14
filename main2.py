from dotenv import load_dotenv
import os
import pandas as pd

from src.scrape import JobSearch
from utils.database import push_to_postgres


load_dotenv()

database_name = os.environ.get("Database-Name")
api_key = os.environ.get("Authorization-Key")
username = os.environ.get("UserName")
password = os.environ.get("Passworde")

db_params = {
    "database": database_name,
    "user": username,
    "password": password,
    "host": "localhost",
    "port": "5432",
}


headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": "noname@gmail.com",
    "Authorization-Key": api_key,
}


Job = JobSearch(headers, 25)


if __name__ == "__main__":
    data = Job.search_job()
    datframe = Job.format_all_jobs(data)

    push_to_postgres(datframe, db_params, "jobs")

    datframe.to_csv("Trial.csv", index=False)
