import re
import string

import spacy
from unidecode import unidecode

nlp = spacy.load("en_core_web_sm")
CHARS = set(string.ascii_letters + string.digits + ' ! ? . \n \'')
MIN_WORDS = 3

def extract_sentences(text):

    text = unidecode(text)
    text = ''.join(c for c in text if c in CHARS)
    text = text.replace('\n', ' ')
    text = re.sub(" +", " ", text)

    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    # Drop the last sentense in case it is incomplete.
    sentences = sentences[:-1]
    # Remove very short sentences.
    sentences = [s for s in sentences if len(s.split()) >= MIN_WORDS]
    return sentences
