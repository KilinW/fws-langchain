from utils.io import ModelParams, ChatRequest, VectorizedParams, FileUploadRequest, Output, generate_chat_history, generate_reference_output
import pytest

# Test for ModelParams
def test_model_params():
    params = ModelParams(temperature=0.5, max_length=100)
    assert params.temperature == 0.5
    assert params.max_length == 100

# Add similar tests for ChatRequest, VectorizedParams, FileUploadRequest, Output here

# Test for generate_chat_history
def test_generate_chat_history():
    chat_history = ["Hi", "Hello there!", "How are you?", "I'm good, thanks!"]
    expected_output = "Human: Hi\nAI: Hello there!\nHuman: How are you?\nAI: I'm good, thanks!\n"
    assert generate_chat_history(chat_history) == expected_output

    # Test with empty chat history
    assert generate_chat_history([]) == ""

# Test for generate_reference_output
# def test_generate_reference_output():
#     docs = [
#         {"metadata": {"source": "http://example.com/doc1.pdf", "page": 10}},
#         {"metadata": {"source": "http://example.com/doc2.pdf", "page": 5}}
#     ]
#     expected_output = "Reference:\n" + "doc1.pdf | Page 10\n" + "doc2.pdf | Page 5\n"
#     assert generate_reference_output(docs) == expected_output

#     # Test with no documents
#     assert generate_reference_output([]) == "Reference:\n"

# Add any additional tests as needed
