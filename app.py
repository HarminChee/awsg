import signal
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Update the base_url to the correct endpoint
base_url = 'https://api.xty.app/v1/chat/completions'
api_key = 'sk-CRIeTtB7ily8Tyrq577d9a2dC628484bB1C8C0B566A69200'

@app.route('/generate', methods=['POST'])
def generate():
    print("Received request data:", request.json)
    
    data = request.json
    model = data.get('model', 'gpt-3.5-turbo')  # Use the default model if not provided
    prompt = data['messages'][0]['content'] if 'messages' in data and len(data['messages']) > 0 else None
    temperature = data.get('temperature', 0.7)  # Use default temperature if not provided
    max_tokens = data.get('max_tokens', 100)  # Default max_tokens

    print(f"Model: {model}")
    print(f"Prompt: {prompt}")
    print(f"Temperature: {temperature}")
    print(f"Max Tokens: {max_tokens}")

    if prompt is None:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Prepare the request payload for the third-party API
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
            # Removed "stream": True
        }

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Make the request to the third-party API
        response = requests.post(base_url, json=payload, headers=headers)

        # Print out the raw response text for debugging
        print("Raw response text:", response.text)

        # Check if the request was successful
        if response.status_code == 200:
            try:
                output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                print("API call successful, response received.")
                print("Response:", output)
                return jsonify({'output': output})
            except ValueError:
                print("Failed to parse JSON response")
                return jsonify({'error': 'Invalid JSON response'}), 500
        else:
            print(f"Error during API call: {response.text}")
            return jsonify({'error': 'The server is overloaded or not ready yet.'}), 500

    except Exception as e:
        print(f"Error during API call: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cuhk_account = data.get('cuhk_account')

    if cuhk_account and len(cuhk_account) == 10 and cuhk_account.isdigit():
        try:
            with open('cuhk_accounts.txt', 'a') as file:
                file.write(cuhk_account + '\n')
            return jsonify({'message': 'Registration successful!'})
        except Exception as e:
            return jsonify({'error': f'Failed to save account: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Invalid CUHK account. Please enter a 10-digit number.'}), 400

def handle_exit(sig, frame):
    print("Shutting down server...")
    sys.exit(0)

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    port = 5000
    while is_port_in_use(port):
        print(f"Port {port} is in use, trying next port...")
        port += 1

    app.run(host='0.0.0.0', port=port)
