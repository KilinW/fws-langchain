# free-wang-square-lc
This is a langchain for some mysterious hackathon.

# Demo
Currently, I build a sample Langchain application to see how langchain communicate with **PDF file** and response with help from **OpenAI API**.

## How to start?
1. Create `.env` file with your own "**OPENAI_API_KEY**" and "**TAVILY_API_KEY**".
2. Start LangServe: `python example.py`
3. Go to `http://localhost:8000` to how langchain intermediate steps work. You can ask questions about DARPA internet protocol design.

## Structure
1. `/sample`: here comes some PDF files we want our chatbot knows.
2. `example.py`: the langchain server, currently does:
    - Load PDF file
    - Convert PDF content to embedding vectors
    - Create retriever tools to help search content based on user input
    - Create agent to actually execute prompt in specific model (I use "GPT-3.5-Turbo" for test)
    - Receive user input and generate output to user
3. `client.py`: currently works as a client to send question. **This should be replaced with Discord Bot.**
