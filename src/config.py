from pathlib import Path

RAND_WIKI = "https://en.wikipedia.org/wiki/Special:Random"
WIKI_LINK = "https://en.wikipedia.org/wiki/"
BATCH_SIZE = 50
NO_BATCHES = 20
TIMEOUT = 1

PD_URL = "url"
PD_TEXT = "text"
PD_TITLE = "title"
HEADERS_SECTION = "headers"

COMPRESS_ALG = "brotli"
NLTK_MODEL = "en_core_web_md"

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT.joinpath("data")
WIKI_RESPONSES_PARQUET = DATA_PATH.joinpath("wiki_responses.parquet")
WIKI_TEXT_PARQUET = DATA_PATH.joinpath("wiki_texts.parquet")
HEADERS = DATA_PATH.joinpath("headers.json")
