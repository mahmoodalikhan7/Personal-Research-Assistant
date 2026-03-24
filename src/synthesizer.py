from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=4000
)

def synthesize_report(user_query: str, retrieved_chunks: list) -> str:
    # build context from retrieved chunks
    context = ""
    sources = []

    for i, chunk in enumerate(retrieved_chunks):
        context += f"[{i+1}] {chunk['text']}\n\n"
        if chunk["url"] not in sources:
            sources.append(chunk["url"])

    # build sources list for prompt
    sources_text = "\n".join([f"[{i+1}] {url}" for i, url in enumerate(sources)])

    prompt = f"""
You are an expert research analyst. Using ONLY the information provided below, write a deeply detailed and comprehensive research report.

USER QUESTION: {user_query}

RETRIEVED INFORMATION:
{context}

Write a structured report with these exact sections:

## Introduction
Write 3-4 paragraphs giving a thorough background on the topic. Explain why it matters, its history, and context.

## Key Findings
Write at least 5-7 detailed findings. Each finding should be 2-3 sentences long and cite its source inline as [1], [2] etc. Go deep — don't just skim the surface.

## Deep Dive
Pick the 2-3 most interesting or complex aspects of the topic and explain them in detail. Each sub-topic should be a paragraph of at least 4-5 sentences.

## Contradictions & Open Debates
Write 2-3 paragraphs about where experts disagree, what is still unknown, and what debates exist around this topic.

## Conclusion
Write 2-3 paragraphs summarizing the key takeaways and what the future looks like for this topic.

## Sources

Rules:
- Only use information from the retrieved chunks above
- Cite sources inline as [1], [2], [3] etc.
- Be thorough, detailed and analytical — this is a professional research report
- Minimum 1500 words. Be as detailed and thorough as possible.
- Under ## Sources, list the URLs provided below

SOURCES TO LIST:
{sources_text}
"""



    response = llm.invoke(prompt)
    return response.content


# test it
if __name__ == "__main__":
    test_chunks = [
        {"text": "Amyloid plaques are a hallmark of Alzheimer's disease and form between neurons.", "url": "https://brightfocus.org", "title": "Plaques"},
        {"text": "Tau protein tangles disrupt communication between brain cells and cause cell death.", "url": "https://nih.gov", "title": "Tau"},
        {"text": "The APOE4 gene is the strongest known genetic risk factor for Alzheimer's disease.", "url": "https://nature.com", "title": "Genetics"},
        {"text": "Some researchers debate whether amyloid plaques are a cause or a symptom of Alzheimer's.", "url": "https://sciencedaily.com", "title": "Debate"},
    ]

    report = synthesize_report("What causes Alzheimer's disease?", test_chunks)
    print(report)
