from google.cloud import storage
from dotenv import load_dotenv
import requests
import os

load_dotenv()

def authenticate_implicit_with_adc(project_id):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
        for file in bucket.list_blobs():
            print(file.name)
    print("Listed all storage buckets.")

authenticate_implicit_with_adc(project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"))

def upload_new_file(project_id: str, url: str, file_name: str):
    res = requests.get(url)
    file = res.content
    with open("resp.pdf", "wb") as f:
        f.write(file)
    
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"))
    blob = bucket.blob(blob_name=file_name)
    blob.upload_from_filename(filename="/Users/cdxvy30/free-wang-square-lc/resp.pdf", content_type="ccc")