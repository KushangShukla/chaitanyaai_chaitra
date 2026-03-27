import re

def extract_store(query):
    match=re.search(r"store\s+(\d+)",query.lower())

    if match:
        return int(match.group(1))
    
    return None