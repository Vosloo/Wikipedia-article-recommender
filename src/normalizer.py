import nltk
import spacy
from nltk import word_tokenize

import config as cfg


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

    def _download_nltk_packages(self):
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
