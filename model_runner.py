import mlx.core as mx
import os 
from mlx_lm import load, generate
from dotenv import load_dotenv
from config import MODEL_CONFIG

class ModelRunner:
    def __init__(self, model_id=None):
        # 加载环境变量
        load_dotenv()
        
        # 使用传入的model_id或配置文件中的默认值
        self.model_id = MODEL_CONFIG["default_model"]
        
        # 如果设置了环境变量，则配置代理
        if os.getenv('PROXY_HOST') and os.getenv('PROXY_PORT'):
            proxy_url = f"http://{os.getenv('PROXY_HOST')}:{os.getenv('PROXY_PORT')}"
            os.environ['HTTPS_PROXY'] = proxy_url
            os.environ['HTTP_PROXY'] = proxy_url
            print(f"[ModelRunner] Proxy configured: {proxy_url}")

        print(f"[ModelRunner] Loading model: {self.model_id}")
        self.model, self.tokenizer = load(self.model_id)
        print("[ModelRunner] Model loaded successfully.")
        

    def chat(self, messages: list, max_tokens=2048):
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
        # 检查token数量并截断
        tokens = self.tokenizer.encode(prompt)
    
        # 推理，增加max_tokens参数
        output = generate(
            self.model, 
            self.tokenizer, 
            prompt, 
            verbose=True,
            max_tokens=max_tokens  # 增加最大输出token数量
        )
        
        # 清理输出中的特殊标记
        cleaned_output = output.replace("<|im_start|>", "").replace("<|im_end|>", "")
        
        print(f"[ModelRunner] Output: {cleaned_output}")
        
        return cleaned_output