"""
Description: Entrypoint for the application.
"""

from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.io import Input, Output, ChatRequest, FileUploadRequest
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

db = ingest_docs()

@app.post("/agent/")
async def agent(request: ChatRequest) -> str:
  docs = db.similarity_search(request.input, k=2)
  chain = get_chain(request.model, chain_type="stuff")
  resp = chain.run(input_documents=docs, question=request.input)

  print(resp)

  return resp

@app.post("/feedback/")
async def feedback(request: Input) -> Output:
  """Handle feedbacks"""
  print(request)
  return Output(output="OK")

@app.post("/upload_file/")
async def upload_file(request: FileUploadRequest):
  """Handle files upload to GCS"""
  upload_to_gcs(project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), url=request.url, file_name=request.file_name)
  return {"message": "file uploaded successfully"}


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)