import hashlib
import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def random_hash():
    input_string = generate_random_string(16)  # Tạo một chuỗi ngẫu nhiên có độ dài 16 ký tự
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    return md5_hash

class Hasher:
    def __init__(self):
        self._hash = hashlib.sha1()
    
    def update(self, data):
        self._hash.update(data)
    
    def digest(self):
        return self._hash.digest()

def sha1(data):
    hasher = Hasher()
    hasher.update(data)
    return hasher.digest()

def hmac_sha1(key, data):
    key_bytes = key.encode('utf-8') if isinstance(key, str) else key
    data_bytes = data.encode('utf-8') if isinstance(data, str) else data
    block_size = 64

    if len(key_bytes) > block_size:
        key_bytes = sha1(key_bytes)
    
    if len(key_bytes) < block_size:
        key_bytes = key_bytes.ljust(block_size, b'\x00')

    ipad = bytes((x ^ 0x36) for x in key_bytes)
    opad = bytes((x ^ 0x5C) for x in key_bytes)

    inner_hash = sha1(ipad + data_bytes)
    result = sha1(opad + inner_hash)

    return result.hex()
def hmac_sha11(key, message):
    # Block size for HMAC-SHA1 is 64 bytes
    block_size = 64

    # If the key is longer than block_size, hash the key
    if len(key) > block_size:
        key = hashlib.sha1(key).digest()
    # If the key is shorter than block_size, pad with zeros
    elif len(key) < block_size:
        key = key.ljust(block_size, b'\x00')

    # Inner and outer padding
    inner_padding = bytes((x ^ 0x36) for x in key)
    outer_padding = bytes((x ^ 0x5C) for x in key)

    # Calculate inner hash
    inner_hash = hashlib.sha1(inner_padding + message).digest()
    # Calculate final hash
    final_hash = hashlib.sha1(outer_padding + inner_hash).hexdigest()

    return final_hash
if __name__ == '__main__':
    key = "minhduchan323"
    message = "minhduchan3"
    result = hmac_sha1(key, message)
    print("HMAC-SHA-1:", result)
    key = b"minhduchan323"
    message = b"minhduchan3"
    result = hmac_sha11(key, message)
    print("HMAC-SHA-1:", result)