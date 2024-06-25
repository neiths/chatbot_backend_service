import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent

def load_llm_model(provider='openai'):
    if provider == 'openai':
        OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
    else:
        raise ValueError(f"Unknown provider: {provider}")
    
    return llm

llm = load_llm_model('openai')

def get_prompt(character='supervisor'):
    if character == "supervisor":
        system_prompt = ("Bạn là giám thị, có thể gọi giáo viên bộ môn hỗ trợ trả lời câu hỏi bằng các sử dụng tool"
                        "supervisor_select_role_tools với input là 'math' hoặc 'literature' để chọn bộ môn cần hỗ trợ"
                        "đối với môn toàn thì câu hỏi thường có số bên trong đó.")
    elif character == "math":
        system_prompt = ("Bạn là giáo viên môn toán, hãy giúp học sinh giải bài toán bằng cách sử dụng tool add với input là 2 số cần cộng. Phải sử dụng máy tính để tính để đem lại kết quả chính xác nhất")
    else:
        system_prompt = ("Bạn là giáo viên môn văn, hãy giúp học sinh tìm kiếm thông tin bài văn bằng cách sử dụng tool"
                        "get_info_from_wikipedia với input là tên tác phẩm văn học")
                    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    
    return prompt

class WikipediaInput(BaseModel):
    query: str = Field(description="should be a search query")

@tool("get_info_from_wikipedia", args_schema=WikipediaInput)
def get_info_from_wikipedia(query: str) -> str:
    """Get information from wikipedia using the query provided."""
    output = WikipediaAPIWrapper().run(query)
    return output

tools_for_literature = [get_info_from_wikipedia]
literature_agent_runnable = create_openai_functions_agent(llm=llm, tools=tools_for_literature, prompt=get_prompt())

class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")
    
@tool("add", args_schema=CalculatorInput)
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

tools_for_math = [add]
math_agent_runnable = create_openai_functions_agent(llm=llm, tools=tools_for_math, prompt=get_prompt())

class SelectRoleInput(BaseModel):
    role: str = Field(description="role to select")
    
@tool("supervisor_select_role_tools", args_schema=SelectRoleInput)
def supervisor_select_role_tools(role: str) -> str:
    """Select role"""
    return role

tools_for_supervisor = [supervisor_select_role_tools]
supervisor_agent_runnable = create_openai_functions_agent(llm=llm, tools=tools_for_supervisor, prompt=get_prompt())

