# app.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import asyncio

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)

@app.get("/chat")
async def generate(input_text: str):
    model = client.models.list().data[0].id
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": input_text}],
        stream=True,
    )

    async def generate_text():
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
            await asyncio.sleep(0.1)  # 模拟流式输出延迟

    return StreamingResponse(generate_text(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
