from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import ResultProxy
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.sql.expression import Select, Update


# Dev DB only for testing
DB_ADDRESS = "postgresql+psycopg2://marek-szyd@127.0.0.1/32/wikipedia_recommender"

CONNECT_TIMEOUT = 10  # seconds


class DBConnector:
    def __init__(self) -> None:
        self.engine, self.db_connection = self.get_connection()

    def get_connection(self) -> Tuple[Engine, Connection]:
        """Returns engine and connection to the DB"""
        engine = create_engine(
            DB_ADDRESS,
            pool_recycle=3600,
            connect_args={"connect_timeout": CONNECT_TIMEOUT},
        )

        db_connection: Connection = engine.connect().execution_options(
            stream_results=True
        )

        return engine, db_connection

    def select(self, query: Select, params: dict = {}) -> ResultProxy:
        """Performs select query using db_connector.db_connection
        Parameters:
            query (Select): select query to be performed
            params (dict): dictionary of optional parameters
        Returns:
            ResultProxy: Contains fetched entries
        """
        return self.db_connection.execute(query, **params)

    def update(self, query: Update, params: dict = {}) -> None:
        """Performs update query using db_connector.engine
        Parameters:
            query (Update): update query to be performed
            params (dict): dictionary of optional parameters
        """
        self.engine.execute(query, **params)
