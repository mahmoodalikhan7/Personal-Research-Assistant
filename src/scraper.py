import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_pages(search_results: list) -> list:
    scraped_data = []

    for result in search_results:
        url = result["url"]
        title = result["title"]

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # remove junk
            for tag in soup(["nav", "script", "style", "footer", "header", "aside"]):
                tag.decompose()

            # extract paragraph text
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs])
            text = text.strip()

            # skip if barely any text
            if len(text) < 200:
                print(f"SKIPPED (too short): {url}")
                continue

            scraped_data.append({
                "url": url,
                "title": title,
                "text": text
            })
            print(f"SCRAPED: {title}")

        except Exception as e:
            print(f"FAILED: {url} — {e}")
            continue

    return scraped_data


# test it
if __name__ == "__main__":
    test_results = [
        {"url": "https://www.brightfocus.org/resource/what-are-alzheimers-plaques-and-tangles/", "title": "What are Alzheimer's Plaques and Tangles?"},
        {"url": "https://www.sciencedaily.com/releases/2026/02/260215225555.htm", "title": "Scientists discover brain switches"}
    ]
    pages = scrape_pages(test_results)
    for page in pages:
        print(f"\n--- {page['title']} ---")
        print(page["text"][:300])
