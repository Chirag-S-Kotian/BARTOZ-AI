import streamlit as st
import requests
import re

# --- Page Config & Sidebar ---
st.set_page_config(page_title="AI Research Assistant", page_icon="🧠", layout="centered")

# Sidebar: About, Tips, Features, Open Source
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/000000/artificial-intelligence.png", width=60)
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
<h1 style='text-align:center; font-size:2.6rem;letter-spacing:2px;margin-bottom:0.2em;'>BARTOZ-AI</h1>
<p style='text-align:center; font-size:1.25rem; color:#555; margin-top:0;'>
  <b>Open Source AI/ML/LLM Research Assistant</b><br>
  <span style='font-size:1.05rem;'>by <a href='https://github.com/Chirag-S-Kotian' target='_blank'>Chirag S Kotian</a></span>
</p>
<p style='text-align:center; font-size:1.05rem;'>
  Your expert assistant for all things <b>AI, ML, LLMs, AI agents, and companies</b>.<br>
  Powered by Retrieval-Augmented Generation (RAG), Gemini, DeepSeek, and open data sources.
</p>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

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
                st.markdown("""
                <div style='background:linear-gradient(90deg,#e0e7ff 0%,#f0f8ff 100%);padding:24px 20px;border-radius:10px;border:1px solid #c7d2fe;margin-bottom:24px;color:#222;font-size:1.15rem;'>
                <b>🧠 Answer</b><br><br>{}</div>
                """.format(main_answer), unsafe_allow_html=True)
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
                    st.info("No supporting documents or context found in the response.")
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