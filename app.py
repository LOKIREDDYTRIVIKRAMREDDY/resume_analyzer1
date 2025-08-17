import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.analyzer import analyze_resume
from utils.groq_client import groq_feedback

st.set_page_config(page_title="Resume Keyword Optimizer", layout="wide")

st.title("📄 Resume Keyword Optimizer")

jd_text = st.text_area("Paste Job Description here:", height=200)

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file and jd_text:
    with st.spinner("Analyzing Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        analysis = analyze_resume(resume_text, jd_text)
        feedback = groq_feedback(resume_text, jd_text)

    st.subheader("📊 Resume Match Score")
    st.metric("Score", f"{analysis['score']}%")

    st.subheader("✅ Matched Skills")
    st.write(", ".join(list(analysis["matched_skills"])) or "None")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(list(analysis["missing_skills"])) or "None")

    st.subheader("🤖 AI Suggestions (Groq)")
    st.write(feedback)
