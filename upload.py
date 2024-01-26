import requests
from google.cloud import storage
from dotenv import load_dotenv
import os

load_dotenv()

def upload_to_gcs(project_id: str, url: str, file_name: str):
  res = requests.get(url)
  file = res.content
  storage_client = storage.Client(project=project_id)
  bucket = storage_client.bucket(bucket_name=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"))
  blob = bucket.blob(blob_name=file_name)
  blob.upload_from_string(file, content_type="application/pdf")
