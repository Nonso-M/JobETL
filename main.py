from dotenv import load_dotenv
import os
import pandas as pd

from src.scrape import JobSearch
from utils.database import push_to_sqlite


load_dotenv()
host = os.environ.get("Host")
user_agent = os.environ.get("User-Agent")
api_key = os.environ.get("Authorization-Key")

headers = {"Host": host, "User-Agent": user_agent, "Authorization-Key": api_key}


Job = JobSearch(headers, 25)


if __name__ == "__main__":
    data = Job.search_job()
    datframe = Job.format_all_jobs(data)

    push_to_sqlite(datframe, "Jobs.db", "jobs")

    datframe.to_csv("Trial.csv", index=False)
