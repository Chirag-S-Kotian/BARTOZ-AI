import streamlit as st
import requests
import re

# --- Page Config & Sidebar ---
st.set_page_config(page_title="AI Research Assistant", page_icon="🧠", layout="wide")

# --- Theme Toggle ---
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

col1, col2 = st.columns([8,1])
with col2:
    if st.button('🌙' if st.session_state['theme']=='light' else '☀️', key='theme_toggle'):
        st.session_state['theme'] = 'dark' if st.session_state['theme']=='light' else 'light'

if st.session_state['theme'] == 'dark':
    st.markdown("""
        <style>
        body, .stApp {background: #18181b !important; color: #e5e7eb !important;}
        .bartoz-title, .bartoz-desc, .bartoz-author {color: #e5e7eb !important;}
        .card {background: #23272f !important; color: #e5e7eb !important;}
        .sample-query-btn {background: linear-gradient(90deg,#818cf8 0%,#38bdf8 100%) !important; color: #fff;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp {background: linear-gradient(120deg, #e0e7ff 0%, #f0f8ff 100%) !important;}
        .card {background: #fff !important; color: #222 !important;}
        </style>
    """, unsafe_allow_html=True)

# Sidebar: About, Tips, Features, Open Source
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/000000/artificial-intelligence.png", width=60)
    # --- RAG DB Size ---
    try:
        db_size_resp = requests.get("http://localhost:8000/db_size", timeout=2)
        db_size = db_size_resp.json().get("size", "-")
        if db_size == 0:
            st.warning("RAG DB Size: 0 chunks (database may be empty or not loaded, try refreshing or re-indexing)")
        else:
            st.markdown(f"**📦 RAG DB Size:** {db_size} chunks")
    except Exception:
        st.markdown("**📦 RAG DB Size:** - (unavailable)")
    # --- Model Health Check ---
    if st.button("🩺 Check Model Health"):
        try:
            health = requests.get("http://localhost:8000/model_health", timeout=4).json()
            gemini = health.get("gemini", {})
            openrouter = health.get("openrouter", {})
            st.markdown(f"<b>Gemini Model:</b> <span style='color:{'green' if gemini.get('status')=='ok' else 'red'}'>{gemini.get('status','unknown')}</span> - {gemini.get('error','')}", unsafe_allow_html=True)
            st.markdown(f"<b>OpenRouter Model:</b> <span style='color:{'green' if openrouter.get('status')=='ok' else 'red'}'>{openrouter.get('status','unknown')}</span> - {openrouter.get('error','')}", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not check model health: {e}")
    st.info("No previous data is ever deleted during indexing or querying. All documents are preserved unless you manually delete the faiss_index directory.")
    # --- Database Preview ---
    if st.button("🔍 Preview Database (first 10 docs)"):
        try:
            preview_resp = requests.get("http://localhost:8000/docs_preview", timeout=4)
            preview = preview_resp.json().get("preview", [])
            if preview:
                st.markdown("<b>Database Preview (first 10 docs):</b>", unsafe_allow_html=True)
                for doc in preview:
                    st.markdown(f"""
                    <div class='card' style='margin-bottom:18px;padding:14px 14px 10px 14px;border-radius:8px;border:1px solid #c7d2fe;'>
                      <b>{doc['title']}</b><br>
                      <span style='color:#6366f1;font-size:0.97rem;'>{doc['source']} | {doc['published_date']}</span><br>
                      <span style='font-size:0.98rem;'>{doc['summary']}</span><br>
                      <a href='{doc['url']}' style='font-size:0.93rem;'>{doc['url']}</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No documents found in the database.")
        except Exception as e:
            st.warning(f"Could not fetch database preview: {e}")
    st.markdown("""
    # 🤖 About
    **BARTOZ-AI: Open Source AI Research Assistant**
    
    **by [Chirag S Kotian](https://github.com/Chirag-S-Kotian)**
    
    [![GitHub Repo](https://img.shields.io/badge/GitHub-BARTOZ--AI-181717?logo=github)](https://github.com/Chirag-S-Kotian/BARTOZ-AI)
    [![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://github.com/Chirag-S-Kotian/BARTOZ-AI)
    
    ---
    ## 💡 Usage Tips
    - Ask about the latest AI/ML/LLM breakthroughs
    - Compare AI agents, LLMs, or companies
    - Request sources for every answer
    
    **Examples:**
    - "Who are the top AI agents in 2025?"
    - "What is the latest research from OpenAI?"
    - "Compare Anthropic and Google DeepMind."
    - "List major LLM companies and their products."
    
    ---
    ## 🚀 Latest Features
    - Strict AI/ML/LLM/company focus
    - Brief, accurate, up-to-date answers
    - Sources: OpenAI, DeepMind, Anthropic, The Batch, arXiv, PubMed, SSRN, and more
    - Source citation and URLs
    - Unified RAG pipeline for both models
    - **Open Source: [Star us on GitHub!](https://github.com/Chirag-S-Kotian/BARTOZ-AI)**
    
    ---
    [GitHub](https://github.com/Chirag-S-Kotian/BARTOZ-AI) | [Docs](https://github.com/Chirag-S-Kotian/BARTOZ-AI#readme)
    """)

# --- Main Landing Page ---
# GitHub star button (live count)
import requests as _requests
from streamlit.components.v1 import html

def github_star_button(user, repo):
    api_url = f"https://api.github.com/repos/{user}/{repo}"
    try:
        stars = _requests.get(api_url, timeout=5).json().get("stargazers_count", "-")
    except Exception:
        stars = "-"
    html(f'''<a href="https://github.com/{user}/{repo}" target="_blank" style="text-decoration:none;">
    <button style="background:#181717;color:white;padding:8px 18px;border-radius:8px;border:none;font-size:1.1rem;display:flex;align-items:center;gap:10px;">
    <img src="https://img.icons8.com/ios-glyphs/24/ffffff/github.png" style="vertical-align:middle;"> Star on GitHub <span style="background:#333;padding:2px 8px;border-radius:8px;margin-left:5px;">{stars}</span>
    </button></a>''', height=44)

github_star_button("Chirag-S-Kotian", "BARTOZ-AI")

st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #e0e7ff 0%, #f0f8ff 100%);
}
.bartoz-title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 0.2em;
    background: linear-gradient(90deg, #6366f1 10%, #3b82f6 90%);
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
}
.bartoz-desc {
    text-align: center;
    font-size: 1.3rem;
    color: #333;
    margin-top: 0.1em;
    margin-bottom: 0.5em;
}
.bartoz-author {
    text-align: center;
    font-size: 1.08rem;
    color: #555;
    margin-bottom: 0.6em;
}
.sample-queries {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1.2em 0 1.7em 0;
    gap: 0.7em;
}
.sample-query-btn {
    background: linear-gradient(90deg,#6366f1 0%,#60a5fa 100%);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 1.05rem;
    padding: 0.5em 1.2em;
    cursor: pointer;
    transition: background 0.2s;
}
.sample-query-btn:hover {
    background: linear-gradient(90deg,#818cf8 0%,#38bdf8 100%);
}
@media (max-width: 600px) {
    .bartoz-title {font-size:2rem;}
    .bartoz-desc {font-size:1.08rem;}
    .bartoz-author {font-size:1rem;}
}
</style>
<div class='bartoz-title'>BARTOZ-AI <img src="https://img.icons8.com/ios-filled/50/6366f1/artificial-intelligence.png" width="40" style="vertical-align:middle;margin-left:10px;"/></div>
<div class='bartoz-desc'>Open Source AI/ML/LLM Research Assistant</div>
<div class='bartoz-author'>by <a href='https://github.com/Chirag-S-Kotian' target='_blank'>Chirag S Kotian</a></div>
<div style='display:flex;justify-content:center;margin:2em 0 1.2em 0;'>
    <input id='main-search' style='width:330px;max-width:95vw;padding:13px 18px;font-size:1.15rem;border-radius:10px;border:1.5px solid #c7d2fe;box-shadow:0 2px 8px #e0e7ff;' placeholder='Ask anything about AI, agents, LLMs...' autofocus />
    <button onclick="document.getElementById('main-search').focus();" style='margin-left:10px;background:linear-gradient(90deg,#6366f1 0%,#60a5fa 100%);color:#fff;border:none;border-radius:10px;padding:13px 22px;font-size:1.15rem;cursor:pointer;box-shadow:0 2px 8px #e0e7ff;'>🔍</button>
</div>
<div class='sample-queries'>
    <button class='sample-query-btn' onclick="window.parent.postMessage('sample_query:Who are the top AI agents in 2025?', '*');">🎲 Who are the top AI agents in 2025?</button>
    <button class='sample-query-btn' onclick="window.parent.postMessage('sample_query:What is the latest research from OpenAI?', '*');">🎲 What is the latest research from OpenAI?</button>
    <button class='sample-query-btn' onclick="window.parent.postMessage('sample_query:Compare Anthropic and Google DeepMind.', '*');">🎲 Compare Anthropic and Google DeepMind.</button>
</div>
<hr style='margin-top:2em;margin-bottom:1.5em;'>
""", unsafe_allow_html=True)


# --- Sample Query Button ---
sample_queries = [
    "Who are the top AI agents in 2025?",
    "What is the latest research from OpenAI?",
    "Compare Anthropic and Google DeepMind."
]
if st.button("🎲 Try a Sample Query"):
    import random
    st.session_state["query"] = random.choice(sample_queries)

# --- Query Form ---
with st.form("query_form", clear_on_submit=False):
    st.markdown("#### Enter your question about AI, AI agents, or AI companies:")
    query = st.text_area("", value=st.session_state.get("query", ""), height=90, key="query")
    model_option = st.selectbox(
        "Choose the model:",
        ["Gemini (Google AI Studio)", "DeepSeek (OpenRouter)"],
        help="Gemini is from Google AI Studio. DeepSeek is via OpenRouter."
    )
    submitted = st.form_submit_button("🔍 Ask")

# --- Model Mapping ---
if model_option == "Gemini (Google AI Studio)":
    model_name = "gemini"
elif model_option == "DeepSeek (OpenRouter)":
    model_name = "deepseek"
else:
    model_name = ""

# --- Handle Query Submission ---
if submitted:
    if not query.strip():
        st.warning("Please enter a question before submitting.")
    elif not model_name:
        st.error("Could not determine the selected model.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"query": query, "model": model_name}
                )
                response.raise_for_status()
                answer = response.json().get("response", "No response received from the backend.")
                # --- Parse answer for context and main answer ---
                context_match = re.search(r'Research Context:\s*(.*?)\s*User Question:', answer, re.DOTALL)
                main_answer_match = re.search(r'Answer:(.*)', answer, re.DOTALL)
                if main_answer_match:
                    main_answer = main_answer_match.group(1).strip()
                else:
                    main_answer = answer.strip()
                # --- Show main answer ---
                # Modern answer card
                st.markdown(f"""
                <div class='card' style='box-shadow:0 2px 12px #c7d2fe55;padding:28px 22px 22px 22px;border-radius:14px;border:1.5px solid #818cf8;margin-bottom:30px;max-width:750px;'>
                  <div style='font-size:1.15rem;font-weight:700;color:#6366f1;margin-bottom:0.3em;'>🧠 AI Research Answer</div>
                  <div style='font-size:1.14rem;line-height:1.7;'>{main_answer}</div>
                  <div style='font-size:0.96rem;color:#666;margin-top:0.8em;'>No previous data is ever deleted during indexing or querying. All documents are preserved unless you manually delete the faiss_index directory.</div>
                </div>
                """, unsafe_allow_html=True)
                # --- Show context/docs ---
                if context_match:
                    context = context_match.group(1).strip()
                    docs = re.split(r'--- Document \d+ ---', context)
                    docs = [doc.strip() for doc in docs if doc.strip()]
                    st.markdown("<b>Supporting Documents:</b>", unsafe_allow_html=True)
                    for idx, doc in enumerate(docs, 1):
                        title = re.search(r'Title:(.*)', doc)
                        source = re.search(r'Source:(.*)', doc)
                        url = re.search(r'URL:(.*)', doc)
                        published = re.search(r'Published:(.*)', doc)
                        content = re.search(r'Content:(.*)', doc, re.DOTALL)
                        with st.expander(f"Document {idx}: {title.group(1).strip() if title else 'No Title'}"):
                            st.markdown(f"**Source:** {source.group(1).strip() if source else 'Unknown'}")
                            if url:
                                st.markdown(f"**URL:** [{url.group(1).strip()}]({url.group(1).strip()})")
                            if published:
                                st.markdown(f"**Published:** {published.group(1).strip()}")
                            if content:
                                st.markdown(f"<span style='color:#111;'><b>Content:</b><br><br>{content.group(1).strip()}</span>", unsafe_allow_html=True)
                else:
                    st.info("""
No supporting documents or research context were found for your query. This means that, based on the current indexed database, there are no relevant documents or sources available to support an answer to your question.

What can you do next?
- Try rephrasing or broadening your question to cover a wider topic or timeframe.
- Re-index or update your data sources if you believe new research should be present.
- Remember: All previously indexed documents are preserved unless you manually delete the faiss_index directory.

For the most accurate results, ensure your question matches the topics and timeframes covered by your indexed documents. If you need the latest research, consider updating your sources or specifying your query more broadly.
""")
            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to the backend API. Please ensure it is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error during API request: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- Footer ---
st.markdown("""
<hr>
<div style='text-align:center;font-size:1rem;color:#444;margin-top:2em;'>
  Made with ❤️ by <a href='https://github.com/Chirag-S-Kotian' target='_blank'>Chirag S Kotian</a> | <a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI' target='_blank'>BARTOZ-AI Repo</a><br>
  <span style='font-size:0.95rem;'>Open Source · Powered by LangChain, Gemini, DeepSeek, and Streamlit</span>
</div>
""", unsafe_allow_html=True)