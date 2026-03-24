from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pages(scraped_data: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    all_chunks = []

    for page in scraped_data:
        chunks = splitter.split_text(page["text"])

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "url": page["url"],
                "title": page["title"]
            })

    return all_chunks


# test it
if __name__ == "__main__":
    test_data = [
        {
            "url": "https://example.com",
            "title": "Test Page",
            "text": "This is a test. " * 200
        }
    ]

    chunks = chunk_pages(test_data)
    print(f"Total chunks created: {len(chunks)}")
    print(f"\nFirst chunk:\n{chunks[0]['text']}")
    print(f"\nSource: {chunks[0]['url']}")
