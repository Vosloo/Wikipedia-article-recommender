import json
from random import choice
from time import sleep

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

    def scrape_batches(self) -> None:
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

    def _get_random_header(self):
        return choice(self.headers)

    def _load_headers(self):
        with open(cfg.HEADERS, "r") as f:
            return json.load(f)[cfg.HEADERS_SECTION]


if __name__ == "__main__":
    Scraper().scrape_batches()
    documents: pd.DataFrame = pd.read_parquet(cfg.WIKI_RESPONSES_PARQUET)

    print(documents.memory_usage(deep=True))
    print(documents.head())
