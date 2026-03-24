# Personal Research Assistant

An AI-powered research tool that takes any topic or question, searches the web, reads and filters results, and synthesizes them into a structured PDF report with citations.

## Live Demo
[Click here to try it](https://personal-research-assistant-muck956sd3sy6pchwg89tc.streamlit.app/)

## How It Works

1. **Agent Query Planner** — LLaMA 3.3 70B expands your query into 3 optimized search queries
2. **Web Search** — SerpAPI fetches top results for each query
3. **Scraper** — BeautifulSoup fetches and cleans each page
4. **Chunker** — Text is split into 500-token chunks
5. **RAG** — Chunks are embedded with sentence-transformers and stored in ChromaDB
6. **Retrieval** — Top 12 most relevant chunks are retrieved for your query
7. **Synthesis** — LLaMA 3.3 70B generates a structured report with citations
8. **PDF Export** — Report is exported as a clean PDF

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | LLaMA 3.3 70B via Groq API |
| Agentic Layer | LangChain |
| Search | SerpAPI |
| Scraping | BeautifulSoup4 |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| PDF Generation | fpdf2 |
| Frontend | Streamlit |
| Deployment | Streamlit Community Cloud |

## Project Structure
```
research-assistant/
│
├── src/
│   ├── agent.py          # LLM query planner
│   ├── search.py         # SerpAPI web search
│   ├── scraper.py        # Web scraping & cleaning
│   ├── chunker.py        # Text chunking
│   ├── vector_store.py   # Embeddings & ChromaDB
│   └── synthesizer.py    # Report generation
│
├── app.py                # Streamlit UI
├── requirements.txt      # Dependencies
├── .env                  # API keys (not committed)
└── README.md
```

## Run Locally

1. Clone the repo
```bash
git clone https://github.com/mahmoodalikhan7/Personal-Research-Assistant.git
cd Personal-Research-Assistant
```

2. Create and activate conda environment
```bash
conda create -n ra python=3.11
conda activate ra
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add your API keys to `.env`
```
GROQ_API_KEY=your_groq_key
SERPAPI_KEY=your_serpapi_key
```

5. Run the app
```bash
streamlit run app.py
```

## API Keys Required

- **Groq API** — Free at [console.groq.com](https://console.groq.com)
- **SerpAPI** — Free tier at [serpapi.com](https://serpapi.com)

## 📄 License
MIT
```

Save with `Ctrl+S` then push:
```
git add README.md
git commit -m "add README"
git push