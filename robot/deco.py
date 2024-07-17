import base64
from Crypto.Cipher import ARC4
def rptges( bencrypted_data):
    key = b"2(8jk)sg" 
    encrypted_data = base64.b64decode(bencrypted_data)
    cipher = ARC4.new(key) 
    return cipher.decrypt(encrypted_data).decode('utf-8')  # 将bytes结果转化为字符串
