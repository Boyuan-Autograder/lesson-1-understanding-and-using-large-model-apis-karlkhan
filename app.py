import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
TOKEN = os.getenv("TOKEN")

def chat_stream(user_text):
    # 1. 硅基流动聊天完成接口
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",   # 2. 模型名称
        "messages": [{"role": "user", "content": user_text}],  # 3. 用户消息
        "stream": True                         # 4. 开启流式
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}",    # 5. 认证头
        "Content-Type": "application/json"     # 6. 数据格式
    }

    # 7. 使用 POST 方法，并开启流
    with requests.post(url, headers=headers, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8").strip()
            if decoded == "data: [DONE]":      # 8. 流结束标志
                break
            if decoded.startswith("data: "):   # 9. 有效 chunk
                try:
                    data_json = json.loads(decoded[len("data: "):])  # 10. 去掉前缀
                    choices = data_json.get("choices", [])           # 11. 取 choices
                    for choice in choices:
                        delta = choice.get("delta", {})              # 12. 取 delta
                        text = delta.get("content")                  # 13. 取内容
                        if text:
                            print(text, end="", flush=True)
                except json.JSONDecodeError:
                    continue

if __name__ == "__main__":
    print("SiliconFlow ChatBot")
    while True:
        user_input = input("\n你: ")
        print("AI: ", end="", flush=True)
        chat_stream(user_input)
        print()