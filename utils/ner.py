import spacy

nlp = spacy.load('xx_ent_wiki_sm')

def identify_names(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    return names