from loaders import DocumentLoader
from processors import DocumentProcessor
import re
from langchain_core.documents import Document
from vectorstores import VectorStoreManager
from retrievers import VectorStoreRetriever

import sys , os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".." ,"..")))
from src.clients.embedding import embeddings
from src.configs import env_config
from src.clients.databases import qdrant


from langchain.embeddings import HuggingFaceBgeEmbeddings

# 1 loader 

file_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\rag\chuong_trinh_toan_10.docx"

loader = DocumentLoader(file_path)
docs = loader.load()
 

for doc in docs:
    # print(f"Page content: {doc.page_content}\n-----------------\n")  
    # print("Metadata:", doc.metadata)
    doc.metadata["chapter"] = "Chương trình Toán 10"
    doc.metadata["source"] = ""
  

vector_manager = VectorStoreManager(
    url = env_config.qdrant_url,
    api_key=env_config.qdrant_api_key
)

collection_name = "documents"
vector_store = vector_manager.create_vector_store(
    # documents=chunks,
    documents=docs, # chỉ dùng tạm
    embeddings=embeddings,
    collection_name=collection_name
)
