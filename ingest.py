import logging
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, GCSFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Weaviate
from google.cloud import storage
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sop_pdf():
    return PyPDFLoader('./sample/機台型號_ x-100.pdf')

def load_gcs_sop_pdf(file_name):
    return GCSFileLoader(project_name=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"), blob=file_name)

def list_files(bucket_name=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"), project_name=os.getenv("GOOGLE_CLOUD_PROJECT_ID")):
    storage_client = storage.Client(project_name)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    print("Blobs:")
    pdf_files = [blob.name for blob in blobs if blob.name.endswith(".pdf")]
    return pdf_files

def ingest_docs(langchain_params: dict, model: str, file_names=None):
    if not file_names:
        file_names = list_files()
        logger.info(f"Defaulting to all PDF files in GCS bucket: {file_names}")
    else:
        existing_files = list_files()
        for file_name in file_names:
            if file_name not in existing_files:
                raise ValueError(f"{file_name} not found in GCS bucket")
    
    logger.info(f"Processing file_names: {file_names}")

    docs_transformed = []

    for file_name in file_names:
        loader = load_gcs_sop_pdf(file_name)
        docs_from_sop_pdf = loader.load()
        logger.info(f"Loaded documents from SOP PDF: {file_name}")

        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=langchain_params.chunk_size,
                chunk_overlap=langchain_params.chunk_overlap,
                separators=[" ", ",", "\n"],
            )
        docs_transformed += text_splitter.split_documents(docs_from_sop_pdf)

    if model == "gpt-3.5-turbo":
        embeddings = OpenAIEmbeddings()
    elif model == "gemini-pro":
        embeddings = GoogleGenerativeAIEmbeddings()
    else:
        embeddings = HuggingFaceEmbeddings()
    return FAISS.from_documents(docs_transformed, embeddings)


if __name__ == "__main__":
    ingest_docs(langchain_params=None, file_names=[], model=None)
