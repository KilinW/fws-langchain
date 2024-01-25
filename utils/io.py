from langchain.memory import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List


prompt = PromptTemplate(
  input_variables = ["input", "chat_history", "retrieved_document"],
   template="\
    你是一個場務知識的聊天機器人，你擅長根據Context和Chat History回答問題，\
    以下是Context、Chat History和問題，請你只針對該問題回答。\n\n\
    Context: {retrieved_document} \n\n\
    Chat History:\n{chat_history}\n\n\
    Question:{input} \n\
    Answer:",
)


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
