import re


def extract_price(price_text: str) -> float:
    price_match = re.search(r"\d+[\d\s]*[,.]?\d*", price_text)
    if price_match:
        return float(price_match.group().replace(" ", "").replace(",", "."))
    return 0.0
