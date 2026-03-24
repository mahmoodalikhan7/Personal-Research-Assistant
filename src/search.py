import requests
from dotenv import load_dotenv
import os

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_web(queries: list) -> list:
    all_results = []
    seen_urls = set()

    for query in queries:
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": 5
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        organic_results = data.get("organic_results", [])

        for result in organic_results:
            url = result.get("link")
            title = result.get("title")
            snippet = result.get("snippet")

            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append({
                    "url": url,
                    "title": title,
                    "snippet": snippet
                })

    return all_results


# test it
if __name__ == "__main__":
    queries = ["alzheimer amyloid beta plaques", "tau protein neurodegeneration"]
    results = search_web(queries)
    for r in results:
        print(r["title"])
        print(r["url"])
        print()
def search_images(query: str) -> list:
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google_images",
        "num": 3
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    images = []
    for result in data.get("images_results", [])[:3]:
        url = result.get("original")
        if url:
            images.append(url)

    return images
