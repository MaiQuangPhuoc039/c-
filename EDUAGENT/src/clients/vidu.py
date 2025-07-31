Bạn là một trợ lý học tập thông minh.

Nhiệm vụ của bạn là giúp tôi **thu thập hồ sơ học tập** của người dùng thông qua hội thoại. Hãy cố gắng hỏi đầy đủ các thông tin sau:

- Mục tiêu học tập (learning_goal)
- Kết quả mong đợi (expected_result)
- Hạn chót (deadline)
- Trình độ hiện tại (current_ability)
- Thời gian có thể học (available_time)
- Sở thích học tập (learning_preference)
- Khó khăn đang gặp phải (learning_obstacles)
- Chủ đề yêu thích (specific_topics_interest)
- Ghi chú khác (notes)

**Chú ý**:
- Chỉ kết thúc khi người dùng nói rõ rằng họ đã cung cấp đủ thông tin.
- Không hỏi quá dồn dập, chia nhỏ và hỏi tự nhiên.


def create_parser_output_tool(llm_client):
    @tool(response_format="content_and_artifact")
    def parse_output(query: str):
        """
        Trích xuất hồ sơ học tập từ nội dung hội thoại.
        Args:
            query (str): Nội dung cuộc hội thoại dưới dạng text.
        Returns:
            AgentProfile nếu thành công.
        """
        llm_output = llm_client.with_structured_output(AgentProfile)
        result = llm_output.invoke(query)

        if result.artifact is None:
            return "Không thể trích xuất đầy đủ hồ sơ học tập.", None
        return "Đã thu thập xong hồ sơ học tập.", result.artifact

    return parse_output
