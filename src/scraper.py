import json
import re
from random import choice
from time import sleep
from typing import Union

import pandas as pd
import requests
from tqdm import tqdm

import config as cfg


class Scraper:
    def __init__(self) -> None:
        self.no_batches = cfg.NO_BATCHES
        self.batch_size = cfg.BATCH_SIZE
        self.timeout = cfg.TIMEOUT  # seconds
        self.rand_url = cfg.RAND_WIKI

        self.headers = self._load_headers()

    def scrape_article(self, text) -> Union[pd.DataFrame, None]:
        """
        Scrape given wikipedia article based on given url or title and return it as pandas DataFrame object.
        """
        url = self._convert_to_url(text)
        r = requests.get(url, headers=self._get_random_header())

        if r.status_code == 200:
            return pd.DataFrame(
                columns=[cfg.PD_URL, cfg.PD_TITLE, cfg.PD_TEXT],
                data=[[r.url, r.url.split("/")[-1], r.text]],
            )

    def scrape_batches(self) -> pd.DataFrame:
        """
        Scrapes random wikipedia articles in batches and saves them to parquet file
        containing pandas DataFrame object with url, title and text.
        """
        documents = pd.DataFrame(columns=[cfg.PD_URL, cfg.PD_TITLE, cfg.PD_TEXT])
        for _ in tqdm(range(self.no_batches), desc="Batch"):
            for _ in tqdm(range(self.batch_size), desc="Request in batch", leave=False):
                r = requests.get(self.rand_url, headers=self._get_random_header())
                if r.status_code == 200 and r.url not in documents[cfg.PD_URL].values:
                    documents = documents.append(
                        {
                            cfg.PD_URL: r.url,
                            cfg.PD_TITLE: r.url.split("/")[-1],
                            cfg.PD_TEXT: r.text,
                        },
                        ignore_index=True,
                    )
            sleep(self.timeout)

        documents.to_parquet(cfg.WIKI_RESPONSES_PARQUET, compression=cfg.COMPRESS_ALG)
        print(f"Wikipedia responses saved to {str(cfg.WIKI_RESPONSES_PARQUET)}")

        return documents

    def _get_random_header(self):
        return choice(self.headers)

    def _convert_to_url(self, text):
        """Checks if text is already an url, if not, it is assumed to be a title and is converted to url"""
        if re.search(r"https?|www\.", text):
            # Is already an url
            return text

        return cfg.WIKI_LINK + text

    def _load_headers(self):
        with open(cfg.HEADERS, "r") as f:
            return json.load(f)[cfg.HEADERS_SECTION]


if __name__ == "__main__":
    Scraper().scrape_batches()
    documents: pd.DataFrame = pd.read_parquet(cfg.WIKI_RESPONSES_PARQUET)

    print(documents.memory_usage(deep=True))
    print(documents.head())
