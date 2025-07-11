# text_summarizer.py

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import streamlit as st
from transformers import pipeline

# Load NLTK tokenizer (first-time users)
import nltk
import os

# Ensure 'punkt' is available and downloaded to a known path
nltk_data_path = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path)



def summarize_with_sumy(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)


def summarize_with_transformers(text):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']


# --- Streamlit UI ---
st.set_page_config(page_title="📝 Text Summarizer")

st.title("📝 Text Summarization Tool")
st.markdown("Summarize long articles using NLP techniques")

input_text = st.text_area("Paste your text below:", height=300)

summarizer_type = st.selectbox("Choose summarization method", ["Sumy (Extractive)", "Transformers (Abstractive)"])

if st.button("Summarize"):
    if input_text.strip() == "":
        st.warning("Please paste some text.")
    else:
        with st.spinner("Generating summary..."):
            if summarizer_type == "Sumy (Extractive)":
                summary = summarize_with_sumy(input_text, num_sentences=3)
            else:
                summary = summarize_with_transformers(input_text)

        st.subheader("📌 Summary:")
        st.success(summary)


# /Applications/Python\ 3.12/Install\ Certificates.command
# python -c "import nltk; nltk.download('punkt')"