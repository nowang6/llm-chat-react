# app.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import asyncio
import json

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = "key"

client = OpenAI(api_key=openai_api_key, base_url="https://api.deepseek.com")

@app.get("/chat")
async def generate(input_text: str):
    model = "deepseek-chat"
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": input_text}],
        stream=True,
    )

    async def generate_text():
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {json.dumps({'content': content})}\n\n"
            await asyncio.sleep(0.1)  # 模拟流式输出延迟
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate_text(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)