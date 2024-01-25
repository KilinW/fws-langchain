from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

# Mocking external dependencies
"""
@patch('main.ingest_docs')
@patch('main.get_chain')
@patch('main.upload_to_gcs')
def test_agent_endpoint(mock_upload_to_gcs, mock_get_chain, mock_ingest_docs):
    # Mocking the get_chain function to return a mock chain
    mock_chain = MagicMock()
    mock_chain.run.return_value = "Mocked Model Output"
    mock_get_chain.return_value = mock_chain

    # Mocking the db to have a similarity_search method
    mock_ingest_docs.return_value = MagicMock(similarity_search=MagicMock(return_value=[]))

    # Simulate a POST request to the /agent/ endpoint
    response = client.post("/agent/", json={
        "input": "Test question",
        "chat_history": ["Hello", "Hi there!"],
        "model": "gpt-3.5-turbo",
        "model_params": {"temperature": 0.5, "max_length": 100}
    })

    # Check the response
    assert response.status_code == 200
    assert "Mocked Model Output" in response.text
"""
    
# Testing the /feedback/ endpoint
"""
def test_feedback_endpoint():
    response = client.post("/feedback/", json={"some_key": "some_value"})
    assert response.status_code == 200
    assert response.json() == {"output": "OK"}
"""
    
# Testing the /upload_file/ endpoint
@patch('main.upload_to_gcs')
@patch('main.ingest_docs')
def test_upload_file_endpoint(mock_ingest_docs, mock_upload_to_gcs):
    response = client.post("/upload_file/", json={
        "url": "http://example.com/file.pdf",
        "file_name": "test_file.pdf",
        "vectorize_params": {"chunk_size": 500, "chunk_overlap": 300}
    })
    assert response.status_code == 200
    assert response.json() == {"message": "file uploaded successfully"}

    # Check if upload_to_gcs and ingest_docs were called
    mock_upload_to_gcs.assert_called_once()
    mock_ingest_docs.assert_called_once()

# Add any additional tests as needed
