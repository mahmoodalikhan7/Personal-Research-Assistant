import streamlit as st
from src.agent import generate_search_queries
from src.search import search_web, search_images
from src.scraper import scrape_pages
from src.chunker import chunk_pages
from src.vector_store import store_and_retrieve
from src.synthesizer import synthesize_report
from src.pdf_generator import generate_pdf

st.set_page_config(page_title="Research Assistant", page_icon="🔍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #050508 !important;
    color: #e2e2f0 !important;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.hero-wrap {
    min-height: 40vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 24px;
    position: relative;
    overflow: hidden;
}

.hero-wrap::before {
    content: '';
    position: fixed;
    top: -40%;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    height: 600px;
    background: radial-gradient(ellipse, rgba(124,58,237,0.15) 0%, rgba(37,99,235,0.08) 40%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 500;
    color: #a78bfa;
    letter-spacing: 0.05em;
    margin-bottom: 32px;
    position: relative;
    z-index: 1;
}

.badge-dot {
    width: 6px;
    height: 6px;
    background: #a78bfa;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(48px, 8vw, 96px) !important;
    font-weight: 800 !important;
    line-height: 1.0 !important;
    text-align: center !important;
    margin-bottom: 24px !important;
    position: relative;
    z-index: 1;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 40%, #60a5fa 70%, #34d399 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.hero-sub {
    font-size: 18px;
    color: #6b6b80;
    text-align: center;
    max-width: 480px;
    line-height: 1.6;
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
    color: #e8e8f0 !important;
    font-size: 17px !important;
    padding: 20px 24px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s !important;
}

.stTextInput > div > div > input::placeholder {
    color: #3a3a4a !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(167,139,250,0.5) !important;
    background: rgba(167,139,250,0.05) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.1), 0 0 40px rgba(167,139,250,0.1) !important;
    outline: none !important;
}

.stTextInput label { display: none !important; }

.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 48px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    margin-top: 12px !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.3) !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(124,58,237,0.45) !important;
}

.stDownloadButton > button {
    background: transparent !important;
    color: #a78bfa !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}

.stDownloadButton > button:hover {
    background: rgba(167,139,250,0.08) !important;
    border-color: rgba(167,139,250,0.6) !important;
}

.stSpinner > div { border-top-color: #a78bfa !important; }

hr { border-color: rgba(255,255,255,0.06) !important; }

.report-body {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(167,139,250,0.15);
    border-radius: 20px;
    padding: 48px;
    margin-top: 16px;
    box-shadow: 0 0 80px rgba(124,58,237,0.08);
}
</style>
""", unsafe_allow_html=True)

# hero section
st.markdown("""
<div class="hero-wrap">
    <div class="badge"><span class="badge-dot"></span> AI · RAG · LLaMA 3.3 · Groq</div>
    <div class="hero-title">Research.<br>Instantly.</div>
    <div class="hero-sub">Ask any question. Get a fully sourced, synthesized research report in seconds.</div>
</div>
""", unsafe_allow_html=True)

# centered input
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_query = st.text_input("", placeholder="What do you want to research?")
    run = st.button("Generate Report") or (user_query and st.session_state.get("last_query") != user_query)
    if run:
        st.session_state["last_query"] = user_query
if run:
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.spinner("Planning search queries..."):
                queries = generate_search_queries(user_query)
                st.success(f"✅ Generated {len(queries)} search queries")

            with st.spinner("Searching the web..."):
                search_results = search_web(queries)
                st.success(f"✅ Found {len(search_results)} unique URLs")

            with st.spinner("Reading and cleaning pages..."):
                scraped_pages = scrape_pages(search_results)
                st.success(f"✅ Scraped {len(scraped_pages)} pages")

            with st.spinner("Running RAG retrieval..."):
                chunks = chunk_pages(scraped_pages)
                retrieved_chunks = store_and_retrieve(chunks, user_query, top_k=12)
                st.success(f"✅ Retrieved {len(retrieved_chunks)} relevant chunks")

            with st.spinner("Fetching relevant images..."):
                images = search_images(user_query)

            with st.spinner("Synthesizing report with LLaMA 3.3..."):
                report = synthesize_report(user_query, retrieved_chunks)


        col1, col2, col3 = st.columns([0.5, 3, 0.5])
        with col2:
            st.markdown('<div class="report-body">', unsafe_allow_html=True)
            st.markdown(f"### 📄 {user_query}")

            if images:
                img_cols = st.columns(len(images))
                for i, img_url in enumerate(images):
                    with img_cols[i]:
                        st.image(img_url, use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(report)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            pdf_bytes = generate_pdf(user_query, report, images)
            st.download_button(
                label="⬇️ Download Report as PDF",
                data=pdf_bytes,
                file_name="research_report.pdf",
                mime="application/pdf"
            )