import requests
import json
import pyttsx3
import edge_tts_demo as edge_tts_demo
import os

MODEL1 = "llama3:8b"
MODEL2 = "llamafamily/llama3-chinese-8b-instruct:latest"
SYSTEM_SETTING = "你的名字叫欢欢，你是一个开朗活泼的女孩子。你说话风格轻松愉悦，爱捉弄人。"

engine = pyttsx3.init()
voices=engine.getProperty('voices')

url = "http://localhost:11434/api/chat"
payload = {
    "model": MODEL1,
    "messages": [
        {
            
        }
    ],
    "stream": True
}
headers = {
    "Content-Type": "application/json"
}

def get_response(messages):
    # update payload with new messages
    payload['messages'] = messages
    response = requests.post(url, json=payload, headers=headers, stream=True)
    return response

# 初始messages
messages = [{'role': 'system', 'content': SYSTEM_SETTING}]
# Read messages from file

if os.path.exists('messages.txt'):
    with open('messages.txt', 'r', encoding='utf-8') as file:
        messages = json.load(file)
else:
    messages = [{'role': 'system', 'content': SYSTEM_SETTING}]

while True:
    user_input = input("\n请输入：")
    messages.append({'role': 'user', 'content': f"{user_input}"})
    assistant_output = ""
    
    # 检查响应状态码
    response = get_response(messages)
    if response.status_code == 200:
        # 逐块读取响应内容
        try:
            print("模型输出：",end="")
            for chunk in response.iter_lines():
                if chunk:
                    # 假设每个块都是一个独立的JSON对象
                    data = json.loads(chunk.decode('utf-8'))
                    # print(json.dumps(data, indent=2))
                    if 'message' in data and 'content' in data['message']:
                        assistant_message = data['message']['content']
                        print(assistant_message, end="")
                        
                        assistant_output += assistant_message
                        # 实时语音输出
                        # engine.say(f'{assistant_message}')
                        # engine.runAndWait()
                        
                        
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")

    
    messages.append({'role': 'assistant', 'content': assistant_output})
    
    # 完成后模型输出
    # print(f'模型输出：{assistant_output}')
    
    # 完成后语音输出
    # engine.say(f'{assistant_output}')
    # engine.runAndWait()
    
    # edge_tts语音输出
    edge_tts_demo.tts(assistant_output)
    
    # Save messages to a file
    with open('messages.txt', 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False)
    
    # print('\n')
