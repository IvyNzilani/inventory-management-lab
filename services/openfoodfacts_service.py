import requests

BASE_URL = "https://world.openfoodfacts.org"

class OpenFoodFactsService:

    @staticmethod
    def get_by_barcode(barcode):
        url = f"{BASE_URL}/api/v0/product/{barcode}.json"
        response = requests.get(url)
        if response.status_code != 200:
            return None, "Failed to reach OpenFoodFacts API"
        data = response.json()
        if data.get("status") != 1:
            return None, "Product not found in OpenFoodFacts"
        product = data["product"]
        return {
            "name":        product.get("product_name", "Unknown"),
            "brand":       product.get("brands", "Unknown"),
            "description": product.get("ingredients_text", "No description available"),
            "barcode":     barcode,
        }, None

    @staticmethod
    def search_by_name(name):
        url = f"{BASE_URL}/cgi/search.pl"
        params = {
            "search_terms":  name,
            "search_simple": 1,
            "action":        "process",
            "json":          1,
            "page_size":     5,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None, "Failed to reach OpenFoodFacts API"
        data     = response.json()
        products = data.get("products", [])
        if not products:
            return None, "No products found"
        results = []
        for p in products:
            results.append({
                "name":    p.get("product_name", "Unknown"),
                "brand":   p.get("brands", "Unknown"),
                "barcode": p.get("code", "Unknown"),
            })
        return results, None
