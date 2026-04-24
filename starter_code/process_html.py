import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # BeautifulSoup is required for robust HTML table extraction.
        return []

    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    table = soup.find("table", {"id": "main-catalog"})
    if table is None:
        return []

    def parse_vnd_price(value):
        text = value.strip()
        if text.lower() in {"n/a", "liên hệ", "lien he", "null", "none", ""}:
            return None
        digits = re.sub(r"[^\d\-]", "", text)
        if not digits:
            return None
        try:
            return float(digits)
        except ValueError:
            return None

    records = []
    for row in table.select("tbody tr"):
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) != 6:
            continue

        sku, name, category, listed_price, stock_text, rating = cols
        stock = None
        try:
            stock = int(stock_text)
        except ValueError:
            pass

        normalized_price = parse_vnd_price(listed_price)

        records.append(
            {
                "document_id": f"html-product-{sku.lower()}",
                "content": (
                    f"Product {name} ({sku}) in category {category}; "
                    f"listed price: {normalized_price if normalized_price is not None else 'unknown'} VND; "
                    f"stock: {stock if stock is not None else 'unknown'}; rating: {rating}."
                ),
                "source_type": "HTML",
                "author": "vinshop_catalog",
                "timestamp": None,
                "source_metadata": {
                    "sku": sku,
                    "category": category,
                    "listed_price_raw": listed_price,
                    "listed_price_vnd": normalized_price,
                    "stock_quantity": stock,
                    "rating": rating,
                },
            }
        )

    return records

