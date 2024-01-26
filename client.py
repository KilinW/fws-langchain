import requests

chat_history = []
def send_request(input_text):
    global chat_history 
    request_data = {
        "input": input_text,
        "model": "gpt-3.5-turbo",
        "model_params": {"temperature":0, "max_length":1000},
        "chat_history": chat_history
    }

    response = requests.post("http://localhost:8000/agent/", json=request_data)
    response_data = response.json()
    chat_history.append({
        "input": input_text,
        "response": response_data.get("answer"),
    })

    print("Answer:", response_data.get("answer"))
    print("Reference:", response_data.get("reference1"))
    print("Reference Page:", response_data.get("page"))
    #print("Reference 2:", response_data.get("reference2"))
    #print("Page 2:", response_data.get("page2"))
    print("Chat History:", chat_history)

send_request("x-100機台未啟動怎麼辦")
send_request("有哪些基本的機台保護措施？")