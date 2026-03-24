from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_search_queries(user_query: str) -> list:
    prompt = f"""
    You are a research assistant. A user wants to research the following topic:
    "{user_query}"
    
    Generate exactly 3 optimized search queries to find the best information about this topic.
    Return ONLY a Python list of 3 strings. Nothing else. No explanation. No extra text.
    
    Example format:
    ["query one", "query two", "query three"]
    """
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    # parse the list from the response
    queries = eval(content)
    return queries


# test it
if __name__ == "__main__":
    queries = generate_search_queries("What causes Alzheimer's disease?")
    print(queries)
