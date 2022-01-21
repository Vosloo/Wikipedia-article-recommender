import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config as cfg

sns.set(style="darkgrid")


def load_data():
    return pd.read_parquet(cfg.WIKI_TEXT_PARQUET)


if __name__ == "__main__":
    data = load_data()

    vectorizer = TfidfVectorizer().fit(data[cfg.PD_TEXT])
    db_tfidf = TfidfVectorizer().fit_transform(data[cfg.PD_TEXT])

    similarity = cosine_similarity(db_tfidf, db_tfidf)
    