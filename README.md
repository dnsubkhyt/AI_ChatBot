# AI Chatbot with DuckDuckGo Search and Ollama Integration

## Overview
This project implements a simple AI chatbot that retrieves relevant information by searching DuckDuckGo, scraping the top 3 URLs, and storing the results in a Chroma database. The chatbot then generates a response using the context provided by the retrieved web content and the Ollama LLM model (Llama3.2). The goal of this chatbot is to answer queries based on real-time, up-to-date news or information from the web.

### Key Features:
- **DuckDuckGo Search**: The chatbot starts by performing a search on DuckDuckGo to retrieve the top 3 relevant URLs based on the user's query.
- **Web Scraping**: The chatbot scrapes the textual content (paragraphs) from each of the top 3 URLs.
- **ChromaDB Integration**: Scraped web content is stored in ChromaDB, an embedded vector database, for efficient retrieval.
- **Ollama (Llama3.2)**: The chatbot uses the Llama3.2 model via Ollama to generate natural language responses based on the retrieved context.
- **Streamlit Interface**: The user can interact with the chatbot via a simple web interface using Streamlit.

## Prerequisites
To run this project, you'll need:
- Python 3.8 or higher
- Installed dependencies (listed below)
- Ollama (Llama3.2) model running locally

### Required Python Libraries:
- `requests`
- `beautifulsoup4`
- `chromadb`
- `langchain_ollama`
- `ollama`
- `duckduckgo_search`
- `streamlit`

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
