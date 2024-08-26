# RAG Chatbot
A simple chatbot using Retrieval-Augmented Generation (RAG).

The chatbot is designed to act as a university administrative officer, assisting with questions related to Higher Degree by Research (HDR) matters.

The chatbot uses the OpenAI API (later changed to Azure openAI) and is based on Langchain. It can use either Pinecone or Chroma as the vector database.

## Running code
1. Create a Python virtual environment and install the requirements:
    ```
    >> python3 -m venv chatbot
    >> pip install -r requirements.txt
    ```
2. Create a `.env` file in the local directory and add your API keys:
   ```
   OPENAI_API_KEY="your key"
   PINECONE_API_KEY="your key"
   MISTRAL_API_KEY="your key"
   ```
3. Add data to the vector database:
   - Save private data as markdown files and store them in `../Data_intranet/`
4. If using Chroma DB:
    ```
    >> python populate_vectorDB_Chroma
    ```

5. If Using Pinecone DB
    ```
    >> python populate_vectorDB_pinecone
    ```

6. Run the app: 
   - TThe app is built with Streamlit. Use the following command to run it: 
    ```
    >> streamlit run demo.py --server.fileWatcherType none --server.port 8080
    ```

