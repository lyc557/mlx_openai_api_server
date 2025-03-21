from fastapi import FastAPI
from pydantic import BaseModel
import time
import uuid
from model_runner import ModelRunner

app = FastAPI()
model_runner = ModelRunner()

# 请求结构体
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: float = 0.7
    stream: bool = False

@app.get("/")
def root():
    return {"message": "MLX OpenAI API Compatible Server Running"}

@app.post("/v1/chat/completions")
def chat_completions(request: ChatRequest):
    output = model_runner.chat([msg.dict() for msg in request.messages])

    return {
        "id": str(uuid.uuid4()),
        "object": "chat.completion",
        "created": int(time.time()),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len("".join([m.content for m in request.messages]).split()),
            "completion_tokens": len(output.split()),
            "total_tokens": len("".join([m.content for m in request.messages]).split()) + len(output.split())
        }
    }