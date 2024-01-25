import requests

chat_history = []
def send_request(input_text):
    global chat_history 
    request_data = {
        "input": input_text,
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "chat_history": chat_history
    }

    response = requests.post("http://localhost:8000/agent/", json=request_data)
    response_data = response.json()
    chat_history.append({
        "input": input_text,
        "response": response_data.get("answer"),
    })

    print("Answer:", response_data.get("answer"))
    print("Reference 1:", response_data.get("reference1"))
    print("Reference 2:", response_data.get("reference2"))
    print("Chat History:", chat_history)

send_request("工作場所的高度高於多少需要定義墜落災害防止計畫？")
send_request("有哪些基本的墜落防護措施？")
