from keyauth import api
import hashlib
import sys
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import  unpad
import base64
def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest
def decryptvalue(password, base64v):
    salt = bytes("0000000000000000", 'utf-8')  
    iterations = 256 
    key_length = 32   
    iv = bytes.fromhex('010110101010020103000100030004F0')
    key = PBKDF2(password, salt, dkLen=key_length, count=iterations)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    encrypted_data = base64.b64decode(base64v)
    decrypted_padded = cipher.decrypt(encrypted_data)
    decrypted = unpad(decrypted_padded, AES.block_size)

    return decrypted.decode()  
def checkauth(key):
    secretvaluebase64="156855"#
    namevaluebase64="256855"#
    owneridvaluebase64="356855"#
    pt=decryptvalue(key,secretvaluebase64)
    name=decryptvalue(key,namevaluebase64)
    ownerid=decryptvalue(key,owneridvaluebase64)
    print(pt)
    print(name)
    print(ownerid)
    keyauthapp = api(
        name = name,
        ownerid = ownerid,
        secret = pt,
        version = "1.0",
        hash_to_check = getchecksum()
    )
    mkey="KEYAUTH-"+key
    print(mkey)
    ret=keyauthapp.license(mkey)
    return  ret