# Cryptography Simulation

An interactive web application for learning cryptography through step-by-step visual simulation.

This project combines a Flask backend with a modern frontend UI to demonstrate how common encryption and hashing algorithms transform input data. Instead of only showing final outputs, it animates intermediate states so learners can understand the process.

## Project Description (GitHub About)

Interactive Flask-based cryptography visualizer that simulates Caesar, Vigenere, AES, MD5, and SHA-256 with animated step-by-step transformations.

## Highlights

- Interactive simulation dashboard for cryptographic operations.
- Supports both encryption/decryption and one-way hashing workflows.
- Detailed step rendering for each algorithm.
- Adjustable simulation speed for classroom demos and self-learning.
- Clear API-driven architecture (frontend calls Flask JSON endpoints).
- Responsive UI with glassmorphism/cyber style.

## Supported Algorithms

1. Caesar Cipher
- Type: Symmetric substitution cipher.
- Operations: Encrypt and decrypt.
- Key: Integer shift (default `3` if omitted).
- Visualization: Character-level shift formula for each alphabetic character.

2. Vigenere Cipher
- Type: Polyalphabetic substitution cipher.
- Operations: Encrypt and decrypt.
- Key: String key phrase.
- Visualization: Per-character key alignment and modular arithmetic formula.

3. AES Simulation (ECB)
- Type: Modern block cipher (real encryption call via PyCryptodome).
- Operations: Encrypt and decrypt.
- Key: String key; normalized internally to AES-compatible lengths.
- Visualization: Block-level input/output plus simulated intermediate round-like metrics for learning.

4. MD5
- Type: One-way hashing.
- Operations: Hash only.
- Key: Not required.
- Visualization: Conceptual chunk processing and final digest.

5. SHA-256
- Type: One-way hashing.
- Operations: Hash only.
- Key: Not required.
- Visualization: Real schedule/compression sampling and final digest.

## Important Notes

- MD5 and SHA-256 are hashes, not ciphers. They cannot be decrypted.
- AES mode in this project is `ECB` for educational simplicity, not production security.
- Some AES round visuals are intentionally simulated to make internal phases easier to explain.
- This project is intended for education, demos, and concept visualization.

## Tech Stack

- Backend: Python, Flask, Flask-CORS
- Crypto library: PyCryptodome
- Frontend: HTML, CSS, Vanilla JavaScript

## Project Structure

```text
Cryptography Simulation/
|-- app.py
|-- ciphers.py
|-- requirements.txt
|-- static/
|   |-- css/
|   |   `-- style.css
|   `-- js/
|       `-- main.js
`-- templates/
    `-- index.html
```

## How It Works

1. User selects algorithm and operation in the browser.
2. Frontend sends JSON payload to:
- `POST /api/encrypt` for encryption/hash
- `POST /api/decrypt` for decryption
3. Backend (`app.py`) validates input and dispatches to cipher/hash functions in `ciphers.py`.
4. Backend returns:
- `original` input
- `result` output
- `steps` array for animation
5. Frontend animates each step in sequence with adjustable delay.

## API Reference

### `POST /api/encrypt`

Request body:

```json
{
  "text": "HELLO",
  "cipher": "caesar",
  "key": "3"
}
```

`cipher` values:
- `caesar`
- `vigenere`
- `aes`
- `md5`
- `sha256`

Response (shape):

```json
{
  "original": "HELLO",
  "result": "KHOOR",
  "steps": [],
  "cipher": "caesar",
  "operation": "encrypt"
}
```

### `POST /api/decrypt`

Request body:

```json
{
  "text": "KHOOR",
  "cipher": "caesar",
  "key": "3"
}
```

Notes:
- `md5` and `sha256` return error on decrypt requests.

## Setup and Run

### Prerequisites

- Python 3.10+ (tested in this workspace with Python 3.13 artifacts)
- `pip`

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "Cryptography Simulation"
```

### 2. Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Example API Calls

### Caesar Encrypt

```bash
curl -X POST http://127.0.0.1:5000/api/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text":"HELLO","cipher":"caesar","key":"3"}'
```

### Vigenere Decrypt

```bash
curl -X POST http://127.0.0.1:5000/api/decrypt \
  -H "Content-Type: application/json" \
  -d '{"text":"RIJVS","cipher":"vigenere","key":"KEY"}'
```

### SHA-256 Hash

```bash
curl -X POST http://127.0.0.1:5000/api/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text":"hello world","cipher":"sha256"}'
```

## Error Handling

The backend returns HTTP `400` for invalid requests such as:
- Missing `text` or `cipher`
- Non-integer Caesar key
- Missing string key for Vigenere/AES
- Decrypt attempt for hash algorithms
- Unsupported cipher type

## Learning Use Cases

- Intro cryptography workshops
- Classroom demonstrations
- Security education labs
- Self-study on classical vs modern crypto concepts

## Security Disclaimer

This application is educational. Do not use it as-is for securing real-world sensitive data. In particular:
- ECB mode is not recommended for secure production systems.
- Visualization-oriented behavior may differ from hardened implementations.

## Future Improvements

- Add CBC/GCM visualizations with IV/nonce flow.
- Add RSA or ECC modules for asymmetric cryptography demos.
- Export simulation timeline as JSON/PNG.
- Add unit tests for API and algorithm outputs.
- Add Docker support for one-command deployment.

## Troubleshooting

1. `ModuleNotFoundError`
- Ensure virtual environment is active.
- Re-run `pip install -r requirements.txt`.

2. AES decryption fails
- Check that ciphertext is valid Base64.
- Ensure key matches encryption key.

3. PowerShell script execution policy blocks venv activation
- Run PowerShell as user and allow local scripts:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## License

No license file is currently included in this repository.

If you plan to publish this project publicly, add a `LICENSE` file (for example, MIT) to clarify usage rights.
