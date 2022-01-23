from typing import Union
from pathlib import Path

import config as cfg
from normalizer import Normalizer
from purifier import Purifier
from recommender import Recommender
from scraper import Scraper

import pandas as pd


class Controller:
    def __init__(
        self,
        to_scrape: int,
        refresh: bool,
        reparse: bool,
        input_path: Path,  # Path to file with user input (urls or titles)
    ) -> None:
        self.input_path = input_path
        self.to_scrape = to_scrape
        self.refresh = refresh
        self.reparse = reparse

        self.normalizer = Normalizer()
        self.purifier = Purifier()
        self.scraper = Scraper(to_scrape)
        self.recommender = Recommender()

    def run(self):
        if self.to_scrape or self.reparse:
            scraped = self._scrape()
            parsed = self._parse_data(scraped)
            self._save_parsed(parsed)

        if self.input_path is not None:
            self._recommender()

    def _scrape(self) -> pd.DataFrame:
        """Runs scraper and saves scraped responses to parquet file"""
        if not self.refresh and cfg.WIKI_RESPONSES_PARQUET_PATH.is_file():
            return self._load_responses()

        return self.scraper.scrape_batches()

    def _parse_data(self, scraped: pd.DataFrame) -> pd.DataFrame:
        """Loads pandas DataFrame object with raw html texts and parses them inplace"""
        if not self.refresh and not self.reparse and cfg.WIKI_PARSED_PARQUET_PATH.is_file():
            return self._load_parsed()

        print("Parsing articles...")
        scraped[cfg.PD_TEXT] = scraped[cfg.PD_TEXT].apply(
            lambda x: self.purifier.purify_after_lemma(
                self.normalizer.normalize(
                    self.purifier.purify_text(self.purifier.process_paragraphs(x))
                )
            )
        )

        return scraped

    def _recommender(self) -> None:
        """Recommends articles (and saves them to data/ directory) based on given query"""
        print("Calculating recommendations...")
        query_documents: pd.DataFrame = self._load_input()
        db_documents: pd.DataFrame = self._load_parsed()

        recommendations = self.recommender.get_recommendations(
            db_documents, query_documents, cfg.NO_RECOMMENDATIONS
        )

        print("\nRecommendations:")
        lst_rec = list(map(list, recommendations[[cfg.PD_URL, cfg.PD_SIMILARITY]].values))
        for url, sim in lst_rec:
            print(f"With similarity of {sim:.4f} - {url}")

    def _load_parsed(self) -> pd.DataFrame:
        """Loads pandas DataFrame object with parsed texts"""
        return pd.read_parquet(str(cfg.WIKI_PARSED_PARQUET_PATH))

    def _save_parsed(self, parsed: pd.DataFrame) -> None:
        """Saves pandas DataFrame object with parsed texts"""
        parsed.to_parquet(str(cfg.WIKI_PARSED_PARQUET_PATH), compression=cfg.COMPRESS_ALG)
        print(f"Wikipedia parsed texts saved to {str(cfg.WIKI_PARSED_PARQUET_PATH)}")

    def _load_responses(self) -> pd.DataFrame:
        """Loads pandas DataFrame object with scraped responses"""
        return pd.read_parquet(str(cfg.WIKI_RESPONSES_PARQUET_PATH))

    def _load_input(self) -> pd.DataFrame:
        """Loads user input data"""

        with open(str(self.input_path), "r") as f:
            input_text = f.readlines()

        query_documents = pd.concat(
            [self.scraper.scrape_article(text.rstrip("\n")) for text in input_text],
            ignore_index=True,
        )

        query_documents[cfg.PD_TEXT] = query_documents[cfg.PD_TEXT].apply(
            lambda x: self.purifier.purify_after_lemma(
                self.normalizer.normalize(
                    self.purifier.purify_text(self.purifier.process_paragraphs(x))
                )
            )
        )

        return query_documents
