import pandas as pd
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    df = df.drop_duplicates(subset=["id"], keep="first")

    def parse_price(value):
        if pd.isna(value):
            return None
        text = str(value).strip()
        lower = text.lower()
        if lower in {"n/a", "null", "none", "liên hệ", "lien he", ""}:
            return None
        if "five dollars" in lower:
            return 5.0

        cleaned = re.sub(r"[^0-9.\-]", "", text)
        if cleaned in {"", "-", ".", "-."}:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None

    def normalize_date(value):
        if pd.isna(value):
            return None
        text = str(value).strip()
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%d %b %Y",
            "%B %dth %Y",
        ]
        for fmt in formats:
            try:
                return pd.to_datetime(text, format=fmt, errors="raise").date().isoformat()
            except (ValueError, TypeError):
                continue
        parsed = pd.to_datetime(text, errors="coerce")
        if pd.isna(parsed):
            return None
        return parsed.date().isoformat()

    documents = []
    for idx, row in df.iterrows():
        price_value = parse_price(row.get("price"))
        normalized_date = normalize_date(row.get("date_of_sale"))

        content = (
            f"Product: {row.get('product_name', '')}; "
            f"Category: {row.get('category', '')}; "
            f"Price: {price_value if price_value is not None else 'unknown'} "
            f"{row.get('currency', '')}; "
            f"Date of sale: {normalized_date or 'unknown'}."
        )

        documents.append(
            {
                "document_id": f"csv-sale-{int(row['id'])}",
                "content": content,
                "source_type": "CSV",
                "author": "sales_system",
                "timestamp": normalized_date,
                "source_metadata": {
                    "seller_id": row.get("seller_id"),
                    "stock_quantity": None
                    if pd.isna(row.get("stock_quantity"))
                    else int(float(row.get("stock_quantity"))),
                    "price_raw": row.get("price"),
                    "price_value": price_value,
                    "currency": row.get("currency"),
                },
            }
        )

    return documents

