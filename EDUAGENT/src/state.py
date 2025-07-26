from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from datetime import date
from langgraph.graph import StateGraph, MessagesState, START, END , add_messages
from langchain_core.messages import (
    AnyMessage)
from langchain_core.documents import Document

# class LearningPreference(BaseModel):
#     """Represents learning preferences and methods preferred by the learner."""
    
#     method: Optional[List[str]] = Field(
#         default_factory=list,
#         description="Phương pháp học ưa thích, ví dụ: 'Video', 'Lý thuyết trước'"
#     )
#     focus: Optional[List[str]] = Field(
#         default_factory=list,
#         description="Ưu tiên học nội dung gì"
#     )

class AgentProfile(BaseModel):
    """
    Complete learner profile containing all necessary information for creating a personalized study plan.
    Extends MessagesState to support conversation history.
    """
    learning_goal: str = Field(default="", description="Mục tiêu học tập, ví dụ: 'Ôn thi THPT'")
    expected_result: str = Field(default="", description="Kết quả mong muốn")
    deadline: Optional[str] = Field(None, description="Hạn chót cần đạt mục tiêu (ví dụ: '2025-07-31')")
    available_time: Optional[str] = Field(default="", description="Thời gian có thể học")
    current_ability: Optional[str] = Field(default="", description="Khả năng hiện tại")
    learning_obstacles: List[str] = Field(default_factory=list, description="Khó khăn hiện tại")
    learning_preference: Optional[str] = Field(default="", description="Sở thích học tập")
    specific_topics_interest: List[str] = Field(default_factory=list, description="Chủ đề muốn tập trung học")
    notes: Optional[str] = Field(None, description="Ghi chú thêm")
    finished: bool = Field(default=False, description="Trạng thái đã hoàn thành hồ sơ")

class Resource(BaseModel):
    """Represents a learning resource with type and access information."""
    
    type: str = Field(..., description="Type of the resource")
    title: str = Field(..., description="Title of the resource", min_length=1)

class DailyStudyItem(BaseModel):
    """Represents a single day's study plan within a module."""
    
    day: int = Field(..., description="Day number within the module (starting from 1)", ge=1)
    hours: float = Field(..., description="Study hours for the day", gt=0, le=24)
    notes: Optional[str] = Field(None, description="Optional note or focus area for the day")

class StudyModule(BaseModel):
    """Represents a complete study module with objectives, resources, and schedule."""
    
    id: str = Field(..., description="Unique identifier for the module", min_length=1)
    title: str = Field(..., description="Name of the study module", min_length=1)
    objectives: List[str] = Field(..., description="List of learning objectives for this module", min_items=1)
    description: Optional[str] = Field(None, description="Brief description of what this module covers")
    prerequisites: Optional[List[str]] = Field(None, description="Required knowledge before starting this module")
    duration_estimate: str = Field(..., description="Estimated duration for completing the module (e.g., '4 days')")
    priority: str = Field("medium", description="Priority level of the module", )
    resources: Optional[List[Resource]] = Field(None, description="Suggested learning resources")
    daily_study_schedule: Optional[List[DailyStudyItem]] = Field(None, description="Suggested daily study schedule for this module")

class Constraints(BaseModel):
    """Represents scheduling and time constraints for the study plan."""
    
    available_hours_per_day: float = Field(..., description="Maximum number of study hours available per day", gt=0, le=24)
    deadline: date = Field(..., description="Deadline to complete the entire study plan")
    max_modules_per_week: Optional[int] = Field(None, description="Maximum number of modules allowed per week (if any)", ge=1)

class LearnerProfile(BaseModel):
    """Represents the learner's current level and preferences."""
    
    level: str = Field(..., description="Current learning level of the student")
    preferred_study_style: Optional[str] = Field(None, description="Preferred study style (e.g., learning by doing, watching videos)")
    learning_goals: List[str] = Field(..., description="List of high-level learning goals", min_items=1)

class StudyPlanOverview(BaseModel):
    """Complete study plan overview containing all modules, constraints, and learner information."""
    
    modules: List[StudyModule] = Field(..., description="List of study modules with objectives, priority, resources, and daily time suggestions", min_items=1)
    total_duration: str = Field(..., description="Overall study plan duration, e.g., '3 weeks', '15 days'")
    constraints: Constraints = Field(..., description="Study time and scheduling constraints")
    learner_profile: LearnerProfile = Field(..., description="Student's current level and goals")

class State(TypedDict): 
    messages: Annotated[list[AnyMessage], add_messages]
    learning_goal: str   
    expected_result: str 
    deadline: str
    available_time: str
    current_ability: str
    learning_obstacles: List[str]  # Changed from str to List[str]
    learning_preference: str
    specific_topics_interest: List[str]  # Changed from str to List[str]
    notes: str

# class ChapterLevel(BaseModel):
#     chapter_id: str  = Field(default="", description="mã định danh, là duy nhất của mỗi chương, ví dụ: 'ch01'")
#     chapter_name: str = Field(default="", description="tên chương, tên chapter của môn toán, ví dụ: 'mệnh đề tập hợp'")
#     level: str =   Field(default="", description="trình độ hiện tai của người học về chương học, ví dụ: 'cơ bản'")

# class MiniTestState(BaseModel):
#     message: Annotated[list[AnyMessage], add_messages]
#     grade: int = Field(..., description="tình trạng hiện tại của ngươi học với chương trình toán 10, vidu : 'tôi đã biết về chương trình toán 10'")
#     chapter: List[ChapterLevel] = Field(..., description="Danh sách trình độ theo từng chương")

# ------------------ STATE ------------------
class ChapterLevel(BaseModel):
    chapter_id: str = Field(..., description="ID chương, ví dụ: 'ch01'")
    chapter_name: str = Field(..., description="Tên chương, ví dụ: 'tập hợp'")
    level: str = Field(..., description="Trình độ hiện tại, ví dụ: 'cơ bản'")

class MiniTestState(MessagesState):  # Kế thừa MessagesState
    grade: str = Field(..., description="Tình trạng hiện tại, ví dụ: 'lớp 10'")
    chapter: List[ChapterLevel] = Field(..., description="Danh sách chương và trình độ")

