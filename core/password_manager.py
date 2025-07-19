import json
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter
import base64
import secrets
import string

class PasswordManager:
    def __init__(self,file_path='storage/password.json',key_file='storage/key.key'):
        self.file_path=file_path
        self.key_file=key_file
        self.key=self.load_or_create_key()

    def load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file,'rb')as f:
                if f.read():
                    return f.read()
                else:
                    key=get_random_bytes(16)
                    with open(self.key_file,'wb')as f:
                        f.write(key)
                    return key
        else:
            key=get_random_bytes(16)
            with open(self.key_file,'wb')as f:
                f.write(key)
            return key        
    
    def encrypt(self,data:str):
        cipher=AES.new(self.key,AES.MODE_CBC)
        ct_bytes=cipher.encrypt(pad(data.encode('utf-8'),AES.block_size))
        iv=base64.b64encode(cipher.iv).decode('utf-8')
        ct=base64.b64encode(ct_bytes).decode('utf-8')
        return iv,ct
    
    def decrypt(self,iv,ct):
        iv=base64.b64decode(iv)
        ct=base64.b64decode(ct)
        cipher=AES.new(self.key,AES.MODE_CBC,iv)
        pt=unpad(cipher.decrypt(ct),AES.block_size)
        return pt.decode('utf-8')
    
    def save_password(self,account:str,password:str):
        try:
            with open(self.file_path,'r')as f:
                data=json.load(f)
        except FileNotFoundError:
            data={}

        iv,encrypted_password=self.encrypt(password)
        data[account]={'iv':iv,'password':encrypted_password}

        with open(self.file_path,'w')as f:
            json.dump(data,f,indent=4)

    def get_password(self,account:str):
        try:
            with open(self.file_path,'r')as f:
                data=json.load(f)
        except FileNotFoundError:
            return None
        
        if account in data:
            entry=data[account]
            return self.decrypt(entry['iv'],entry['password'])
        else:
            return None
        
    def generate_password(self,length=12):
        characters=string.ascii_letters+string.digits+string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))
