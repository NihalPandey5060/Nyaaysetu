import streamlit as st
from docx import Document
import io
from openai import OpenAI

# Set page title
st.set_page_config(page_title="Nyaaysetu", layout="wide")

st.title("Nyaaysetu")

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    # Publicly set OpenAI API key
    api_key = "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"
    return OpenAI(api_key=api_key)

client = get_openai_client()

# Input method selection
input_method = st.radio("Choose input method:", ("Upload File", "Paste Text"))

document_content = ""

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload a .txt or .docx file", type=["txt", "docx"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            document_content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(uploaded_file.read()))
            for para in doc.paragraphs:
                document_content += para.text + "\n"
        st.success("File uploaded successfully!")
elif input_method == "Paste Text":
    document_content = st.text_area("Paste your legal document text here:", height=300)

if st.button("Simplify Document"):
    if document_content:
        with st.spinner("Simplifying document and identifying risky terms..."):
            try:
                prompt = f"""Summarize and simplify the following legal document. Clearly identify any risky or concerning legal terms and explain them in plain English. Format the output into two distinct sections: 'Simplified Document:' and 'Risky Terms Explained:'.

Document:
{document_content}
"""
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful legal assistant that simplifies legal documents."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                full_response_content = response.choices[0].message.content
                
                # Split the response into two sections
                if "Risky Terms Explained:" in full_response_content:
                    simplified_text, risky_terms_explanation = full_response_content.split("Risky Terms Explained:", 1)
                else:
                    simplified_text = full_response_content
                    risky_terms_explanation = "No risky terms explicitly identified or separated."

                st.subheader("Simplified Document")
                st.write(simplified_text.replace("Simplified Document:", "").strip())

                st.subheader("Risky Terms Explained")
                st.write(risky_terms_explanation.strip())

            except Exception as e:
                st.error(f"An error occurred during API call: {e}")
    else:
        st.error("Please upload a file or paste some text to simplify.")

import os
os.system('C:/Users/Nihal31/OneDrive - Amrita Vishwa Vidyapeetham/Documents/Nyaaysetu/venv/Scripts/python.exe app.py')