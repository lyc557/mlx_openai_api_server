### 启动方式 ###
# 本地运行
# python3 -m venv venv && source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --host 0.0.0.0 --port 8000

# Docker 运行（可选）
# docker build -t mlx-openai-api .
# docker run -p 8000:8000 mlx-openai-api

### 模型配置 ###
模型配置在 config.py 文件中管理，目前支持以下模型：
- deepseek-ai/DeepSeek-R1-Distill-Qwen-7B（默认模型）
- mlx-community/Mistral-7B-v0.1-mlx

如需使用其他模型，请在 config.py 的 available_models 列表中添加。

### 代理配置 ###
如需配置代理，请在项目根目录创建 .env 文件并设置以下环境变量：
```env
PROXY_HOST=your.proxy.host
PROXY_PORT=your.proxy.port
```

### 访问接口 ###

# 示例：
```bash
curl http://localhost:8000/v1/chat/completions \
   -H "Content-Type: application/json" \
   -d '{
         "model": "mlx-mistral",
         "messages": [{"role": "user", "content": "Hello!"}]
       }'
```
# 返回结果为标准 OpenAI API 规范