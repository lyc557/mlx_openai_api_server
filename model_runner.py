import mlx.core as mx
import os 
from mlx_lm import load, generate
from dotenv import load_dotenv

class ModelRunner:
    def __init__(self, model_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"):
        # 加载环境变量
        load_dotenv()
        
        # 如果设置了环境变量，则配置代理
        if os.getenv('PROXY_HOST') and os.getenv('PROXY_PORT'):
            proxy_url = f"http://{os.getenv('PROXY_HOST')}:{os.getenv('PROXY_PORT')}"
            os.environ['HTTPS_PROXY'] = proxy_url
            os.environ['HTTP_PROXY'] = proxy_url
            print(f"[ModelRunner] Proxy configured: {proxy_url}")

        self.model_id = model_id
        print(f"[ModelRunner] Loading model: {model_id}")
        self.model, self.tokenizer = load(model_id)
        print("[ModelRunner] Model loaded successfully.")
        

    def chat(self, messages: list):
        # 拼接 prompt
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"[System]: {msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"[User]: {msg['content']}\n"
            elif msg["role"] == "assistant":
                prompt += f"[Assistant]: {msg['content']}\n"
        print(f"[ModelRunner] Prompt: {prompt}")

        # 推理
        output = generate(self.model, self.tokenizer, prompt, verbose=True)
        print(f"[ModelRunner] Output: {output}")

        return output