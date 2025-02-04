import requests
from bs4 import BeautifulSoup
import chromadb
from langchain_ollama import OllamaEmbeddings
import os
import ollama
import re
from duckduckgo_search import DDGS

LLM_MODEL = "llama3.2"
CHROMA_DB_PATH = os.path.join(os.getcwd(), "chroma_db")
COLLECTION_NAME = "news_articles_collection"

import streamlit as st
st.set_page_config(page_title="AI Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>AI Chatbot</h1>", unsafe_allow_html=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

embedding_function = OllamaEmbeddings(
    model=LLM_MODEL, 
    base_url="http://localhost:11434" 
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"description": "A collection for news articles"},
    embedding_function=embedding_function
)

# DuckDuckGo Search to get the top 3 URLs
def ddg_search(query):
    results = DDGS().text(query, max_results=3)  
    urls = [result['href'] for result in results]
    return urls  # Return the 1st 3 URLs

def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.find_all("p")  # Extract all paragraphs
    return [p.get_text() for p in paragraphs]

def truncate(text):
    words = text.split()
    return " ".join(words[:500])  


def save_to_chromadb(search_results, source_urls):
    if len(search_results) != len(source_urls):
        print(f"Warning: Mismatch in the number of search results and source URLs. Skipping invalid data.")
        return
    
    embeddings = embedding_function.embed_documents(search_results)  
    
    for i, content in enumerate(search_results):
        if content: 
            collection.add(
                ids=[f"doc_{i}"],  
                documents=[content],  
                embeddings=[embeddings[i]], 
                metadatas=[{"source": source_urls[i]}]  
            )
    print("✅ Data stored in ChromaDB successfully!")


# Create a prompt for Ollama (Llama3.2)
def create_prompt_ollama(llm_query, search_results):
    content = (
        "Answer the question using only the context below.\n\n"
        "Context:\n" +
        "\n\n---\n\n".join(search_results) +
        f"\n\nQuestion: {llm_query}\nAnswer:"
    )
    return [{'role': 'user', 'content': content}]


def create_completion_ollama(prompt):
    completion = ollama.chat(model=LLM_MODEL, messages=prompt)
    return completion['message']['content']


with st.form("prompt_form"):
    query = st.text_area("Ask a question:", None)
    submitted = st.form_submit_button("Send")

    if submitted:
        # Step 1: Search DuckDuckGo for the query and get the top 3 URLs
        print(f"Searching DuckDuckGo for query: {query}")
        top_urls = ddg_search(query)  
        print(f"Top URLs: {top_urls}")

        # Step 2: Scrape the content of each of the 3 URLs
        docs = []
        for url in top_urls:
            print(f"Scraping the content of: {url}")
            page_content = get_page(url)
            docs.append([truncate(re.sub("\n\n+", "\n", doc)) for doc in page_content])

        # Flatten the list of documents (if any content exists in multiple chunks)
        flattened_docs = [item for sublist in docs for item in sublist]

        # Step 3: Print out the URLs that will be used for the final response
        st.write("The following URLs were retrieved and will be used for generating the response:")
        for url in top_urls:
            st.write(url)

        # Step 4: Save to ChromaDB
        save_to_chromadb(flattened_docs, top_urls)


        # Step 5: Generate prompt and get response from Ollama
        prompt = create_prompt_ollama(query, flattened_docs)
        result = create_completion_ollama(prompt)
        
        # Step 6: Display result
        e = st.expander("Generated LLM Prompt:")
        e.write(prompt)
        st.write(result)
