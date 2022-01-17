import config as cfg

import pickle
from time import sleep

from tqdm import tqdm
import grequests

if __name__ == '__main__':
    responses = []
    
    for _ in tqdm(range(cfg.NO_BATCHES), desc='Batches'):
        rqs = (grequests.get(cfg.RAND_WIKI) for _ in range(cfg.BATCH_SIZE))
        _responses = grequests.map(rqs)
        _responses = [rs for rs in _responses if rs.status_code == 200]
        responses.extend(_responses)
        sleep(cfg.TIMEOUT)

    with open(cfg.WIKI_RESPONSES_PKL, 'wb') as f:
        pickle.dump(responses, f)