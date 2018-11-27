import sys, getopt
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Padding

master = ''
encrypted = ''

try:
    opts, args = getopt.getopt(sys.argv[1:],'hm:e:')
except getopt.GetoptError:
    print('Usage: key_cbc_dec.py -m <master> -e <encrypted>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('Usage: key_cbc_dec.py -m <master> -e <encrypted>')
        sys.exit()
    elif opt == '-m':
        master = arg
    elif opt == '-e':
        encrypted = arg

    
if len(master) == 0:
    print('Error: Enter master password')
    sys.exit(2)

if len(encrypted) == 0:
    print('Error: No password to decrypt')
    sys.exit(2)
	
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

