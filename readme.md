### 启动方式 ###


# 本地运行
# python3 -m venv venv && source venv/bin/activate
# pip install -r requirements.txt
# uvicorn app:app --host 0.0.0.0 --port 8000

# Docker 运行（可选）
# docker build -t mlx-openai-api .
# docker run -p 8000:8000 mlx-openai-api

### 访问接口 ###
# curl http://localhost:8000/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#         "model": "mlx-mistral",
#         "messages": [{"role": "user", "content": "Hello!"}]
#       }'

# 返回结果为标准 OpenAI API 规范