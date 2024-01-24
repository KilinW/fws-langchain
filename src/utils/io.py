from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from typing import List, Optional, Dict



# 5. Adding chain route

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

class Input(BaseModel):
  input: str

class Output(BaseModel):
  output: str

class ChatRequest(BaseModel):
  input: str
  chat_history: List[str]
  model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
  model_params: Optional[Dict] = None
