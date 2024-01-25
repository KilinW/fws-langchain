from upload import upload_to_gcs
from unittest.mock import patch, Mock
import os

# Mocking the requests.get call
@patch('requests.get')
# Mocking the Google Cloud Storage client
@patch('google.cloud.storage.Client')
def test_upload_to_gcs(mock_storage_client, mock_requests_get):
    # Set up the mock response object for requests.get
    mock_response = Mock()
    mock_response.content = b'mocked_file_content'
    mock_requests_get.return_value = mock_response

    # Setting environment variables for the test
    os.environ["GOOGLE_CLOUD_STORAGE_BUCKET"] = "mock_bucket"

    # Mocking the bucket and blob objects
    mock_bucket = Mock()
    mock_blob = Mock()
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_storage_client.return_value.bucket.return_value.blob.return_value = mock_blob

    # Call the function with mock parameters
    upload_to_gcs('mock_project_id', 'http://example.com/mock_file.pdf', 'mock_file.pdf')

    # Check if requests.get was called with the correct URL
    mock_requests_get.assert_called_with('http://example.com/mock_file.pdf')

    # Check if the file was uploaded to the correct bucket and blob
    mock_storage_client.return_value.bucket.assert_called_with('mock_bucket')
    mock_storage_client.return_value.bucket.return_value.blob.assert_called_with('mock_file.pdf')
    mock_blob.upload_from_string.assert_called_with(b'mocked_file_content', content_type="application/pdf")

# Add any additional tests as needed
