
# JobETL: Loading Jobs from API to Database
## Overview
This is an ETL (Extract, Transform, Load) pipeline that automates the process of extracting job data from a Job API, transforming it as needed, and loading it into a database. By containerizing the ETL process with Docker, this pipeline ensures consistent and isolated execution across different environments.

## Prerequisites
Before running the Dockerized ETL pipeline, ensure you have the following:

- Docker installed on your system.
- Docker Compose (if you're using a multi-container setup).
- Access credentials for the API.
- Access credentials if you choose to push to a Postgres Database(SQLite doesn't need Credentials).

## Setup
Clone this repository to your local machine.
```
git clone https://github.com/Nonso-M/JobETL.git
```
Navigate to the root directory of the project.

## Configuration
Create a .env file in the root directory and populate it with the following credential

```
User-Agent= noname@gmail.com
Authorization-Key=<API_KEY>
Database-Name= <Database Name>
DB-UserName= <Database Username>
Password= <Database Password>
DatabaseHost= <Hostname of your Postgres Server> 
Port=<Port Number>
```
- Authorization-Key: This is the API key gotten from [Usa Jobs](https://developer.usajobs.gov/APIRequest/)
- Database-Name: Database Name  Name.
- UserName - Username of the database you would Like to push it to
- Password -  Database Password

- __N/B__: If you don't intend to send the Data to a SQL or Postgres Server you shuld use the first version of the enviroment file

Database Configuration: The docker-compose.yml file is adjusted to fit the  Database credentials (e.g., host, port, username, password) filled in your environment variables file. If you wan to use diffferent database credentials i.e outside the container, you can change the enviroment to the new credentials you wan to use.

# Running the Dockerized ETL Pipeline
- Open a terminal and navigate to the root directory of the project.
- Build the Docker image for the ETL pipeline by running:
```
docker build -t etl-pipeline .
Start the Dockerized ETL pipeline by running:
```

```
docker run -it etl-pipeline
```
----
### The ETL pipeline performs the following steps within the Docker container:

> Extract: Connects to the AmericanJob API and retrieves job data using the provided parameters.
Transform: Transforms the raw job data into the desired format, applying any necessary data filtering or preprocessing.
Load: Loads the processed job data into either a sqlite db or a Postgres DB.

Data Structure
The structure of the data stored in the database after running the Dockerized ETL pipeline will be as follows:

Table Name: [Name of the target table]
Fields:
[Field 1]
[Field 2]
...
Data Schedule
You can configure the Dockerized ETL pipeline to run periodically using a scheduling tool (e.g., cron jobs, Airflow). Decide on the appropriate schedule based on the frequency of updates to the API data and the needs of your analysis.

Troubleshooting
If you encounter any issues or errors while running the Dockerized ETL pipeline, please refer to the error messages in the terminal. If the problem persists, feel free to reach out to [Your Contact Information] for assistance.

Maintenance
As the API or data requirements may change over time, it's essential to periodically review and update this Dockerized ETL pipeline to ensure it continues to function properly. Regularly check for updates to the API configuration, dependencies, credentials, and data transformations to maintain the pipeline's reliability.



> **Note:** This is how you write a note.
>
> It can have multiple lines.