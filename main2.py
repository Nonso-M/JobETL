from dotenv import load_dotenv
import os

from src.scrape import JobSearch
from utils.database import push_to_postgres


load_dotenv()

database_name = os.environ.get("Database-Name")
api_key = os.environ.get("Authorization-Key")
username = os.environ.get("DB-UserName")
password = os.environ.get("Password")

print(username)

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


Job = JobSearch(headers, 200)


def main():
    data = Job.get_all_jobs()
    datframe = Job.format_all_jobs(data)

    push_to_postgres(datframe, db_params, "jobs")


if __name__ == "__main__":
    main()
