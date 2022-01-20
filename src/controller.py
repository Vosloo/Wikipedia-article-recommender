from typing import Union

from normalizer import Normalizer
from purifier import Purifier
from scraper import Scraper

import pandas as pd

class Controller:
    def __init__(self) -> None:
        self.documents: Union[pd.DataFrame, None] = None
        self.parsed: Union[pd.DataFrame, None] = None
        
        self.normalizer = Normalizer()
        self.purifier = Purifier()
        self.scraper = Scraper()

    def parse_data(self):
        """Loads pandas DataFrame object with raw html texts"""
        
        # 1. Load DataFrame with raw html texts
        # 2. Apply general purifying
        # 3. Apply normalization
        # 4. Apply purifying after normalization
        # 5. Save parsed data to parquet file
        ...

    def recommender(self):
        """Recommends articles based on given query"""
        ...

    def scrape(self):
        """Runs scraper and saves scraped responses to parquet file"""
        ...

    def _load_parsed(self):
        """Loads pandas DataFrame object with parsed texts"""
        ...

    def _load_responses(self):
        """Loads pandas DataFrame object with scraped responses"""
        ...


if __name__ == "__main__":
    print("Ciupaga")

