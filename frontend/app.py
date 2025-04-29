import streamlit as st
import requests
import re

st.set_page_config(page_title="AI Research Assistant", page_icon="", layout="wide")

# --- Minimal Modern CSS ---

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
""", unsafe_allow_html=True)

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

# --- Footer ---
st.markdown("""
<hr>
<div style='text-align:center;font-size:1rem;color:#444;margin-top:2em;'>
  Made with ❤️ by <a href='https://github.com/Chirag-S-Kotian' target='_blank'>Chirag S Kotian</a> | <a href='https://github.com/Chirag-S-Kotian/BARTOZ-AI' target='_blank'>BARTOZ-AI Repo</a><br>
  <span style='font-size:0.95rem;'>Open Source · Powered by LangChain, Gemini, DeepSeek, and Streamlit</span>
</div>
""", unsafe_allow_html=True)