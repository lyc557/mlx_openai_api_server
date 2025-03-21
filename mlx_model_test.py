from huggingface_hub import list_models, model_info
import time
import requests.exceptions
import os

# 设置代理
os.environ['HTTPS_PROXY'] = 'http://10.45.9.130:9666'  # 根据你的代理端口修改
os.environ['HTTP_PROXY'] = 'http://10.45.9.130:9666'   # 根据你的代理端口修改

def check_model_exists(model_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            info = model_info(model_id)
            print(f"模型信息：")
            print(f"- 名称：{info.modelId}")
            print(f"- 作者：{info.author}")
            print(f"- 最后更新：{info.lastModified}")
            print(f"- 下载量：{info.downloads}")
            return True
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"网络连接失败，{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"网络连接失败（已重试{max_retries}次）：{e}")
        except Exception as e:
            print(f"模型检查失败：{e}")
            return False

# 测试模型ID
model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
exists = check_model_exists(model_id)
print(f"\n模型 {model_id} {'存在' if exists else '不存在'}")