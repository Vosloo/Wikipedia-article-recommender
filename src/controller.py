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
        input_path: Path,
        data_path: Path,
        responses_path: Path,
    ) -> None:
        self.input_path = input_path
        self.data_path = data_path
        self.responses_path = responses_path
        self.query_documents: Union[pd.DataFrame, None] = None
        self.documents: Union[pd.DataFrame, None] = None

        self.normalizer = Normalizer()
        self.purifier = Purifier()
        self.scraper = Scraper()
        self.recommender = Recommender()

    def run(self):
        self._scrape()
        self._parse_data()
        self._load_input()
        self._recommender()

    def _scrape(self) -> None:
        """Runs scraper and saves scraped responses to parquet file"""
        if self.data_path:
            return

        if self.responses_path and self.responses_path.is_file():
            self._load_responses()
            return

        self.documents = self.scraper.scrape_batches()

    def _parse_data(self) -> None:
        """Loads pandas DataFrame object with raw html texts"""
        # 1. Load DataFrame with raw html texts
        # 2. Apply general purifying
        # 3. Apply normalization
        # 4. Apply purifying after normalization
        # 5. Save parsed data to parquet file

        if self.data_path and self.data_path.is_file():
            self._load_parsed()
            return

        self.documents[cfg.PD_TEXT] = self.documents[cfg.PD_TEXT].apply(
            lambda x: self.purifier.purify_after_lemma(
                self.normalizer.normalize(
                    self.purifier.purify_text(self.purifier.process_paragraphs(x))
                )
            )
        )

        self._save_parsed()

    def _recommender(self) -> None:
        """Recommends articles based on given query"""

        print(
            self.recommender.get_recommendations(self.documents, self.query_documents)
        )

    def _load_parsed(self) -> None:
        """Loads pandas DataFrame object with parsed texts"""
        self.documents = pd.read_parquet(str(self.data_path))

    def _save_parsed(self) -> None:
        """Saves pandas DataFrame object with parsed texts"""
        self.documents.to_parquet(
            str(cfg.WIKI_TEXT_PARQUET), compression=cfg.COMPRESS_ALG
        )
        print(f"Wikipedia parsed texts saved to {str(cfg.WIKI_TEXT_PARQUET)}")

    def _load_responses(self) -> None:
        """Loads pandas DataFrame object with scraped responses"""
        self.documents = pd.read_parquet(str(self.responses_path))

    def _load_input(self) -> None:
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

        self.query_documents = query_documents
