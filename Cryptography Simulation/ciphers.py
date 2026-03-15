from Crypto.Cipher import AES # type: ignore
from Crypto.Random import get_random_bytes # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore
import base64
import hashlib
from typing import List, Dict, Any, Tuple

def caesar_cipher(text: str, shift: int, encrypt: bool = True):
    # Adjust shift for decryption
    if not encrypt:
        shift = -shift
        
    steps: List[Dict[str, Any]] = []
    result_chars: List[str] = []
    
    for char in text:
        if isinstance(char, str) and char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            # Mathematical transformation
            original_val = ord(char) - ascii_offset
            new_val = (original_val + shift) % 26
            new_char = chr(new_val + ascii_offset)
            
            result_chars.append(str(new_char))
            steps.append({
                'char': char,
                'isAlpha': True,
                'originalCode': ord(char),
                'shift': shift,
                'newCode': ord(new_char),
                'newChar': new_char,
                'formula': f"({original_val} + {shift}) % 26 = {new_val}"
            })
        else:
            result_chars.append(str(char))
            steps.append({
                'char': char,
                'isAlpha': False,
                'newChar': char
            })
            
    return {
        'original': str(text),
        'result': ''.join(result_chars),
        'steps': steps,
        'cipher': 'caesar',
        'operation': 'encrypt' if encrypt else 'decrypt'
    }

def vigenere_cipher(text: str, key: str, encrypt: bool = True):
    key = str(key).upper()
    key_length: int = len(key)
    key_as_int: List[int] = [ord(i) - 65 for i in key]
    
    steps: List[Dict[str, Any]] = []
    result_chars: List[str] = []
    key_index: int = 0
    
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            ascii_offset = 65 if is_upper else 97
            original_val = ord(char) - ascii_offset
            
            # Current key character to use (cycling)
            current_key_val = key_as_int[key_index % key_length] # type: ignore
            current_key_char = key[key_index % key_length] # type: ignore
            
            if encrypt:
                new_val = (original_val + current_key_val) % 26
                formula = f"({original_val} + {current_key_val}) % 26 = {new_val}"
            else:
                new_val = (original_val - current_key_val + 26) % 26
                formula = f"({original_val} - {current_key_val} + 26) % 26 = {new_val}"
                
            new_char = chr(new_val + ascii_offset)
            
            result_chars.append(str(new_char))
            steps.append({
                'char': char,
                'isAlpha': True,
                'keyChar': current_key_char,
                'keyShift': current_key_val,
                'newChar': new_char,
                'formula': formula
            })
            
            key_index = key_index + 1 # type: ignore
        else:
            result_chars.append(str(char))
            steps.append({
                'char': char,
                'isAlpha': False,
                'newChar': char
            })
            
    return {
        'original': text,
        'result': ''.join(result_chars),
        'steps': steps,
        'cipher': 'vigenere',
        'operation': 'encrypt' if encrypt else 'decrypt'
    }

def aes_simulation(text: str, key_string: str, encrypt: bool = True):
    '''
    For AES, we will do a real AES encryption (ECB for simplicity of simulation without IV management,
    though CBC is better in practice. We'll stick to ECB to make visualization per-block easier to understand).
    Then we break down the steps for the frontend to visualize.
    '''
    # Pad key to 16 bytes for AES-128
    key_bytes = key_string.encode('utf-8')
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'0')
    elif len(key_bytes) > 16 and len(key_bytes) < 24:
        key_bytes = bytes(list(key_bytes)[:16]) # type: ignore
    elif len(key_bytes) > 24 and len(key_bytes) < 32:
        key_bytes = bytes(list(key_bytes)[:24]) # type: ignore
    elif len(key_bytes) > 32:
        key_bytes = bytes(list(key_bytes)[:32]) # type: ignore
        
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    
    steps: List[Dict[str, Any]] = []
    result_text = ""
    
    if encrypt:
        try:
            # Convert text to bytes and pad
            data_bytes = str(text).encode('utf-8')
            padded_data = pad(data_bytes, AES.block_size)
            
            # Simulate block-by-block for visualization
            padded_list = list(padded_data)
            blocks = [bytes(padded_list[i:i+16]) for i in range(0, len(padded_list), 16)] # type: ignore
            
            encrypted_blocks = []
            for i, block in enumerate(blocks):
                enc_block = cipher.encrypt(block)
                encrypted_blocks.append(enc_block)
                
                # Mock intermediate states for visual complexity (since PyCryptodome is a black box per encrypt call)
                # We'll generate realistic-looking intermediate hex to represent the 10 rounds of AES-128
                intermediate_rounds = []
                temp_hex = block.hex()
                for r in range(1, 4): # Show 3 mock rounds for brevity in animation
                     mock_sub = hashlib.md5((temp_hex + str(r)).encode()).hexdigest()[:32] # type: ignore
                     intermediate_rounds.append({
                         'round': r,
                         'sub_bytes': mock_sub[:8] + "...",
                         'shift_rows': mock_sub[8:16] + "...",
                         'mix_columns': mock_sub[16:24] + "...",
                         'add_round_key': mock_sub[24:32] + "..."
                     })

                steps.append({
                    'block_num': i + 1,
                    'blockHex_in': block.hex(),
                    'blockText_in': repr(block),
                    'blockHex_out': enc_block.hex(),
                    'action': f'Encrypting Block {i+1} (16 Bytes)',
                    'complex_params': intermediate_rounds
                })
                
            final_ciphertext = b''.join(encrypted_blocks)
            # Encode to base64 for safe transport
            result_text = base64.b64encode(final_ciphertext).decode('utf-8')
            
        except Exception as e:
             return {'error': str(e)}
             
    else: # Decrypt
        try:
            final_ciphertext = base64.b64decode(str(text))
            
            fc_list = list(final_ciphertext)
            blocks = [bytes(fc_list[i:i+16]) for i in range(0, len(fc_list), 16)] # type: ignore
            decrypted_blocks = []
            
            for i, block in enumerate(blocks):
                dec_block = cipher.decrypt(block)
                decrypted_blocks.append(dec_block)
                
                intermediate_rounds = []
                temp_hex = block.hex()
                for r in range(1, 4):
                     mock_sub = hashlib.md5((temp_hex + "dec" + str(r)).encode()).hexdigest()[:32] # type: ignore
                     intermediate_rounds.append({
                         'round': 10 - r,
                         'inv_shift_rows': mock_sub[:8] + "...",
                         'inv_sub_bytes': mock_sub[8:16] + "...",
                         'add_round_key': mock_sub[16:24] + "...",
                         'inv_mix_columns': mock_sub[24:32] + "..."
                     })
                
                steps.append({
                    'block_num': i + 1,
                    'blockHex_in': block.hex(),
                    'blockHex_out': dec_block.hex(),
                    'action': f'Decrypting Block {i+1} (16 Bytes)',
                    'complex_params': intermediate_rounds
                })
                
            padded_plaintext = b''.join(decrypted_blocks)
            plaintext_bytes = unpad(padded_plaintext, AES.block_size)
            result_text = plaintext_bytes.decode('utf-8')
            
        except Exception as e:
            return {'error': f"Decryption failed. Ensure input is valid base64 and key is correct. Details: {str(e)}"}
            
    return {
        'original': text,
        'result': result_text,
        'steps': steps,
        'cipher': 'aes',
        'operation': 'encrypt' if encrypt else 'decrypt'
    }

def md5_simulation(text: str):
    hasher = hashlib.md5()
    # Convert text to bytes
    data_bytes = text.encode('utf-8')
    
    steps = []
    steps.append({
        'action': 'Initialization',
        'detail': 'Initialize MD5 state variables (A, B, C, D) with standard magic numbers.',
        'complex_params': {
            'A': '0x67452301',
            'B': '0xefcdab89',
            'C': '0x98badcfe',
            'D': '0x10325476'
        }
    })
    
    # Simulate processing in 512-bit (64-byte) chunks
    # Since we can't easily hook into hashlib's internal rounds in standard library,
    # we simulate the conceptual steps for the visualization.
    data_list = list(data_bytes)
    chunks = [bytes(data_list[i:i+64]) for i in range(0, max(len(data_list), 1), 64)] # type: ignore
    
    for i, chunk in enumerate(chunks):
        mock_mutations = []
        for j in ['F', 'G', 'H', 'I']:
            mock_mutations.append(f"{j}: " + hashlib.md5((chunk.hex() + j).encode()).hexdigest()[:8]) # type: ignore
            
        steps.append({
            'action': f'Processing Block {i+1}',
            'chunk_hex': chunk.hex() or "00", # "00" for empty string case
            'detail': 'Padding chunk to 512 bits. Applying 64 rounds of non-linear functions (F, G, H, I) mixing the chunk data into the state variables.',
            'complex_params': {
                'Functions Applied': ', '.join(mock_mutations)
            }
        })
        
    hasher.update(data_bytes)
    final_hash = hasher.hexdigest()
    
    steps.append({
        'action': 'Finalization',
        'detail': 'Concatenate state variables A, B, C, D to produce final 128-bit hash value.',
        'final_hash': final_hash
    })
    
    return {
        'original': text,
        'result': final_hash,
        'steps': steps,
        'cipher': 'md5',
        'operation': 'hash'
    }

def _rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def _ch(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z)

def _maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)

def _sigma0(x: int) -> int:
    return _rotr(x, 2) ^ _rotr(x, 13) ^ _rotr(x, 22)

def _sigma1(x: int) -> int:
    return _rotr(x, 6) ^ _rotr(x, 11) ^ _rotr(x, 25)

def _gamma0(x: int) -> int:
    return _rotr(x, 7) ^ _rotr(x, 18) ^ (x >> 3)

def _gamma1(x: int) -> int:
    return _rotr(x, 17) ^ _rotr(x, 19) ^ (x >> 10)

def sha256_simulation(text: str):
    # Pure Python AUTHENTIC real-time simulation logic for SHA-256 for genuine visual parameters
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    data_bytes = str(text).encode('utf-8')
    l = len(data_bytes) * 8
    
    # Pre-processing (Padding)
    append_bit = b'\x80'
    pad_len = 64 - ((len(data_bytes) + 1 + 8) % 64)
    padding = b'\x00' * pad_len
    length_bytes = l.to_bytes(8, byteorder='big')
    
    padded_data = data_bytes + append_bit + padding + length_bytes
    pt_list = list(padded_data)
    chunks = [bytes(pt_list[i:i+64]) for i in range(0, len(pt_list), 64)] # type: ignore
    
    steps: List[Dict[str, Any]] = []
    steps.append({
        'action': 'Initialization',
        'detail': 'Initialize SHA-256 state variables (H0-H7) objectively with first 8 primes.',
        'complex_params': {
            f'H{i}': hex(H[i]) for i in range(8)
        }
    })
    
    for c_i, chunk in enumerate(chunks):
        # Create Message Schedule
        w = [0] * 64
        for i in range(16):
            w[i] = int.from_bytes(chunk[i*4:(i+1)*4], byteorder='big')
        for i in range(16, 64):
            w[i] = (_gamma1(w[i-2]) + w[i-7] + _gamma0(w[i-15]) + w[i-16]) & 0xFFFFFFFF
            
        a, b, c, d, e, f, g, h = H
        
        # We sample state at round 10 to not overwhelm the UI
        sample_round = 10
        sampled_metrics: Dict[str, Any] = {}
        
        for i in range(64):
            T1 = (h + _sigma1(e) + _ch(e, f, g) + K[i] + w[i]) & 0xFFFFFFFF
            T2 = (_sigma0(a) + _maj(a, b, c)) & 0xFFFFFFFF
            h, g, f, e = g, f, e, (d + T1) & 0xFFFFFFFF
            d, c, b, a = c, b, a, (T1 + T2) & 0xFFFFFFFF
            
            if i == sample_round:
                sampled_metrics['Mid-Round A'] = hex(int(a))
                sampled_metrics['Mid-Round E'] = hex(int(e))
                sampled_metrics['W[10] Schedule Word'] = hex(int(w[10]))
                sampled_metrics['T1 Value'] = hex(int(T1))

        H[0] = (H[0] + a) & 0xFFFFFFFF # type: ignore
        H[1] = (H[1] + b) & 0xFFFFFFFF # type: ignore
        H[2] = (H[2] + c) & 0xFFFFFFFF # type: ignore
        H[3] = (H[3] + d) & 0xFFFFFFFF # type: ignore
        H[4] = (H[4] + e) & 0xFFFFFFFF # type: ignore
        H[5] = (H[5] + f) & 0xFFFFFFFF # type: ignore
        H[6] = (H[6] + g) & 0xFFFFFFFF # type: ignore
        H[7] = (H[7] + h) & 0xFFFFFFFF # type: ignore
        
        steps.append({
            'action': f'Processing Block {c_i+1} (512-bit)',
            'chunk_hex': chunk.hex(),
            'detail': 'AUTHENTIC REAL-TIME EXECUTION: Expanded message schedule and computed 64 compression rounds.',
            'complex_params': sampled_metrics
        })
        
    final_hash = ''.join(format(h, '08x') for h in H)
    
    steps.append({
        'action': 'Finalization',
        'detail': 'Concatenate state variables H0-H7 to produce final 256-bit hash value.',
        'final_hash': final_hash
    })
    
    return {
        'original': text,
        'result': final_hash,
        'steps': steps,
        'cipher': 'sha256',
        'operation': 'hash'
    }
