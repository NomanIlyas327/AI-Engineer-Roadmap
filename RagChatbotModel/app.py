import os
import streamlit as st
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq

# --- Streamlit Page Setup ---
st.set_page_config(page_title="RAG Knowledge Bot", page_icon="🤖")
st.title("🤖 RAG Knowledge Chatbot")

# Paths Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# --- Step 1, 2 & 3: Initialization & Vector DB Setup ---
@st.cache_resource
def setup_vector_db():
    documents = []
    if os.path.exists(DATA_DIR):
        for file_name in os.listdir(DATA_DIR):
            if file_name.endswith(".txt"):
                file_path = os.path.join(DATA_DIR, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    documents.append({"text": f.read(), "source": file_name})

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks, all_metadatas, all_ids = [], [], []
    chunk_count = 0

    for doc in documents:
        chunks = text_splitter.split_text(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadatas.append({"source": doc["source"]})
            all_ids.append(f"doc_{chunk_count}")
            chunk_count += 1

    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    collection = chroma_client.get_or_create_collection(name="rag_docs")

    # upsert se purana data update ho jayega aur nayi files bhi index ho jayengi
    if all_chunks:
        collection.upsert(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )

    return collection

collection = setup_vector_db()

# --- Groq Setup ---
GROQ_API_KEY = ""  # Apni Groq API Key yahan paste karein
groq_client = Groq(api_key=GROQ_API_KEY)

# --- Chat History Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Previous Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Step 4 & 5: Interactive Search & LLM Generation ---
if user_query := st.chat_input("Apna sawal yahan poochein..."):
    
    # User Message Display
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 1. Retrieval (ChromaDB Vector Search - Top 4 chunks)
    results = collection.query(query_texts=[user_query], n_results=4)
    retrieved_chunks = results['documents'][0] if results['documents'] else []
    context = "\n\n".join(retrieved_chunks)

    # 2. Prompt Framing
    system_prompt = f"""
    Aap ek helpful AI assistant hain. 
    Neche diye gaye Context ka istemal karte hue user ke sawal ka jawab dein. 
    Agar jawab Context mein mojood nahi hai, toh saaf keh dein ke "Mujhe is baare mein jankari nahi hai."

    Context:
    {context}
    """

    # 3. LLM Response Generation
    with st.chat_message("assistant"):
        with st.spinner("Jawab tayyar ho raha hai..."):
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                model="openai/gpt-oss-120b"
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})