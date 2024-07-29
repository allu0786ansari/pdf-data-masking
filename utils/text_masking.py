import re
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# Create a pipeline for NER
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# Regular expressions for patterns
patterns = {
    "phone": re.compile(r"\b\d{10}\b|\+\d{1,3}\s?\d{10}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "account": re.compile(r"\b\d{10,16}\b"),
    "ifsc": re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "passport": re.compile(r"\b[A-Z0-9]{6,9}\b"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b"),
}

def mask_sensitive_info(text):
    # Apply regular expressions for additional patterns
    for key, pattern in patterns.items():
        text = pattern.sub("[MASKED]", text)
    
    # Use NER model for names, organizations, and locations
    ner_results = nlp(text)
    masked_text = text

    for entity in ner_results:
        if entity['entity'] in ["B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]:
            start = entity['start']
            end = entity['end']
            masked_text = masked_text[:start] + "[MASKED]" + masked_text[end:]

    return masked_text
