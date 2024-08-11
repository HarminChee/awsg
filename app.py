from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

# Replace with your API key and base URL if needed
api_key = 'sk-5pkp7lLRC2nx8hCzBfB44fD499Bf48B3B408Eb39E604Fa77'
base_url = 'https://oneapi.xty.app/v1'

openai.api_key = api_key
openai.api_base = base_url

@app.route('/generate', methods=['POST'])
def generate():
    # 打印请求数据以进行调试
    print("Received request data:", request.json)
    
    data = request.json
    model = data.get('model')
    prompt = data.get('prompt')
    temperature = data.get('temperature')
    max_tokens = data.get('max_tokens')

    # 打印收到的参数
    print(f"Model: {model}")
    print(f"Prompt: {prompt}")
    print(f"Temperature: {temperature}")
    print(f"Max Tokens: {max_tokens}")

    try:
        # 调用 OpenAI API 并打印调用状态
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        print("API call successful, response received.")
        
        # 打印响应内容
        print("Response:", response.choices[0].text)
        
        return jsonify({'output': response.choices[0].text})
    except Exception as e:
        # 打印异常信息
        print(f"Error during API call: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
