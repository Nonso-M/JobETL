from dotenv import load_dotenv
import os

from src.scrape import JobSearch, BASE_URL
from utils.database import push_to_postgres
from utils.async_op import AsyncOperations


load_dotenv()

database_name = os.environ.get("Database-Name")
api_key = os.environ.get("Authorization-Key")
username = os.environ.get("DB-UserName")
password = os.environ.get("Password")
host = os.environ.get("DatabaseHost")
port = os.environ.get("Port")


db_params = {
    "database": database_name,
    "user": username,
    "password": password,
    "host": host,
    "port": port,
}

headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": "noname@gmail.com",
    "Authorization-Key": api_key,
}

# Prepping the async class for ansynchronous injection
asyncc = AsyncOperations(f"{BASE_URL}search?", headers=headers)
Job = JobSearch(headers, 200, asyncc)


def main():
    # Extracting Data from the client API asynchronously
    data = Job.get_all_jobs_async()
    data_list = Job.extract_data_async(data)
    dataframe = Job.format_all_jobs(data_list)

    push_to_postgres(dataframe, db_params, "jobs")


if __name__ == "__main__":
    main()
