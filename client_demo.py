import requests
import json

def chat_with_model(prompt, model="Qwen/Qwen2.5-3B-Instruct", temperature=None):
    """
    与本地运行的大模型API服务进行对话
    """
    url = "http://localhost:8000/v1/chat/completions"
    # url = "https://api.deepseek.com/v1/chat/completions"
    model = "deepseek-chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"test-api-key"  # 添加Bearer前缀  # 替换为你的API密钥
    }

    # 多行字符串
    system_prompt = (
        "你是TrustAI，一个万向信托推出的AI智能助手。\n"
        "请直接回答用户的问题，不要创建虚构的对话。\n"
        "不要重复用户的问题，只需提供一个简洁、准确的回答。"
    )

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    # 只有当temperature不为None时才添加到请求中
    if temperature is not None:
        data["temperature"] = temperature
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"错误: {response.status_code}, {response.text}"

def main():
    print("欢迎使用本地大模型聊天程序！输入'退出'结束对话。")
    
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("再见！")
            break
        
        print("\n正在思考...")
        print("user_input: ", user_input)
        response = chat_with_model(user_input)
        print(f"\n大模型: {response}")

if __name__ == "__main__":
    main()