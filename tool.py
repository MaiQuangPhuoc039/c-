from langchain_core.tools import tool

def create_retrieve_tool(vector_db, retrieve_count: int):
    """Create retrieve tool for the bot."""
    @tool(response_format="content")
    def retrieve(query: str):
        """Retrieve information related to a query."""
        retrieved_docs = vector_db.db.similarity_search(
            query, 
            k=retrieve_count,
        )
        content = "\n\n".join(
            f"Content: {doc.page_content}"
            for doc in retrieved_docs
        )
        return content
    return retrieve

def create_parser_output_tool(llm_client, state):
    """Create tool for parsing output.""" 
    @tool(response_format="content_and_artifact")
    def parse_output(query: str):
        """
        Trích xuất hồ sơ học tập  từ các tin nhắn đã thu thập trong hội thoại.
        Chức năng này sử dụng LLM để phân tích nội dung hội thoại giữa người học và AI, 
        từ đó trích xuất các thông tin đã được cung cấp một cách rõ ràng 
        Công cụ này **không đặt câu hỏi mới** mà chỉ parser khi có đủ thông tin.
        Agrs :
            query (str): Chuỗi văn bản chứa các tin nhắn đã thu thập từ người dùng.
        """
        
        llm_output = llm_client._llm.with_structured_output(state)
        
        response = llm_output.invoke(query)
        
        return "Đang xử lý hồ sơ học tập của bạn..." if response else "Không thể trích xuất hồ sơ học tập.", response
    
    return parse_output

 