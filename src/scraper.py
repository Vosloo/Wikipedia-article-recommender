import config as cfg
from purifier import Purifier

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import pickle
import pandas as pd

if __name__ == "__main__":    
    with open(cfg.WIKI_RESPONSES_PKL, "rb") as f:
        responses = pickle.load(f)

    articles = pd.DataFrame(columns=[cfg.PD_URL, cfg.PD_TEXT])

    for res in responses:
        purifier = Purifier(res.text)
        purified = purifier.purify_text(purifier.process_paragraphs())

        print(repr(purified), res.url)
        break
    