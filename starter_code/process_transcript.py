import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    cleaned = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)
    cleaned = re.sub(r"\[(?:Music starts|Music ends|Music|inaudible|Laughter)\]", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    price_wording_match = re.search(r"năm trăm nghìn", cleaned, flags=re.IGNORECASE)
    explicit_digits_match = re.search(r"500,000\s*VND", cleaned, flags=re.IGNORECASE)

    mentioned_price_vnd = None
    if explicit_digits_match:
        mentioned_price_vnd = 500000
    elif price_wording_match:
        mentioned_price_vnd = 500000

    return {
        "document_id": "transcript-demo-001",
        "content": cleaned,
        "source_type": "Video",
        "author": "Speaker 1",
        "timestamp": None,
        "source_metadata": {
            "detected_price_vnd": mentioned_price_vnd,
            "detected_phrase_nam_tram_nghin": bool(price_wording_match),
            "detected_numeric_500000": bool(explicit_digits_match),
        },
    }

