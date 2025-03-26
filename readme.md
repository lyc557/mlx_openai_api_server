### 启动方式 ###
# 本地运行
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

# 端口如占用
```bash
lsfo -i :8000
kill -9 进程号
```
或者根据启动时答应的信息看情况修改端口
```bash
INFO:     Started server process [49796]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

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