from dotenv import load_dotenv
import os

from src.scrape import JobSearch, BASE_URL
from utils.database import push_to_sqlite
from utils.async_op import AsyncOperations


load_dotenv()

user_agent = os.environ.get("User-Agent")
api_key = os.environ.get("Authorization-Key")

headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": user_agent,
    "Authorization-Key": api_key,
}


# Prepping the async class for ansynchronous injection
asyncc = AsyncOperations(f"{BASE_URL}search?", headers=headers)
Job = JobSearch(headers, 200, asyncc)


def main():
    data = Job.get_all_jobs()
    dataframe = Job.format_all_jobs(data)

    push_to_sqlite(dataframe, "Jobs.db", "jobs")


if __name__ == "__main__":
    main()
