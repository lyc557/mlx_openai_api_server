import requests
import json

def chat_with_model(prompt, model="Qwen/Qwen2.5-3B-Instruct", temperature=None):
    """
    与本地运行的大模型API服务进行对话
    """

    # url = "http://10.45.9.130:8888/v1/chat/completions"
    url = "http://127.0.0.1:8000/v1/chat/completions"
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

    QA_GEN_PROMPT_TMPL = """
        我会给你一段文本（<document></document>之间的部分），请仔细阅读并生成5个高质量的问答对。要求如下
        1. 问题要求：
        - 问题必须与文本内容直接相关
        - 避免询问文档结构相关的问题（如"在哪一章"）
        - 问题应该有实质性的信息价值
        - 优先生成需要理解和分析的问题，而不是简单的事实查找
        2. 上下文要求：
        - 必须是原文的直接引用，不允许任何形式的改写
        - 应该包含完整的相关信息，确保上下文自包含
        - 如果信息分散在多处，可以用"..."连接相关段落
        3. 答案要求：
        - 基于上下文直接回答问题
        - 保持完整性和准确性
        - 简明扼要，避免冗余
        - 使用肯定的语气
        - 不要引用文档结构（如章节、页码）

        返回格式：
        [
            {
                "question": "问题描述",
                "context": "原文引用",
                "answer": "基于上下文的答案"
            },
            {
                "question": "问题描述",
                "context": "原文引用",
                "answer": "基于上下文的答案"
            },
            {
                "question": "问题描述",
                "context": "原文引用",
                "answer": "基于上下文的答案"
            },
            {
                "question": "问题描述",
                "context": "原文引用",
                "answer": "基于上下文的答案"
            },
            {
                "question": "问题描述",
                "context": "原文引用",
                "answer": "基于上下文的答案"
            }
        ]

        如果文本主要是目录、人名列表、联系方式等无实质内容的信息，请返回空数组 []。

        下方是待分析文本：
        <document>
        {{document}}
        </document>
    """
        
    response = chat_with_model(user_input)


if __name__ == "__main__":
    main()