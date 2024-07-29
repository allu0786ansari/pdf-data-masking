import re

def mask_sensitive_info(text):
    name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    clinic_pattern = r'(?i)clinic\s?[A-Z][a-z]*'
    
    text = re.sub(name_pattern, '[MASKED NAME]', text)
    text = re.sub(phone_pattern, '[MASKED PHONE]', text)
    text = re.sub(email_pattern, '[MASKED EMAIL]', text)
    text = re.sub(clinic_pattern, '[MASKED CLINIC]', text)
    
    return text
