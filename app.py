from datetime import datetime

import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import base64
import os

from langchain_groq import ChatGroq
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate



import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())






# get text from pdf using PdfReader

def get_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

# get chunks from text
def get_chunks(text,model_name):
    if(model_name=="Groq"):
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=20)
    chunks=text_splitter.split_text(text)
    return chunks

# storing chunks in vector db
# def get_vector(text_chunks,model_name,api_key=None):
#     if (model_name=="Google AI"):
#         embeddings=GoogleGenerativeAIEmbeddings(model="model/embedding-001",google_api_key=api_key)
#     vector_store=FAISS.from_texts(text_chunks,embedding=embeddings)
#     vector_store.save_local("faiss_index")
#     return vector_store

def get_vector(text_chunks, model_name, api_key=None):
    if model_name == "Groq":
        # Replace Gemini with HuggingFace all-MiniLM
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store




# create conversational chain using langchain
def get_conversational_chain(model_name,vector_store=None,api_key=None):
    if model_name=="Groq":
        prompt_template="""
            You are an AI medical report assistant.

            Your role is to analyze uploaded medical reports and answer user questions safely and accurately.

            ------------------------
            RESPONSE RULES
            ------------------------

            1. FACTUAL EXTRACTION (STRICT)
            - If the question asks for values (e.g., BP, hemoglobin, sugar, TSH, findings, test results):
            → Extract ONLY from the provided context.
            → Return the exact value clearly.
            → Do NOT guess or infer missing values.

            2. MISSING INFORMATION
            - If the requested information is NOT present in the report:
            → Reply exactly:
            "Answer is not available in the context"

            3. INTERPRETATION (ALLOWED BUT SAFE)
            - If the user asks:
            "what does this mean", "is this normal", "what is my condition"
            → You may explain based on the report values.
            → Keep it general and educational.
            → Do NOT give a medical diagnosis.
            → Use phrases like:
                "This may indicate..." or "This could be associated with..."

            4. HEALTH ADVICE (GENERIC ONLY)
            - If the user asks:
            "how to improve", "what should I do", "precautions", "how to reduce"
            → Provide general health guidance.
            → No medicines, no dosage, no prescriptions.
            → No strict instructions.

            5. NO HALLUCINATION
            - Never create values, diseases, or results not present in the report.

            6. RESPONSE STYLE
            - Be clear and concise.
            - No reasoning steps.
            - No internal thoughts.
            - No phrases like "let me think", "analysis", etc.

            ------------------------
            INPUT
            ------------------------
            Context:
            {context}

            Question:
            {question}

            ------------------------
            FINAL ANSWER:
        """
        # model=ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.3,google_api_key=api_key)
        model = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )
        prompt=PromptTemplate(template=prompt_template,input_variables=["context","question"])
        chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)
        return chain



def process_pdfs(pdf_docs, model_name, api_key):
    text = get_text(pdf_docs)
    text_chunks = get_chunks(text, model_name)
    vector_store = get_vector(text_chunks, model_name, api_key)
    return vector_store



# take user inout
def user_input(user_question,model_name,api_key,pdf_docs):
    if api_key is None or st.session_state.vector_store is None or pdf_docs is None:
        st.warning("Please upload and process PDF first")
        return
    # text_chunks=get_chunks(get_text(pdf_docs),model_name)
    # vector_store=get_vector(text_chunks,model_name,api_key)
    user_question_output=""
    response_output=""
    if model_name=="Groq":
        # embeddings=GoogleGenerativeAIEmbeddings(model="model/embedding-001",google_api_key=api_key)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # new_db=FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)
        new_db = st.session_state.vector_store
        # docs=new_db.similarity_search(user_question)
        docs = new_db.max_marginal_relevance_search(user_question, k=10, fetch_k=20)
        chain=get_conversational_chain("Groq",vector_store=new_db,api_key=api_key)
        response=chain({"input_documents":docs,"question":user_question},return_only_outputs=True)
        user_question_output=user_question
        response_output=response['output_text']
        pdf_names=[pdf.name for pdf in pdf_docs] if pdf_docs else []
        st.session_state.conversation_history.append((user_question_output,response_output,model_name,datetime.now().strftime
        ('%Y-%m-%d %H:%M:%S')," , ".join(pdf_names)))


    for question, answer, model_name, timestamp, pdf_name in reversed(st.session_state.conversation_history):
        st.markdown(
            f"""
            <div class="chat-message user">
                <div class="avatar">
                    <img src="https://i.ibb.co/CKpTnWr/user-icon-2048x2048-ihoxz4vq.png">
                </div>    
                <div class="message">{question}</div>
            </div>
            <div class="chat-message bot">
                <div class="avatar">
                    <img src="https://i.ibb.co/wNmYHsx/langchain-logo.webp" >
                </div>
                <div class="message">{answer}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    if len(st.session_state.conversation_history) > 0:
        df = pd.DataFrame(st.session_state.conversation_history, columns=["Question", "Answer", "Model", "Timestamp", "PDF Name"])

        # df = pd.DataFrame(st.session_state.conversation_history, columns=["Question", "Answer", "Timestamp", "PDF Name"])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64
        href = f'<a href="data:file/csv;base64,{b64}" download="conversation_history.csv"><button>Download conversation history as CSV file</button></a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.markdown("To download the conversation, click the Download button on the left side at the bottom of the conversation.")
    # st.snow()
def main():
    st.set_page_config(page_title="Medical Report AI Assistant", page_icon="🩺")
    st.header("Medical Report AI Assistant:")
    st.markdown("""
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 20%;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    linkedin_profile_link = "https://www.linkedin.com/in/akila-arulselvam-5a0ab826a/"
    # linkedin_profile_link = "https://www.linkedin.com/in/akila-arulselvam-5a0ab826a/"
    github_profile_link = "https://github.com/akill005"

    st.sidebar.markdown(
        f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({linkedin_profile_link}) "
        f"[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]({github_profile_link})"
    )



    model_name = st.sidebar.radio("Select the Model:", ( "Groq"))

    api_key = None

    if model_name == "Groq":
        api_key = st.sidebar.text_input("Enter your Groq API Key:")
        st.sidebar.markdown("Click [here](https://console.groq.com/keys/) to get a Groq API key.")
        
        if not api_key:
            st.sidebar.warning("Please enter your Groq API Key to proceed.")
            return


    #     reset_button = col2.button("Reset")
    #     # clear_button = col1.button("Rerun")

    #     if reset_button:
    #         st.session_state.conversation_history = []  # Clear conversation history
    #         st.session_state.user_question = ""  # Clear user question input 
    #         st.session_state.vector_store = None 
            
            
            api_key = None  # Reset Google API key
            pdf_docs = None  # Reset PDF document
            
    #     # else:
    #     #     if clear_button:
    #     #         if 'user_question' in st.session_state:
    #     #             st.warning("The previous query will be discarded.")
    #     #             st.session_state.user_question = "" 
    #     #             if len(st.session_state.conversation_history) > 0:
    #     #                 st.session_state.conversation_history = st.session_state.conversation_history[:-1]  # Son sorguyu kaldır
    #     #         else:
    #     #             st.warning("The question in the input will be queried again.")




    #     pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
    #     if st.button("Submit & Process"):
    #         if pdf_docs:
    #             with st.spinner("Processing..."):
    #                 st.session_state.vector_store = process_pdfs(pdf_docs, model_name, api_key)
    #                 st.success("Done")
    #         else:
    #             st.warning("Please upload PDF files before processing.")
    with st.sidebar:
        st.title("Menu:")

        st.session_state.pdf_docs = st.file_uploader(
            "Upload your PDF Files",
            accept_multiple_files=True,
            key=f"pdf_docs_{st.session_state.get('uploader_key', 0)}"
        )

        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            submit_button = st.button("Submit", use_container_width=True)

        with col3:
            reset_button = st.button("Reset",use_container_width=True)

        if submit_button:
            if st.session_state.pdf_docs:
                with st.spinner("Processing..."):
                    st.session_state.vector_store = process_pdfs(st.session_state.pdf_docs, model_name, api_key)
                    st.success("Done")
            else:
                st.warning("Please upload PDF files before processing.")
        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 0
        if reset_button:
            st.session_state.conversation_history = []
            st.session_state.user_question = ""
            st.session_state.vector_store = None
            st.session_state.uploader_key += 1 
            st.rerun()
            
    user_question = st.text_input("Ask a Question from the PDF Files",key="user_question")

    if user_question:
        user_input(user_question, model_name, api_key, st.session_state.pdf_docs)
        # st.session_state.user_question = ""  # Clear user question input 

if __name__ == "__main__":
    main()


