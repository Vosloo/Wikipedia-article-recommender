import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from collections import Counter

import config as cfg

sns.set(style="darkgrid")

def load_data():
    return pd.read_parquet(cfg.WIKI_PARSED_PARQUET_PATH)

def _count_words(data: pd.DataFrame) -> pd.DataFrame:
    db_counter = Counter()
    for _, item in data[cfg.PD_TEXT].iteritems():
        db_counter.update(item.split())

    return pd.DataFrame(columns=["word", "count"], data=db_counter.most_common())

def n_most_frequent_words(word_frequency: pd.DataFrame, n: int = 10) -> None:
    ax = sns.barplot(x="word", y="count", data=word_frequency.head(n))
    plt.xticks(rotation=45)
    plt.title("Top ten most frequent words in database")
    plt.show()


def word_length_frequency(word_frequency: pd.DataFrame) -> None:
    word_len_frequency = word_frequency.copy()
    word_len_frequency["length"] = word_len_frequency["word"].apply(lambda x: len(x))
    word_len_frequency_v2 = word_len_frequency.groupby(by='length').sum().reset_index()
    
    # ax = sns.barplot(x="length", y="count", data=word_len_frequency)
    # plt.xticks(rotation=45)
    # plt.title("Top ten most frequent words in database")
    # plt.show()
    for w in word_len_frequency[word_len_frequency['length'] > 15]['word'].values:
        print(w)


if __name__ == "__main__":
    data = load_data()
    word_frequency = _count_words(data)
    # n_most_frequent_words(word_frequency)
    word_length_frequency(word_frequency)
    
    # vectorizer = TfidfVectorizer().fit(data[cfg.PD_TEXT])
    # db_tfidf = TfidfVectorizer().fit_transform(data[cfg.PD_TEXT])
    # similarity = cosine_similarity(db_tfidf, db_tfidf)

    # print(vectorizer.get_feature_names_out())

