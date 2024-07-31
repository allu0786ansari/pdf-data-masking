import re
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# Create a pipeline for NER
nlp_hf = pipeline("ner", model=model, tokenizer=tokenizer)

# Enhanced regular expressions for patterns
patterns = {
    "phone": re.compile(r"\b(?:\+\d{1,3}\s?)?\d{10,15}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "account": re.compile(r"\b\d{10,16}\b"),
    "ifsc": re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "passport": re.compile(r"\b[A-Z0-9]{6,9}\b"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b"),
}

def mask_sensitive_info(text):
    # Apply regular expressions for additional patterns first
    masked_text = text
    for key, pattern in patterns.items():
        masked_text = pattern.sub("[MASKED]", masked_text)
    
    # Use Hugging Face NER model
    ner_results = nlp_hf(masked_text)
    
    # Sort entities by start position and by length (longer entities first) to prioritize
    ner_results = sorted(ner_results, key=lambda x: (x['start'], -x['end']))
    
    # Masking overlaps and consolidate entities
    result = []
    last_end = 0
    masked_intervals = []

    for entity in ner_results:
        start, end = entity['start'], entity['end']
        
        # Update masked intervals if overlapping with current entity
        new_masked_intervals = []
        for (masked_start, masked_end) in masked_intervals:
            if masked_end > start:  # There's an overlap
                start = min(start, masked_start)
                end = max(end, masked_end)
            else:
                new_masked_intervals.append((masked_start, masked_end))
        masked_intervals = new_masked_intervals
        masked_intervals.append((start, end))

        if start > last_end:
            result.append(masked_text[last_end:start])
        # Masking entities detected by Hugging Face model
        if entity['entity'] in ["B-PER", "B-ORG", "B-LOC"]:
            result.append("[MASKED]")
        last_end = end

    # Append remaining part of the text
    result.append(masked_text[last_end:])
    
    return ''.join(result)

# Test with a variety of text samples
test_samples = [
    "John Doe's email is john.doe@example.com and his phone number is +1234567890.",
    "The account number 1234567890123456 and credit card number 1234-5678-9012-3456 are masked.",
    "For more information, visit our website or contact us at support@example.org.",
    "Your transaction ID is ABCD1234 and IFSC code is ABCD0000123."
]

for i, sample_text in enumerate(test_samples):
    print(f"Sample {i+1}:\n{mask_sensitive_info(sample_text)}\n")
