import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.schema import HumanMessage

success_env = load_dotenv(find_dotenv())

model = AzureChatOpenAI(
    azure_deployment="gpt4",
    api_version="2023-06-01-preview",
)

print(model.invoke(
    [
        HumanMessage(
            content="Translate this sentence from English to French. I love programming."
        )
    ]
))
