from langchain_qdrant import QdrantVectorStore
from pymongo import MongoClient
from src.configs import env_config
from src.clients.embedding import embeddings

mongo_client = MongoClient(
    host=env_config.mongodb_uri
)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    api_key = env_config.qdrant_api_key,
    collection_name="eduagent",
    url="https://2adad8b3-089a-485c-bd8e-13b1f7e81d6b.us-east4-0.gcp.cloud.qdrant.io",
)
