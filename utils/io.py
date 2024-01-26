from langchain.memory import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List, Dict


prompt = PromptTemplate(
  input_variables = ["input", "chat_history", "retrieved_document"],
   template="\
    你是一個廠務知識的聊天機器人，你擅長並只能根據Context和Chat History回答Question，\
    以下是Context、Chat History和Question，請你只針對該Question回答。\n\n\
    Context: {retrieved_document} \n\n\
    Chat History:\n{chat_history}\n\
    Question:{input} \n\
    Answer:",
)


class ChatRequest(BaseModel):
  input: str
  chat_history: List[str]
  model: str
  model_params: Dict

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
  output = ""
  for i in range(len(chat_history)):
    if i % 2 == 0:
      output += "Human: " + chat_history[i] + "\n"
    else:
      output += "AI: " + chat_history[i] + "\n"
  return output

def generate_reference_output(docs):
  reference_output = "\n"
  for doc in docs:
    pdf_name = doc.metadata["source"].split("/")[-1]
    page = doc.metadata["page"]
    reference_output += f"{pdf_name} | Page {page+1}\n"
  return reference_output

def generate_formatted_docs(docs):
  formatted_docs = ""
  for doc in docs:
    context = doc.page_content.replace("\n", "")
    formatted_docs += f"{context}\n\n"
  return formatted_docs
