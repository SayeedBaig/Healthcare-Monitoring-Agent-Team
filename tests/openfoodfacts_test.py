# tests/openfoodfacts_test.py
import requests, json
from pathlib import Path

def search_product(product_name="apple"):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 3
    }
    r = requests.get(url, params=params, timeout=15)
    print("Status:", r.status_code)
    return r.json()

if __name__ == "__main__":
    data = search_product("apple")

    # Always save correctly no matter where script runs
    save_path = Path(__file__).resolve().parent.parent / "docs" / "api_samples" / "openfoodfacts_sample.json"
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Data saved successfully at: {save_path}")
