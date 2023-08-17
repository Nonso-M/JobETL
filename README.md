
# JobETL: Loading Jobs from API to Database
## Overview
This is an ETL (Extract, Transform, Load) pipeline that automates the process of extracting job data from a Job API, transforming it as needed, and loading it into a database. By containerizing the ETL process with Docker, this pipeline ensures consistent and isolated execution across different environments.

## Prerequisites
Before running the Dockerized ETL pipeline, ensure you have the following:

- Docker installed on your system.
- Docker Compose.
- Access credentials for the API.
- DataBase Credentials if you want to push it to your own PostGres DB.

## Setup
Clone this repository to your local machine.
```
git clone https://github.com/Nonso-M/JobETL.git
```
Navigate to the root directory of the project.

## Configuration
Create a .env file in the root directory and populate it with the following credential

```
Authorization-Key=<API_KEY>
Database-Name=etldb
DB-UserName=etladmin
Password=mypassword
DatabaseHost=postgres
Port=5432

```
Database Configuration: The docker-compose.yml file is adjusted to fit the  Database credentials (e.g., host, port, username, password) filled in your environment variables file. If you wan to use diffferent database credentials i.e outside the container, you can change the enviroment to the new credentials you wan to use.

- Authorization-Key: This is the API key gotten from [Usa Jobs](https://developer.usajobs.gov/APIRequest/)
- Database-Name: Database Name  Name.
- UserName - Username of the database you would Like to push it to
- Password -  Database Password

- __N/B__: If you don't intend to send the Data to a personal Posgres Server when running locally change the `DB-UserName`, `DatabseHost`,`Password`, `DatabaseHost`, `Port` to your own details

# Running the pipeline Locally on your Machine
To run the pipeline locally on your machine carry out the following steps
- Create a virtual Environment
- Install the requirements.txt file using
```bash
pip install -r requirements.txt
``` 
- Populate the .env as specified above **N/B** Add the API key in .env file
- Run `main_sql.py` to push data to a SQLite database and `main2.py` to push data to a postgres Databse
**N/B** Before running `main2.py`, add your Postgres database credentials to push it

# Running the Dockerized ETL Pipeline
- Open a terminal and navigate to the root directory of the project.
- Build and run the Docker container for the ETL pipeline by running:

```
docker-compose up -d .
```
`-d`is running it in detached mode
If you would like to push the data to your own Postgres Instance, you have to change the enviromental variables before building to match yours
## Logging Into the Postgres Database
To access the postgres database go into your browser and search `localhost:8088` to access PGadmin
- The login for pgadmin is as follows
EMAIL: admin@example.com
PASSWORD: adminpassword

To access the table data you have to register the database on PGadmin. To do this;
- Right click and register new database
- Retieve the Host name by running
```
docker ps
```
This helps yo retrieve the running containers and their corresponding IDs. Copy the ID for postgres container which would be used to get the Host IP Address
To get the host ip run
```
docker inspect <postgres_container_ID>
```
The Host Ip is found under the key `IPAddress`
----
The remaining credentials are as follows
Host name/address:  <IP gotten above>
Port: 5432
Maintenance Database: etldb
Username: etladmin
Password: mypassword

**N/B** The data is backed up in the postgres-data folder
### The ETL pipeline performs the following steps within the Docker container:

- Extract: Connects to the AmericanJob API and retrieves job data using the provided parameters.
- Transform: Transforms the raw job data into the desired format, applying any necessary data filtering or preprocessing.
- Load: Loads the processed job data into either a sqlite db or a Postgres DB.

Data Structure
The structure of the data stored in the database after running the Dockerized ETL pipeline will be as follows:

### Table Name: jobs
Table Schema:
`PositionTitle` - Title of the Job
`PositionURI` - Link to the job posting on USAJobs
`PositionLocation` - A list of locations for the job
`Salary-Range` - A concatenation of the lower and upper bound of the salary available for the role
`RateIntervalCode`- Is it PA(Per Annum) or PM(Per Month)
`AgencyContactEmail`- Email of the agency hiring
`AgencyContactPhone`- Phone of the agency hiring
`Grade`- A concatenation of the maximum and minimum grade for the role
`ApplyOnlineURL`- A direct link to the application page
`Organization_name` - Name of Organizzation
`Organization_dept` - Department that is hiring
`JobCategory` -  Is it a full time, part time etc
`ApplicationClodeDate`- When the application closes

## Deployment and Scheduling
Amazon Elastic Container Service (Amazon ECS), is a shared state, optimistic concurrency system that provides flexible scheduling capabilities for your tasks and containers. Amazon ECS provides a service scheduler for long-running tasks and applications. It also provides the ability to run tasks manually for batch jobs or single run tasks.
EventBridge Scheduler to create a schedule.

### Pros of using ECS for Scheduling and Deployment includes 
- Fully Managed Service
- Flexibility in Task Scheduling
- Auto Scalability
- Security and Networking

### Cons of using ECS for Scheduling and Deployment includes 
- Cost Optimization Management
- Learning Curve
- Advanced Features and Customization

## Data Schedule
You can configure the Dockerized ETL pipeline to run periodically using a scheduling tool (e.g., cron jobs, Airflow). Decide on the appropriate schedule based on the frequency of updates to the API data and the needs of your analysis.

Troubleshooting
If you encounter any issues or errors while running the Dockerized ETL pipeline, please refer to the error messages in the terminal. If the problem persists, feel free to reach out to [Your Contact Information] for assistance.

Maintenance
As the API or data requirements may change over time, it's essential to periodically review and update this Dockerized ETL pipeline to ensure it continues to function properly. Regularly check for updates to the API configuration, dependencies, credentials, and data transformations to maintain the pipeline's reliability.

