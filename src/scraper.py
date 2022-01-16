import json
import re
from time import sleep, perf_counter
from typing import List

from random import random
import numpy as np
import pandas as pd
# import grequests
import requests
import spacy
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

from purifier import Purifier

# (min_timeout, max_timeout)
REQUEST_TIMEOUT = (3, 5)
# how may synchronous requests before timeout
BATCH_SIZE = 20

RAND_WIKI = "https://en.wikipedia.org/wiki/Special:Random"
TF_IDF_WIKI = "https://en.wikipedia.org/wiki/Tf%E2%80%93idf"

# TODO: request Session for cookies


def get_random_header(headers: List[dict]) -> dict:
    return headers[np.random.randint(len(headers)) - 1]



if __name__ == "__main__":    
    with open("data/headers.json", "r") as infile:
        headers: List[dict] = json.load(infile)["headers"]

    start = perf_counter()
    no_docs = 0
    while no_docs < 2000:

        http = requests.get(RAND_WIKI, headers=get_random_header(headers))

        if http.status_code == 200:
            print(http.url)
            purifier = Purifier(http.text)
            purified = purifier.purify_text(purifier.process_paragraphs())
        else:
            print(f"ERROR: {http.status_code} {http.url}")
            sleep(REQUEST_TIMEOUT)
            continue

        no_docs += 1
        if no_docs % BATCH_SIZE == 0:
            sleep(np.random.randint(*REQUEST_TIMEOUT))

    print(f"Time elapsed: {perf_counter() - start}")

# ID, URL, RAW_HTML, PURIFIED_HTML
