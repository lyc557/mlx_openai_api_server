from huggingface_hub import list_models, model_info
import time
import requests.exceptions
import os
from dotenv import load_dotenv
import json
from config import MODEL_CONFIG

# 从.env文件加载环境变量
load_dotenv()

# 设置代理
proxy_host = os.getenv("PROXY_HOST")
proxy_port = os.getenv("PROXY_PORT")
if proxy_host and proxy_port:
    proxy_url = f"http://{proxy_host}:{proxy_port}"
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['HTTP_PROXY'] = proxy_url
    print(f"已设置代理: {proxy_url}")
else:
    print("未找到代理设置或.env文件中缺少PROXY_HOST和PROXY_PORT")

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

def get_model_max_tokens(model_id, max_retries=3):
    """
    获取模型的最大token限制
    """
    for attempt in range(max_retries):
        try:
            info = model_info(model_id)
            
            # 尝试从模型卡片的配置信息中获取
            if hasattr(info, 'config') and info.config:
                config = json.loads(info.config)
                if 'max_position_embeddings' in config:
                    return config['max_position_embeddings']
                elif 'n_positions' in config:
                    return config['n_positions']
                elif 'max_sequence_length' in config:
                    return config['max_sequence_length']
            
            # 如果无法从配置中获取，则根据模型类型推断
            model_defaults = {
                "qwen": 8192,
                "deepseek": 4096,
                "mistral": 8192,
                "minicpm": 4096,
                "llama": 4096
            }
            
            # 根据模型ID判断模型类型
            model_name = model_id.lower()
            for model_type, max_tokens in model_defaults.items():
                if model_type in model_name:
                    print(f"根据模型名称推断最大token限制: {max_tokens}")
                    return max_tokens
            
            # 如果无法确定，返回保守的默认值
            print("无法确定模型的最大token限制，使用默认值: 2048")
            return 2048
            
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"网络连接失败，{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"网络连接失败（已重试{max_retries}次）：{e}")
                return 2048  # 连接失败时返回默认值
        except Exception as e:
            print(f"获取模型最大token限制失败：{e}")
            return 2048  # 出错时返回默认值

# 测试模型ID
model_id = MODEL_CONFIG["default_model"]  # 修正：使用字典访问方式
exists = check_model_exists(model_id)
print(f"\n模型 {model_id} {'存在' if exists else '不存在'}")

# 获取模型的最大token限制
if exists:
    max_tokens = get_model_max_tokens(model_id)
    print(f"模型 {model_id} 的最大token限制: {max_tokens}")