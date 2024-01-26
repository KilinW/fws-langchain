"""
Description: Entrypoint for the application.
"""

from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.io import Output, ChatRequest, FileUploadRequest, generate_chat_history, generate_reference_output, generate_formatted_docs
from ingest import ingest_docs
from chain import get_chain
from upload import upload_to_gcs

load_dotenv()


app = FastAPI(
  title="LangChain Server",
  description="A simple API server using LangChain's Runnable interfaces",
)


app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"],
)


@app.post("/agent/")
async def agent(request: ChatRequest) -> dict:
  """Handle a request."""
  db = ingest_docs(request.params.langchain_params)
  chain = get_chain(request.model, request.params.model_params.dict())
  
  chat_history = generate_chat_history(request.chat_history)

  docs = db.similarity_search(request.input, k=2)

  formatted_docs = generate_formatted_docs(docs)

  reference_output = generate_reference_output(docs)


  model_output = chain.run({
    "instruction": request.instruction,
    "input": request.input,
    "chat_history": chat_history,
    "retrieved_document": formatted_docs,
  })

  response_data = {
        "model": request.model,
        "model_params": request.params.model_params,
        "input": request.input,
        "answer": model_output,
        "reference1": formatted_docs,
        "page": reference_output,
        "langchain_params": request.params.langchain_params,
  }

  return response_data
  


@app.post("/feedback/")
async def feedback(request) -> Output:
  """Handle feedbacks"""
  print(request)
  return Output(output="OK")


@app.post("/upload_file/")
async def upload_file(request: FileUploadRequest):
  """Handle files upload to GCS"""
  upload_to_gcs(project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), url=request.url, file_name=request.file_name)
  ingest_docs()
  return {"message": "file uploaded successfully"}


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)