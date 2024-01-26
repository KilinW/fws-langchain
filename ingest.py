"""
1. Load files from GCS into LangChain
2. Convert to embeddings
3. Store in FAISS
"""

import logging
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, GCSDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Weaviate

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Should be GCS loader
# loader = GCSDirectoryLoader(project_name=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"))

def load_sop_pdf():
  return PyPDFLoader('./sample/機台型號_ x-100.pdf')


def load_gcs_sop_pdf():
  return GCSDirectoryLoader(project_name=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"), loader_func=PyPDFLoader)


def ingest_docs(langchain_params: dict):
  docs_from_sop_pdf = load_gcs_sop_pdf()
  print(docs_from_sop_pdf)
  logger.info(f"Loaded documents from SOP PDF.")

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=langchain_params.chunk_size,
    chunk_overlap=langchain_params.chunk_overlap,
    separators=[" ", ",", "\n"],
  )
  docs_transformed = docs_from_sop_pdf.load_and_split(text_splitter=text_splitter)

  # If using Weaviate as vector storage client, need to add metadata
  for doc in docs_transformed:
    if "source" not in doc.metadata:
      doc.metadata["source"] = ""
    if "page" not in doc.metadata:
      doc.metadata["page"] = ""
    if "title" not in doc.metadata:
      doc.metadata["title"] = ""

  embeddings = HuggingFaceEmbeddings()
  #return Weaviate.from_documents(docs_transformed, embeddings, weaviate_url="http://localhost:8765", by_text=False)
  return FAISS.from_documents(docs_transformed, embeddings)

if __name__ == "__main__":
  ingest_docs()
