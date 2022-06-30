from Crypto.Cipher import AES
import json

key = b'agrOjAsON_PrOJect_greeN '

def my_encode(data):
    global key
    data = data.encode()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    msg = json.dumps({'ciphertext': ciphertext.hex(), 'tag': tag.hex(), 'nonce': nonce.hex()})
    return msg.encode()

def my_decode(msg):
    global key
    msg = msg.decode()
    ciphertext = bytes.fromhex(json.loads(msg)['ciphertext'])
    tag = bytes.fromhex(json.loads(msg)['tag'])
    nonce = bytes.fromhex(json.loads(msg)['nonce'])
    cipher2 = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher2.decrypt(ciphertext)
    try:
        cipher2.verify(tag)
        return plaintext.decode()
    except ValueError:
        return None