# 🩺 Medical Report AI Assistant (RAG + Analytics Dashboard)

An intelligent **AI-powered medical report analysis system** built using **Streamlit, LangChain, FAISS, Groq LLM, and HuggingFace embeddings**, extended with a **Business Intelligence layer using Microsoft Power BI**.

This application allows users to upload medical PDFs, ask natural language questions, and analyze user interactions through a data-driven dashboard.

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
- 📈 Power BI dashboard for analytics & insights  
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
9. Conversation data is exported and analyzed in Power BI  

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
- Microsoft Power BI  

---

## 📁 Project Structure

- app.py → Main Streamlit application  
- faiss_index/ → Vector database storage  
- req.txt → Required Python dependencies  

---

## 💡 Use Cases

- 📊 Analyze blood test reports  
- 🧪 Extract medical values (BP, sugar, hemoglobin, etc.)  
- 🧾 Understand diagnostic reports  
- 🧠 Get explanations of medical terms  
- 📚 Summarize long medical documents  

---

## 📊 Analytics Dashboard (Power BI)

This project extends beyond a chatbot by introducing a **data analytics layer**.

Conversation history is exported as CSV and visualized using Power BI to generate insights.

### 📈 Dashboard Highlights

- Domain Distribution (Cardiology, Neurology, Endocrinology, etc.)  
- Frequently Asked Questions  
- User Segmentation (Patients, Students, General Users)  
- Query Trends Over Time  

---

## 📈 Analytics Use Cases

### 1. 🔥 Frequently Asked Questions
- Identify most repeated medical queries  
- Improve chatbot responses based on real usage  

### 2. 🧠 Medical Domain Insights
- Understand which medical domains are most queried  
- Helps prioritize healthcare AI improvements  

### 3. 👥 User Behavior Analysis
- Analyze how users interact with the chatbot  
- Understand query patterns and complexity  

### 4. 📊 Health Trend Detection
- Detect commonly asked symptoms  
- Identify emerging health concerns  

### 5. 🧾 Prompt Optimization
- Improve LLM responses using real user data  
- Reduce hallucination risks  
- Enhance answer accuracy  

### 6. 🎯 Audience Identification
- Segment users into Patients, Students, General Users  
- Helps build targeted AI healthcare solutions  

---

## 🚀 Production-Level Vision

- Store conversation logs in a database  
- Connect Power BI to live data  
- Enable real-time dashboard updates  
- Add AI-generated insights from user behavior  

---

## 💡 Key Differentiator

This project combines:

- AI (RAG + LLM)  
- Data Analytics  
- Business Intelligence  

Creating an **insight-driven AI system**, not just a chatbot.

---

## 🖼️ Dashboard Preview

<img width="1147" height="646" alt="image" src="https://github.com/user-attachments/assets/05620172-ed01-43ea-bf5d-7e20441efb4a" />


---

## 📦 Installation

```bash
git clone https://github.com/akill005/Medical_Report_AI_Assistant_RAG.git
cd Medical_Report_AI_Assistant_RAG
pip install -r req.txt
streamlit run app.py


## 🔑 Setup
- Get your Groq API key from: https://console.groq.com/keys/
- Enter it in the sidebar


##⭐ If you like this project
Give it a star ⭐ and share your feedback!
