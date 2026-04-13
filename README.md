# 🩺 Medical Report AI Assistant (RAG-Based Chatbot)

An intelligent **AI-powered medical report analysis system** built using **Streamlit, LangChain, FAISS, Groq LLM, and HuggingFace embeddings**.  
This application allows users to upload medical PDFs and ask natural language questions to extract and understand medical insights safely and accurately.

---

## 🚀 Features

- 📄 Upload single or multiple medical PDF reports
- 🤖 Ask questions in natural language (chat interface)
- 🧠 Retrieval-Augmented Generation (RAG) pipeline
- 🔍 Semantic search using FAISS vector database
- ⚡ Fast inference using Groq (LLaMA 3 model)
- 🤗 HuggingFace embeddings for text representation
- 💬 Chat-style UI for better user experience
- 📊 Download full conversation history as CSV
- 🔒 Safe AI responses (no hallucinations, no prescriptions)

---

## 🧠 How It Works

1. Upload medical PDF files
2. Extract text using PyPDF2
3. Split text into chunks using LangChain text splitter
4. Convert text into embeddings using HuggingFace model
5. Store embeddings in FAISS vector database
6. User asks a question
7. Relevant chunks are retrieved using semantic search
8. Groq LLM generates a safe, context-based response

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🎈
- LangChain 🦜
- FAISS (Vector Database)
- HuggingFace Sentence Transformers 🤗
- Groq API (LLaMA 3)
- PyPDF2
- Pandas

---

## 📁 Project Structure

- app.py # Main Streamlit application
- faiss_index/ # Vector database storage
- req.txt # Required Python dependencies


---


## 💡 Use Cases
📊 Analyze blood test reports
🧪 Extract medical values (BP, sugar, hemoglobin, etc.)
🧾 Understand diagnostic reports
🧠 Get explanations of medical terms
📚 Summarize long medical documents



## 📈 Analytics Use Cases (VERY IMPORTANT)

After downloading conversation history CSV, we can analyze:

### 1. 🔥 Frequently Asked Questions
- Identify most repeated medical questions
- Improve prompt engineering based on real demand

### 2. 🧠 Medical Domain Insights
- Categorize queries into:
  - Cardiology ❤️
  - Neurology 🧠
  - Endocrinology 🍬
  - Gastroenterology 🫃
- Understand which medical field users care about most

### 3. 👥 User Behavior Analysis
- How users interact with AI:
  - Short vs detailed questions
  - Follow-up question patterns
  - Report-based vs general health queries

### 4. 📊 Health Trend Detection
- Common symptoms asked (fever, sugar, BP, etc.)
- Emerging health concerns across users

### 5. 🧾 Prompt Optimization
- Improve system prompt based on:
  - Missing answers
  - Frequent confusion areas
  - Hallucination risk reduction

### 6. 🎯 Audience Identification
- Identify whether users are:
  - Patients
  - Students (MBBS / nursing)
  - General public
- Helps in building targeted healthcare AI products

---


