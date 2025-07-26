import logging
from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_qdrant import QdrantVectorStore

logger = logging.getLogger(__name__)

class VectorStoreRetriever:
    """
    Retriever for document search using vector stores.
    
    This class provides document retrieval functionality for RAG pipelines
    using similarity search in vector stores.
    """
    
    def __init__(
        self,
        vector_store: QdrantVectorStore,
        search_kwargs: Optional[dict] = None
    ):
        """
        Initialize the retriever.
        
        Args:
            vector_store: QdrantVectorStore instance
            search_kwargs: Additional search parameters
        """
        if not vector_store:
            raise ValueError("Vector store is required")
            
        self.vector_store = vector_store
        self.search_kwargs = search_kwargs or {"k": 4}
        
        logger.info(f"VectorStoreRetriever initialized with search_kwargs: {self.search_kwargs}")
    
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query string
            
        Returns:
            List of relevant documents
            
        Raises:
            ValueError: If query is empty
            Exception: If retrieval fails
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        try:
            documents = self.vector_store.similarity_search(
                query, 
                **self.search_kwargs
            )
            
            logger.info(f"Retrieved {len(documents)} documents for query: '{query[:50]}...'")
            return documents
            
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {str(e)}")
            raise
    
    def as_retriever(self) -> BaseRetriever:
        """
        Get the retriever as a LangChain BaseRetriever.
        
        Returns:
            BaseRetriever instance
        """
        return self.vector_store.as_retriever(search_kwargs=self.search_kwargs)
