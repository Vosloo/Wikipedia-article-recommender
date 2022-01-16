import pandas as pd
from models.document import Document
from models.wikipedia import Wikipedia
from sqlalchemy import bindparam, select

from db_model.DBConnector import DBConnector


class DBQuery:
    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector: DBConnector = db_connector

    def get_wikipedia_by_url(self, url: str) -> Wikipedia:
        query = select([Wikipedia]).where(Wikipedia.url == bindparam("url"))

        res = self.db_connector.select(query, {"url": url})
        return pd.DataFrame(res.fetchall(), columns=res.keys())

    def get_all_documents(self) -> pd.DataFrame:
        query = select([Wikipedia])

        res = self.db_connector.select(query)
        return pd.DataFrame(res.fetchall(), columns=res.keys())

    def insert_document(self, document: Document) -> None:
        ...

if __name__ == "__main__":
    db_connector = DBConnector()
    db_query = DBQuery(db_connector)
    wikipedia = db_query.get_all_documents()
    print(wikipedia)
