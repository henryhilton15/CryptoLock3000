import sys, getopt
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Padding


keystring = ''
password = ''

try:
    opts, args = getopt.getopt(sys.argv[1:],'hk:p:')
except getopt.GetoptError:
    print('Usage: key_cbc_enc.py -k <keystring> -p <password>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('Usage: key_cbc_enc.py -k <keystring> -p <password>')
        sys.exit()
    elif opt == '-k':
        keystring = arg
    elif opt == '-p':
        password = arg


def cbc_encrypt(keystring, password):    
    if len(keystring) != 16:
        print('Error: Keystring must be 16 bytes')

    if len(password) == 0:
        print('Error: Password is missing.')
        sys.exit(2)

    # encryption
    print('Encrypting...', end='')

    # generate a random IV and encrypt it in ECB mode
    iv = Random.get_random_bytes(AES.block_size)
    key = keystring.encode('utf-8')
    cipher_ECB = AES.new(key, AES.MODE_ECB)
    enc_iv = cipher_ECB.encrypt(iv)

    # create an AES-CBC cipher object
    cipher_CBC = AES.new(key, AES.MODE_CBC, iv)

    # add padding
    padded_password = Padding.pad(password.encode('utf-8'), AES.block_size)

    # encrypt the plaintext
    encrypted_password = cipher_CBC.encrypt(padded_password)
	
    encrypted = enc_iv + encrypted_password

    print('Done')

    print(encrypted)
    return encrypted

cbc_encrypt(keystring, password)

