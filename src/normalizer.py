from pathlib import Path
from typing import Union

import spacy
import nltk
import pandas as pd

from nltk import word_tokenize

import config as cfg

from purifier import Purifier

# pd.apply(df["text"], axis=1, func=normalizer.normalize)
# pd.apply(df_query["text"], axis=1, func=normalizer.normalize)

class Normalizer:
    def __init__(self) -> None:
        self._download_nltk_packages()

        self.nlp = spacy.load(cfg.NLTK_MODEL)
        self.stop_words = self.nlp.Defaults.stop_words
        self.stop_words.update(["(", ")", ",", ".", ":", "-"])

    def normalize(self, text: str) -> str:
        tokens = [token.lower() for token in word_tokenize(text)]
        cleared = [word for word in tokens if word not in self.stop_words]

        return " ".join(cleared)

    # def save(self, path: Path):
    #     if not path.parent.exists():
    #         raise Exception("Normalizer save path doesn't exists")
    #     if self.documents is None:
    #         print("No documents to save")

    #     self.documents.to_parquet(str(path), compress=cfg.COMPRESS_ALG)

    def _download_nltk_packages(self):
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("wordnet")
