# 基于官方 python 镜像
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目文件
COPY . .

# 启动服务
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

