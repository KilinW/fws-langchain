from typing import List
from dotenv import load_dotenv
import os

from fastapi import FastAPI
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain

from utils.io import ChatRequest
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

class ChatHistoryItem(BaseModel):
    input: str
    response: str

class ChatRequest(BaseModel):
    input: str
    model: str
    chat_history: List[ChatHistoryItem]

@app.post("/agent/")
async def agent(request: ChatRequest) -> dict:
  chat_history = request.chat_history
  folder_path = './samples'
  document = []
  for file in os.listdir(folder_path):
      if file.endswith('.pdf'):
          file_path = os.path.join(folder_path, file)
          loader = UnstructuredPDFLoader(file_path)
          document.extend(loader.load())
  text_spilter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=300, separators=[" ", ",", "\n"])
  pages = text_spilter.split_documents(document)
  embeddings = HuggingFaceEmbeddings()
  faiss_index = FAISS.from_documents(pages, embeddings)

  os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

  llm = HuggingFaceHub(
    repo_id=request.model,
    model_kwargs={"temperature":0.2, "max_length":1500},
  )
  chain = load_qa_chain(llm, chain_type="stuff")
  """Handle a request."""
  #print(request.input)
  docs = faiss_index.similarity_search(request.input, k=2)
  res = chain.run(input_documents=docs, question=request.input, chat_history=chat_history)
  #print(res)
  reference1 = docs[0].page_content
  reference2 = docs[1].page_content
  response_data = {
        "answer": res,
        "reference1": reference1,
        "reference2": reference2
  }

  return response_data



if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)