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
    
if len(keystring) == 0:
    print('Error: Please enter a the keystring')

if len(password) == 0:
    print('Error: Password is missing.')
    sys.exit(2)

# encryption
if operation == 'enc': 
    print('Encrypting...', end='')
	
    # read the content of the input file into a variable
    ifile = open(inputfile, 'r')
    plaintext = ifile.read()
    plaintext_bytes = plaintext.encode('utf-8')
    ifile.close()
    # generate a random IV and encrypt it in ECB mode
    iv = Random.get_random_bytes(AES.block_size)
    key = keystring.encode('utf-8')
    cipher_ECB = AES.new(key, AES.MODE_ECB)
    enc_iv = cipher_ECB.encrypt(iv)

    # create an AES-CBC cipher object
    cipher_CBC = AES.new(key, AES.MODE_CBC, iv)

    # add padding
    padded_plaintext = Padding.pad(plaintext.encode('utf-8'), AES.block_size)

    # encrypt the plaintext
    ciphertext = cipher_CBC.encrypt(padded_plaintext)
	
    # write the random nonce and the ciphertext into the output file
    ofile = open(outputfile, 'wb')
    ofile.write(enc_iv+ciphertext)
    ofile.close()

	
# decryption
else:
    print('Decrypting...', end='')

    # read the padded iv and the padded ciphertext from the input file
    ifile = open(inputfile, 'rb')
    ciphertext = ifile.read()
    ifile.close()

    enc_iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
	
    # decrypt iv using AES_ECB
    key = keystring.encode('utf-8')
    cipher_ECB = AES.new(key, AES.MODE_ECB)
    iv = cipher_ECB.decrypt(enc_iv)

    # create AES-CBC cipher object
    cipher_CBC = AES.new(key, AES.MODE_CBC, iv)

    # decrypt ciphertext
    padded_plaintext = cipher_CBC.decrypt(ciphertext)
    plaintext = Padding.unpad(padded_plaintext, AES.block_size)
    plaintext = plaintext.decode('utf-8')
	
    # write out the plaintext obtained into the output file
    ofile = open(outputfile, 'w')
    ofile.write(plaintext)
    ofile.close()

print('Done.')

