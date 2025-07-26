from langchain_openai import OpenAIEmbeddings
from src.configs import env_config

embeddings = OpenAIEmbeddings(
    model=env_config.embedding_model
)