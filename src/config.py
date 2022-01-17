from pathlib import Path

RAND_WIKI = 'https://en.wikipedia.org/wiki/Special:Random'
BATCH_SIZE = 50
NO_BATCHES = 50
TIMEOUT = 5

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT.joinpath('data')
WIKI_RESPONSES_PKL = DATA_PATH.joinpath('wiki_responses.pkl')