import spacy

nlp = spacy.load("en_core_web_sm")

def extract_sentences(text):
    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    #drop the last sentense in case it is incomplete
    sentences = sentences[1:-1]
    return sentences
