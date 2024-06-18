# RAG_chatbot_demo
Simple chatbot using Retrieval-Augmented Generation aka RAG.

The chatbot uses OpenAI API and is based on Langchain. Can use either Pinecone or Chroma vector database.

## Running code
1. Create a python virtual environment and install the requirements in `requirements.txt`
2. Create `.env` file in the local directory and add
   ```
   OPENAI_API_KEY="your key"
   PINECONE_API_KEY="your key"
   MISTRAL_API_KEY="your key"
   ```
3. Adding to vector database - The private data shold be saved as markdown files and stored at `../Data_intranet/`
4. If Using Chroma DB:
    ```
    >> python populate_vectorDB_Chroma
    ```

5. If Using Pinecone DB
    ```
    >> python populate_vectorDB_pinecone
    ```

7. Running the app - The app is done in Streamlit and you can run with following command. If using 
    ```
    >> streamlit run demo.py --server.fileWatcherType none --server.port 8080
    ```

