from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ciphers import caesar_cipher, vigenere_cipher, aes_simulation, md5_simulation, sha256_simulation

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    if not data or 'text' not in data or 'cipher' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    text = data['text']
    cipher_type = data['cipher']
    
    # Optional parameters based on cipher type
    key = data.get('key')
    
    if cipher_type == 'caesar':
        try:
            shift = int(key) if key else 3
            result = caesar_cipher(text, shift, encrypt=True)
            return jsonify(result)
        except ValueError:
            return jsonify({'error': 'Caesar cipher requires an integer key (shift)'}), 400
            
    elif cipher_type == 'vigenere':
        if not key or not isinstance(key, str):
            return jsonify({'error': 'Vigenere cipher requires a string key'}), 400
        result = vigenere_cipher(text, key, encrypt=True)
        return jsonify(result)
        
    elif cipher_type == 'aes':
        if not key or not isinstance(key, str):
            return jsonify({'error': 'AES requires a string key (16, 24, or 32 chars recommended)'}), 400
        result = aes_simulation(text, key, encrypt=True)
        return jsonify(result)
        
    elif cipher_type == 'md5':
        result = md5_simulation(text)
        return jsonify(result)
        
    elif cipher_type == 'sha256':
        result = sha256_simulation(text)
        return jsonify(result)
        
    else:
        return jsonify({'error': 'Unsupported cipher type'}), 400

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    if not data or 'text' not in data or 'cipher' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    text = data['text']
    cipher_type = data['cipher']
    key = data.get('key')
    
    if cipher_type == 'caesar':
        try:
            shift = int(key) if key else 3
            result = caesar_cipher(text, shift, encrypt=False)
            return jsonify(result)
        except ValueError:
            return jsonify({'error': 'Caesar cipher requires an integer key (shift)'}), 400
            
    elif cipher_type == 'vigenere':
        if not key or not isinstance(key, str):
            return jsonify({'error': 'Vigenere cipher requires a string key'}), 400
        result = vigenere_cipher(text, key, encrypt=False)
        return jsonify(result)
        
    elif cipher_type == 'aes':
        if not key or not isinstance(key, str):
             return jsonify({'error': 'AES requires a string key (16, 24, or 32 chars recommended)'}), 400
        result = aes_simulation(text, key, encrypt=False)
        return jsonify(result)
        
    elif cipher_type in ['md5', 'sha256']:
        return jsonify({'error': 'Hashing algorithms cannot be decrypted.'}), 400
        
    else:
         return jsonify({'error': 'Unsupported cipher type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
