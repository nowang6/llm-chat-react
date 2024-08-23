from flask import Flask, Response, request
from flask_cors import CORS
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)  # 这行添加了 CORS 支持

openai_api_key = "key"

client = OpenAI(api_key=openai_api_key, base_url="https://api.deepseek.com")
model = "deepseek-chat"

@app.route('/chat', methods=['GET'])
def stream():
    input_text = request.args.get('input_text', '')
    def event_stream():
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": input_text}],
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {json.dumps({'content': content})}\n\n"
        yield "data: [DONE]\n\n"  # 发送结束信号

    return Response(event_stream(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)