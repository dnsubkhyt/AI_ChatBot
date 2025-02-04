# AI_ChatBot
AI Chatbot with DuckDuckGo Search and Ollama Integration
Overview
This project implements a simple AI chatbot that retrieves relevant information by searching DuckDuckGo, scraping the top 3 URLs, and storing the results in a Chroma database. The chatbot then generates a response using the context provided by the retrieved web content and the Ollama LLM model (Llama3.2). The goal of this chatbot is to answer queries based on real-time, up-to-date news or information from the web.

Key Features:
DuckDuckGo Search: The chatbot starts by performing a search on DuckDuckGo to retrieve the top 3 relevant URLs based on the user's query.
Web Scraping: The chatbot scrapes the textual content (paragraphs) from each of the top 3 URLs.
ChromaDB Integration: Scraped web content is stored in ChromaDB, an embedded vector database, for efficient retrieval.
Ollama (Llama3.2): The chatbot uses the Llama3.2 model via Ollama to generate natural language responses based on the retrieved context.
Streamlit Interface: The user can interact with the chatbot via a simple web interface using Streamlit.
Prerequisites
To run this project, you'll need:

Python 3.8 or higher
Installed dependencies (listed below)
Ollama (Llama3.2) model running locally
Required Python Libraries:
requests
beautifulsoup4
chromadb
langchain_ollama
ollama
duckduckgo_search
streamlit
Installation
Clone the repository:
bash
Copy
git clone <repository_url>
cd <repository_directory>
Install the required dependencies:
bash
Copy
pip install -r requirements.txt
Ensure you have the Ollama model (Llama3.2) running locally. Instructions for setting up Ollama can be found on Ollama's official documentation.

You may also need to install the chromadb and duckduckgo_search packages if they are not included in the requirements.txt file.

bash
Copy
pip install chromadb duckduckgo-search
Configuration
Model and Database Configuration:
The following configurations can be adjusted based on your preferences:

LLM_MODEL: Set this to "llama3.2" to use the Llama3.2 model.
CHROMA_DB_PATH: This is the local path where ChromaDB will store the documents. By default, it's stored in the current working directory under the chroma_db folder.
COLLECTION_NAME: The name of the ChromaDB collection (default is "news_articles_collection").
Ensure that Ollama is running and accessible at http://localhost:11434. If it's running on a different port, modify the base URL in the configuration.

Running the Application
To run the chatbot, execute the following:

bash
Copy
streamlit run app.py
This will start a local Streamlit web app. You can now interact with the chatbot via a simple text box interface.

Workflow:
Search and Scraping: Upon submitting a query, the chatbot searches DuckDuckGo and scrapes content from the top 3 relevant URLs.
ChromaDB Storage: The scraped content is stored in ChromaDB, along with the URLs from which they were sourced.
Response Generation: A prompt is generated using the scraped context and the query. This is sent to the Ollama model (Llama3.2) to generate a response.
Result Display: The response from the model is displayed to the user, and the raw prompt used to generate the response can be expanded for review.
How It Works (In Detail)
DuckDuckGo Search:

The chatbot uses the duckduckgo_search.DDGS library to search for the user's query and retrieve the top 3 URLs.
Scraping the Content:

The chatbot fetches the content of these URLs using the requests library and extracts the textual content (paragraphs) using BeautifulSoup.
The content is truncated to the first 500 words for efficiency.
Saving to ChromaDB:

The chatbot stores the scraped content in ChromaDB, associating each document with its source URL. The documents are embedded using Ollama's Llama3.2 model for semantic search.
Generating a Response:

The chatbot forms a prompt for Ollama by including the scraped content and the original query. This is sent to Ollama (Llama3.2) for natural language processing.
The model's response is then displayed in the Streamlit interface.
Code Breakdown
ddg_search: This function performs a DuckDuckGo search using the user's query and returns the top 3 URLs.

get_page: This function scrapes a webpage, extracting all the text inside <p> tags.

truncate: This helper function ensures that the text does not exceed 500 words, keeping the response manageable.

save_to_chromadb: This function saves the scraped and embedded documents to ChromaDB, associating each document with its source URL.

create_prompt_ollama: This function creates the prompt that is passed to Ollama for processing, combining the user's question and the context from the scraped content.

create_completion_ollama: This function sends the prompt to Ollama and receives the generated response.

Streamlit Form: The interface allows users to input their queries and see the results, including the list of URLs used for generating the response.

Troubleshooting
Error with ChromaDB: Ensure that ChromaDB is properly initialized and the database path is accessible.
Ollama Connection: Make sure the Ollama server is running locally at http://localhost:11434 (or the configured URL).
Scraping Issues: Some websites may block automated scraping. If this happens, consider adding error handling for such cases or using another data source.
