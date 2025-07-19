import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad

def encrypt_data(key:bytes,data:str)->dict:
    """
    使用 AES-CBC 模式加密数据
    
    Args:
        key (bytes): 16字节的加密密钥
        data (str): 要加密的原始数据
    
    Returns:
        dict: 包含 IV 和密文的字典
    """  
    cipher =AES.new(key,AES.MODE_CBC)
    ct_bytes=cipher.encrypt(pad(data.encode('utf-8'),AES.block_size))

    return{
        'iv':base64.b64encode(cipher.iv).decode('utf-8'),
        'ciphertext':base64.b64encode(ct_bytes).decode('utf-8')
    }  

def decrypt_data(key:bytes,iv:str,ciphertext:str)->str:
    """
    使用 AES-CBC 模式解密数据
    
    Args:
        key (bytes): 16字节的加密密钥
        iv (str): 初始化向量(Base64编码)
        ciphertext (str): 密文(Base64编码)
    
    Returns:
        str: 解密后的原始数据
    """
    iv_data=base64.b64decode(iv)
    ct_data=base64.b64decode(ciphertext)

    cipher =AES.new(key,AES.MODE_CBC,iv=iv_data)
    pt=cipher.decrypt(ct_data)

    return unpad(pt,AES.block_size).decode('utf-8')

def generate_key()->bytes:
    """
    生成 128 位(16 字节)的随机密钥
    
    Returns:
        bytes: 随机生成的密钥
    """
    return get_random_bytes(16)
