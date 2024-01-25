from langchain.memory import ChatMessageHistory
from pydantic import BaseModel, Field
from typing import List


class ModelParams(BaseModel):
  temperature: float
  max_length: int

class ChatRequest(BaseModel):
  input: str
  chat_history: List[str]
  model: str
  model_params: ModelParams

class VectorizedParams(BaseModel):
  chunk_size: int
  chunk_overlap: int


class FileUploadRequest(BaseModel):
  url: str
  file_name: str
  vectorize_params: VectorizedParams


class Output(BaseModel):
  output: str


def generate_chat_history(chat_history: List[str]):
  for i in range(len(chat_history)):
    if i % 2 == 0:
      chat_history += "Human: " + chat_history[i] + "\n"
    else:
      chat_history += "AI: " + chat_history[i] + "\n"
  return chat_history
