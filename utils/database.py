import pandas as pd
import logging
import sqlite3
from sqlalchemy import create_engine


# Configuring the logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def push_to_sqlite(data: pd.DataFrame, database_name: str, table_name: str):
    """Pushes data to either a sqlite database or postgres databse

    Args:
        data (pd.DataFrame): Data to be pushed to the database
        database_name (str): Name of the persistent Database
    """
    # Connect to the SQLite database and send data to it
    try:
        conn = sqlite3.connect(database_name)
        data.to_sql(table_name, conn, if_exists="replace", index=False)

        # Commit the transaction and close the connection
        conn.commit()

    except Exception as e:
        logging.error(f"error:{e}", exc_info=True)

    finally:
        # Close the cursor and connection in the 'finally' block
        if conn:
            conn.close()


def push_to_postgres(data: pd.DataFrame, db_params: dict[str, str], table_name: str):
    """

    Args:
        data (pd.DataFrame): Data to be pushed to a Postgres Database
        db_params (dict[str,str]): Database Parameters to connect to a database
        table_name (str): Table name for storing the data
    """

    try:
        # Create a SQLAlchemy engine
        engine = create_engine(
            f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}'
        )
        data.to_sql(table_name, engine, if_exists="replace", index=False)
        logging.info(
            f"DataFrame pushed to the '{table_name}' table in the PostgreSQL database."
        )

    except Exception as e:
        logging.error(f"error:{e}", exc_info=True)
