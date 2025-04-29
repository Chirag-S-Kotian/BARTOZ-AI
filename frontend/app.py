import streamlit as st
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Get backend URL from environment or default to localhost
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

st.set_page_config(page_title="AI Research Assistant", page_icon="", layout="wide")

# --- Minimal Modern CSS ---

st.markdown("""
<style>
body, .stApp {
    background: #18181b !important;
    color: #e5e7eb !important;
}


.bartoz-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2em 0 0.6em 0;
    margin-bottom: 0.6em;
    flex-wrap: wrap;
    background: #23232a;
    border-radius: 14px;
    box-shadow: 0 2px 12px #111a;
    border: 1.5px solid #23272f;
}


.bartoz-logo-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.3em;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    text-align: center;
}


.bartoz-logo {
    display: flex;
    align-items: center;
    gap: 0.7em;
    flex: 1;
}
.bartoz-logo-img {
    width: 54px;
    height: 54px;
    margin-bottom: 0.1em;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.bartoz-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #a5b4fc 10%, #38bdf8 90%);
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
    filter: brightness(1.15);
}
.bartoz-tagline {
    font-size: 1.08rem;
    color: #a5b4fc;
    margin-bottom: 0.6em;
    text-align: center;
    width: 100%;
}


.bartoz-gh-star-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.7em;
    width: 100%;
}
.bartoz-gh-star {
    display: flex;
    align-items: center;
    gap: 0.6em;
    font-size: 1.05rem;
    background: #23272f;
    color: #e5e7eb;
    padding: 7px 16px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: 600;
    box-shadow: 0 1px 6px #111a;
    transition: background 0.18s;
    border: none;
    outline: none;
    margin-left: 1em;
}


.bartoz-gh-star:hover {
    background: #333;
    color: #fff;
}

.bartoz-desc {
    text-align: center;
    font-size: 1.15rem;
    color: #d1d5db;
    margin: 0.7em 0 1.1em 0;
    background: #23232a;
    border-radius: 10px;
    padding: 0.7em 0.5em;
}


.card {
    background: #23232a;
    border-radius: 14px;
    box-shadow: 0 1px 8px #111a;
    border: 1.5px solid #303446;
    padding: 28px 22px 22px 22px;
    margin: 0 auto 30px auto;
    max-width: 750px;
    color: #e5e7eb;
}


.stTextArea textarea {
    font-size: 1.11rem;
    border-radius: 9px;
    border: 1.5px solid #303446;
    background: #18181b;
    color: #e5e7eb;
}


.stSelectbox, .stButton button {
    font-size: 1.09rem;
    border-radius: 8px;
    border: 1.5px solid #303446;
    background: #23232a;
    color: #e5e7eb;
}


.stButton button {
    background: linear-gradient(90deg,#6366f1 0%,#38bdf8 100%);
    color: #fff;
    padding: 0.5em 1.2em;
    font-weight: 600;
    border: none;
    box-shadow: 0 1px 6px #111a;
}


.stButton button:hover {
    background: linear-gradient(90deg,#818cf8 0%,#6366f1 100%);
    color: #fff;
    filter: brightness(1.1);
}


.st-expander {
    border-radius: 10px !important;
    border: 1px solid #303446 !important;
    background: #23232a !important;
    color: #e5e7eb !important;
}


.sample-queries-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5em;
    margin: 1.1em 0 0.7em 0;
}
.sample-query-pill {
    background: linear-gradient(90deg, #23272f 60%, #23232a 100%);
    color: #a5b4fc;
    border: 1.5px solid #6366f1;
    border-radius: 22px;
    padding: 0.38em 1.1em;
    font-size: 1.01rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 1px 6px #23272f55;
    transition: background 0.14s, color 0.14s, border 0.14s, box-shadow 0.14s;
    margin-bottom: 0.2em;
    user-select: none;
}
.sample-query-pill:hover {
    background: linear-gradient(90deg,#6366f1 0%,#38bdf8 100%);
    color: #fff;
    border-color: #38bdf8;
    box-shadow: 0 2px 12px #38bdf877;
}

.bartoz-footer {
    text-align: center;
    margin-top: 2.7em;
    margin-bottom: 0.7em;
    color: #a1a1aa;
    font-size: 1.07rem;
    background: #23232a;
    border-radius: 12px;
    padding: 1.6em 0 1.4em 0;
    box-shadow: 0 1px 8px #111a;
}
.bartoz-footer-links {
    margin-top: 0.7em;
    margin-bottom: 0.3em;
}
.bartoz-footer-links a {
    color: #38bdf8;
    margin: 0 0.7em;
    font-weight: 600;
    text-decoration: none;
    font-size: 1.06rem;
}
.bartoz-footer-links a:hover {
    color: #a5b4fc;
    text-decoration: underline;
}
.bartoz-footer-badges {
    margin-top: 0.5em;
}

.query-form-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.7em;
    padding: 1.4em 0 1.1em 0;
    background: linear-gradient(120deg, #23232a 60%, #23272f 100%) padding-box, linear-gradient(90deg, #6366f1 0%, #38bdf8 100%) border-box;
    border: 2.5px solid transparent;
    border-radius: 18px;
    box-shadow: 0 4px 28px #111a;
    max-width: 700px;
    margin: 0 auto 2.2em auto;
    position: relative;
    border-radius: 12px;
    padding: 1em 0;
}


.bartoz-footer a {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 600;
}


.bartoz-footer a:hover {
    text-decoration: underline;
}
@media only screen and (max-width: 768px) {
    .bartoz-header {
        flex-direction: column;
        align-items: center;
    }
    .bartoz-logo-center {
        margin-bottom: 1em;
    }
    .bartoz-gh-star {
        margin-left: 0;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Project Header / Navbar ---
st.markdown("""
<div class='bartoz-navbar'>
  <div class='bartoz-logo-center'>
    <img src='https://img.icons8.com/ios-filled/100/6366f1/artificial-intelligence.png' alt='AI Logo' class='bartoz-logo-img'/>
    <div class='bartoz-title'>BARTOZ-AI</div>
    <div class='bartoz-tagline'>Your Open Source AI/ML/LLM Research Assistant</div>
    <div class='bartoz-gh-star-center'>
      <a class='bartoz-gh-star-btn' href='https://github.com/Chirag-S-Kotian/BARTOZ-AI' target='_blank'>
        <img src='https://img.icons8.com/ios-glyphs/30/ffffff/github.png' width='22' style='vertical-align:middle;margin-right:2px;'/> Star on GitHub
      </a><br>
      <img src='https://img.shields.io/github/stars/Chirag-S-Kotian/BARTOZ-AI?style=social' alt='GitHub stars' style='margin-top:0.3em;'/>
    </div>
    <div class='bartoz-nav-links-centered'>
      <a href='#about'>About</a>
      <a href='#features'>Features</a>
      <a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI' target='_blank'>GitHub</a>
      <a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI#docs' target='_blank'>Docs</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Landing Page Project Details ---
st.markdown("""
<a id='about'></a>
<div class='bartoz-desc'>
  <b>BARTOZ-AI</b> is an open-source, modern research assistant for AI/ML/LLM topics.<br>
  <span style='color:#6366f1;font-weight:500;'>Ask questions about AI agents, companies, or breakthroughs and get concise, sourced answers.</span><br><br>
  <span style='font-size:1.07rem;'>
    <b>✨ Features:</b> Fast RAG pipeline · Multi-model (Gemini, DeepSeek) · Source citations · Modern UI · 100% Open Source
  </span>
</div>
""", unsafe_allow_html=True)

# --- Features Section ---
st.markdown("""
<a id='features'></a>
<div class='features-section'>
  <div class='features-title'>Key Features</div>
  <ul class='features-list'>
    <li>🔍 <b>Semantic Search</b> over curated AI/ML/LLM docs & news</li>
    <li>⚡ <b>Instant Answers</b> from Gemini & DeepSeek models</li>
    <li>📚 <b>Source Citations</b> for every answer</li>
    <li>🧩 <b>Modular RAG Pipeline</b> (LangChain powered)</li>
    <li>🌐 <b>Open Source</b> & extensible for your own research</li>
  </ul>
</div>
""", unsafe_allow_html=True)

# --- Docs Section ---
st.markdown("""
<a id='docs'></a>
<div class='docs-section'>
  <div class='docs-title'>Documentation</div>
  <div class='docs-body'>
    <ul class='docs-list'>
      <li><a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI#installation' target='_blank'>Installation Guide</a></li>
      <li><a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI#usage' target='_blank'>Usage & Examples</a></li>
      <li><a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI#contributing' target='_blank'>Contributing</a></li>
      <li><a href='mailto:chiragskotian@gmail.com'>Contact Maintainer</a></li>
    </ul>
  </div>
</div>
""", unsafe_allow_html=True)


# --- Main Query Form ---
# --- Sample Queries as Pill Buttons (OUTSIDE FORM) ---
import streamlit as st
sample_queries = [
    "What is Gemini?",
    "Top AI companies 2024",
    "How does DeepSeek work?",
    "Best open source LLMs"
]
cols = st.columns(len(sample_queries))
for i, q in enumerate(sample_queries):
    if cols[i].button(q, key=f"sample_{i}"):
        st.session_state["query_input"] = q
        # No rerun needed; Streamlit will update the input box on next interaction.

with st.form("query_form", clear_on_submit=False):
    st.markdown("""
    <div class='query-form-center'>
      <div class='query-form-label'><span class='input-icon'>🤖</span> Ask a question about <b>AI, agents, or companies</b>:</div>
      <div class='query-form-input'>
        <div id='input-float-wrap' class='textarea-float-wrap'>
          <span class='textarea-floating-label' id='input-float-label'>Type your question here...</span>
        </div>
    """, unsafe_allow_html=True)
    query = st.text_area("", value=st.session_state.get("query_input", ""), height=90, key="query_input")
    st.markdown("""
      </div>
      </div>
      <div class='sample-queries-row' style='margin-bottom:0.5em;'>
      </div>
      <div style='height:0.7em;'></div>
      <div class='query-form-select'>
        <div class='model-select-label' style='text-align:center;'>Choose the model:</div>
    """, unsafe_allow_html=True)
    model_option = st.selectbox(
        "",
        ["Gemini (Google AI Studio)", "DeepSeek (OpenRouter)"],
        help="Gemini is from Google AI Studio. DeepSeek is via OpenRouter."
    )
    st.markdown("""
      </div>
      <div style='height:0.7em;'></div>
      <div class='query-form-btn'>
    """, unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Ask")
    st.markdown("""
      </div>
    </div>
    """, unsafe_allow_html=True)

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
                    f"{BACKEND_URL}/query",
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
                st.markdown(f"""
                <div class='card'>
                  <div style='font-size:1.18rem;font-weight:700;color:#6366f1;margin-bottom:0.3em;'>🧠 AI Research Answer</div>
                  <div style='font-size:1.13rem;line-height:1.7;'>{main_answer}</div>
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
                    st.info("No relevant documents or supporting context were found for your query.")
            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to the backend API. Please ensure it is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error during API request: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- Unique Footer ---
st.markdown("""
<hr style='margin-top:2.5em;margin-bottom:1.7em;'>
<div class='bartoz-footer'>
  <div style='font-size:1.13rem; font-weight:700; margin-bottom:0.4em;'>BARTOZ-AI: Open Source AI/ML/LLM Research Assistant</div>
  <div style='font-size:1.01rem; margin-bottom:0.6em;'>Empowering researchers, students, and enthusiasts to explore the world of artificial intelligence with transparency and speed.</div>
  <div class='bartoz-footer-links'>
    <a href='#about'>About</a> |
    <a href='#features'>Features</a> |
    <a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI' target='_blank'>GitHub</a> |
    <a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI#docs' target='_blank'>Docs</a> |
    <a href='mailto:kotianchinnu99@gmail.com'>Contact</a>
  </div>
  <div class='bartoz-footer-badges'>
    <img src='https://img.shields.io/github/stars/Chirag-S-Kotian/BARTOZ-AI?style=social' alt='GitHub stars' style='vertical-align:middle; margin-right:0.7em;'/>
    <img src='https://img.shields.io/badge/License-MIT-blue.svg' alt='MIT License' style='vertical-align:middle; margin-right:0.7em;'/>
    <img src='https://img.shields.io/badge/PRs-Welcome-brightgreen.svg' alt='PRs Welcome' style='vertical-align:middle;'/>
  </div>
  <div style='margin-top:0.9em; font-size:0.99rem; color:#7dd3fc;'>Built with ❤️ by <a href='https://github.com/Chirag-S-Kotian' target='_blank' style='color:#38bdf8;'>Chirag S Kotian</a> · Powered by LangChain, Gemini, DeepSeek, and Streamlit</div>
</div>
""", unsafe_allow_html=True)