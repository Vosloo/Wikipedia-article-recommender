import requests
import spacy
from spacy import displacy

from purifier import Purifier

RAND_WIKI = "https://en.wikipedia.org/wiki/Special:Random"

if __name__ == "__main__":
    html = requests.get(RAND_WIKI)

    purifier = Purifier(html.text)
    purified = purifier.purify_text(purifier.raw_text)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(purified)

    displacy.serve(doc, style="ent")

    # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
