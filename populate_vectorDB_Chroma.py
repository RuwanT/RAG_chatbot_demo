from dotenv import load_dotenv, find_dotenv
import glob
import difflib
from pathlib import Path
import os
import shutil

from langchain_text_splitters import MarkdownHeaderTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
import os
# from langchain_pinecone import PineconeVectorStore
# from langchain_community.vectorstores import Pinecone
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings

DATA_PATH = "../Data_intranet/"

USE_OPENAI = True

if USE_OPENAI:
    PROCESSED_FILE = "processed_files_chroma_openAI-large.txt"
else:
    PROCESSED_FILE = "processed_files_chroma_mistral.txt"

def getTextFiles2Add():
    firstTime = True
    print("Get files not added to vector database...")
    f = open(DATA_PATH + "current_files.txt", "w")
    for file in glob.glob(DATA_PATH + '**/*.md', recursive=True):
        f.writelines(file + '\n')
    f.close()
    
    files2process = []
    if not Path(DATA_PATH + PROCESSED_FILE).is_file(): 
        firstTime = True 
        with open(DATA_PATH + "current_files.txt") as cur_f: 
            files2process = [line[:-1] for line in cur_f.readlines()]
    else:
        firstTime = False
        with open(DATA_PATH + PROCESSED_FILE) as proc_f: 
            proc_f_text = proc_f.readlines() 
    
        with open(DATA_PATH + "current_files.txt") as cur_f: 
            cur_f_text = cur_f.readlines() 
        
        # Find and print the diff: 
        start = False
        for line in difflib.unified_diff(proc_f_text, cur_f_text): 
            if line[0] == '@':
                start = True
            
            if start and line[0] == '+':
                # print(line[1:-1])
                files2process.append(line[1:-1])
    
    # print(files2process)
    shutil.move(DATA_PATH+"current_files.txt", DATA_PATH + PROCESSED_FILE)
    return files2process, firstTime
    
    
    
if __name__ == "__main__":
    # read API keys for Pinecone and OpenAI
    #   Should have keys saved in .env file
    success_env = load_dotenv(find_dotenv())
    
    # Identifiy the text files that are not processed yet.
    files2process, first_time = getTextFiles2Add()
    print("Number of files Processed: ", len(files2process))
    
    headers_to_split_on = [
        ("#", "Header 1"),
    ]
    
    new_documents = []
    for file in files2process:
        f = open(file, 'r')
        text = f.read()
        
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_splits = markdown_splitter.split_text(text)
        new_documents.extend(md_splits)
    
    if len(new_documents) > 0:
        # print(new_documents)
        if USE_OPENAI:
            embedding = AzureOpenAIEmbeddings(
                azure_deployment="text-embedding-3-large",
                api_version="2023-06-01-preview",
            )
            vector_store_dir = "../hdr-manager-rmit-chroma_db_v2"
        else:
            embedding = MistralAIEmbeddings()
            vector_store_dir = "../hdr-manager-rmit-chroma_db_mistral"
        
        if first_time:
            vectorstore = Chroma.from_documents(
                    new_documents,
                    embedding,
                    persist_directory=vector_store_dir,
            )
        else:
            vectorstore = Chroma(persist_directory=vector_store_dir, 
                                embedding_function=embedding)
            vectorstore.add_documents(new_documents)
    else:
        print("No ducuments to add.")    
        
    
        