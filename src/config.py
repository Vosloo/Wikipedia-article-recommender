from pathlib import Path

RAND_WIKI = "https://en.wikipedia.org/wiki/Special:Random"
WIKI_LINK = "https://en.wikipedia.org/wiki/"

NO_ARTICLES = 1000
BATCH_SIZE = 50
TIMEOUT = 1
# TODO Create timestamp at program start and add it to all generated file
TIMESTAMP = ""

MIN_DF = 1
NO_RECOMMENDATIONS = 5
SAVE_RECOMMENDATIONS = True

PD_URL = "url"
PD_TEXT = "text"
PD_TITLE = "title"
PD_SIMILARITY = "similarity"
HEADERS_SECTION = "headers"

COMPRESS_ALG = "brotli"
NLTK_MODEL = "en_core_web_md"

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT.joinpath("data")

HEADERS = DATA_PATH.joinpath("headers.json")

WIKI_TEXT_PARQUET = DATA_PATH.joinpath("wiki_texts.parquet")
WIKI_RESPONSES_PARQUET = DATA_PATH.joinpath("wiki_responses.parquet")
WIKI_RECOMMENDATIONS_CSV = DATA_PATH.joinpath("wiki_recommendations.csv")
