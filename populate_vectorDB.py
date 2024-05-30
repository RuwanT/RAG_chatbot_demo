from dotenv import load_dotenv, find_dotenv



if __name__ == "__main__":
    # read API keys for Pinecone and OpenAI
    #   Should have keys saved in .env file
    load_dotenv(find_dotenv())
    