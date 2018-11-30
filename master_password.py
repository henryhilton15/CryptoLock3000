import sys, getopt
import random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

#First decision is whether the user is creating a master password, adding a new password, or getting a password

masterpassword = ""
operation = "create"
logininfofile = "infofile.txt"
KEY_CREATED = "Hash of master key:"
loginInfoObjects = []

try:
    opts, args = getopt.getopt(sys.argv[1:],'hcag')
except getopt.GetoptError:
    print("Usage: master_password.py [-c|-a|-g] -m <masterpassword> -u <username/URL>")
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print("Usage: master_password.py [-c|-a|-g] -p <password> -u <username/URL>")
        sys.exit()
    elif opt == '-c':
        operation = "create"
    elif opt == '-a':
        operation = "add"
    elif opt == '-g':
    	operation = "get"

if (operation != "create") and (operation != "add") and (operation != "get"):
    print('Error: Operation must be -c (for create) or -a (for add) or -g (for get).')
    sys.exit(2)

if (operation == "create"):
	# check to see if a master password has already been created
	# if (master password has already been created):
	infofile = open(logininfofile, 'r')
	# if infofile.readline() contains some word that lets us know password has been created
	firstline = infofile.readline()
	infofile.close()
	if (KEY_CREATED in firstline):
		print("Error! Master password has already been created. Type 'a' to add a password or 'g' to get a password.")
		switchoperation = ""
		switchoperation = input()
		while (switchoperation != "a") and (switchoperation != "g"):
			print("Error! Choose to add or get a password (a/g)")
		if switchoperation == "a":
			operation = "add"
		if switchoperation == "g":
			operation = "get"
	else:
		print("Create master password by entering it now.\nMaster password must be at least 8 chars long, contain an upper case letter, a lower case letter, and a digit")
		masterpassword = input()
		validate_pw(masterpassword)
		store_master_password(masterpassword)




if (operation == "add"):
	inputmpw = ""
	print("Enter master password")
	inputmpw = input()
	if (inputmpw == masterkey): #need to have some way of going from input master password to the correct master key
		mode = "e"
		password = ""
		username = ""
		URL = ""
		print("Adding new password:")
		print("Enter 'e' to add a password for an existing account. Enter 'n' to generate a password for a new account.")
		mode = input()
		while (mode != "e") and (mode != "n"):
			print("Error! Enter e/n")
			mode = input()
		if mode == "e":
			print("Enter password to be encrypted")
			password = input()
			print("Enter username associated with password")
			username = input()
			print("Enter URL associated with password")
			URL = input()
			newLogin = (username, URL, cbc_encrypt(masterkey, password))
			infofile = open(logininfofile, 'w')
			infofile.write("\n" + format_loginInfo(newLogin))
		elif mode == "n":
			print("Enter username")
			username = input()
			print("Enter URL")
			URL = input()
			password = random_pw_gen()
			print("Password generated.")
			newLogin = (username, URL, cbc_encrypt(masterkey, password))
			infofile = open(logininfofile, 'w')
			infofile.write("\n" + format_loginInfo(newLogin))


if (operation == "get"):
	inputmpw = ""
	print("Enter master password")
	inputmpw = input()
	if (inputmpw == masterkey):
		mode = "url"
		print("Enter 'url' to look up accounts by URL. Enter 'user' to look up accounts by username.")
		mode = input()
		while (mode != "url") and (mode != "user"):
			print("Error! Enter url/user")
			mode = input()
		if mode == "url":
			URL = ""
			print("Enter URL associated with password")
			URL = input()
			matchingURL = lookup_url(URL)
			usernamesString = ""
			for loginInfo in matchingURL:
				usernamesString += loginInfo.username + "  "
			print(usernamesString)
			print("Enter one of the above usernames to get its password")
			desiredUsername = input()
			for loginInfo in matchingURL:
				if loginInfo.username == desiredUsername:
					encrypted_password = loginInfo.password
					return cbc_decrypt(masterkey, encrypted_password)
		if mode == "user":
			username = ""
			print("Enter username associated with password")
			username = input()
			matchingUser = lookup_user(username)
			URLString = ""
			for loginInfo in matchingUser:
				URLString += loginInfo.url + "  "
			print(URLString)
			print("Enter one of the above URLs to get its password")
			desiredURL = input()
			for loginInfo in matchingUser:
				if loginInfo.url == desiredURL:
					encrypted_password = loginInfo.password
					return cbc_decrypt(masterkey, encrypted_password)


def validate_pw(attemptedpw):
	pwvalid = 0
	while pwvalid == 0:
		attemptedpw = input()
		if (len(attemptedpw) >= 8) and (any(x.isupper() for x in attemptedpw)) and (any(x.islower() for x in attemptedpw)) and any(x.isdigit() for x in attemptedpw):
			pwvalid = 1
		else:
			if len(attemptedpw) < 8:
				print("Error! Password must be at least 8 chars.")
			if not any(x.isupper() for x in attemptedpw):
				print("Error! Password must contain an upper case letter.")
			if not any(x.islower() for x in attemptedpw):
				print("Error! Password must contain a lower case letter.")
			if not any(x.isdigit() for x in attemptedpw):
				print("Error! Password must contain a digit.")
	if pwvalid:
		print("Master password created")


def random_pw_gen():
	s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
	pwlen = 16
	randompw = "".join(random.sample(s,pwlen))
	return randompw


SEPARATOR = "|||"

def format_loginInfo(loginInfo):
	return loginInfo.username + SEPARATOR + loginInfo.url + SEPARATOR + loginInfo.password

def parse_line(entry):
	first_sep = entry.find(SEPARATOR, 0, len(entry) - 1)
	second_sep = entry.find(SEPARATOR, first_sep + 3, len(entry) - 1)
	username = entry[:first_sep]
	url = entry[first_sep + 3 : second_sep]
	password = entry[second_sep + 3 : len(entry) - 1]
	newLogin = LoginInfo(username, url, password)
	return newLogin

class LoginInfo:
	def __init__(self, username, url, password):
		self.username = str(username)
		self.url = str(url)
		self.password = str(password)

	def toString():
		return "Username: " + self.username + " | URL: " + self.url


def init_login_objects():
	for line in loginInfoFile:
		loginInfo = parse_line(line)
		loginInfoObjects.append(loginInfo)

def update_login_file():
	ofile = open(loginInfoFile, "w")
	for loginInfo in loginInfoObjects:
		line = format_loginInfo(loginInfo)
		ofile.write(line)
	ofile.close()


def cbc_encrypt(keystring, password):    

    if len(keystring) != 16:
        print('Error: Keystring must be 16 bytes')

    if len(password) == 0:
        print('Error: Password is missing.')
        sys.exit(2)

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

    return encrypted


def cbc_decrypt(keystring, encrypted):
    
    if len(keystring) == 0:
        print('Error: Enter keystring')
        sys.exit(2)

    if len(encrypted) == 0:
        print('Error: No password to decrypt')
        sys.exit(2)


    enc_iv = encrypted[:AES.block_size]
    encrypted_password = encrypted[AES.block_size:]
	
    # decrypt iv using AES_ECB
    key = keystring.encode('utf-8')
    cipher_ECB = AES.new(key, AES.MODE_ECB)
    iv = cipher_ECB.decrypt(enc_iv)

    # create AES-CBC cipher object
    cipher_CBC = AES.new(key, AES.MODE_CBC, iv)

    # decrypt ciphertext
    padded_password = cipher_CBC.decrypt(encrypted_password)
    password = Padding.unpad(padded_password, AES.block_size)
    password = password.decode('utf-8')
	
    return password


def lookup_url(url):
	matching_login_list = []
	for loginInfo in loginInfoObjects:
		if loginInfo.url == url:
			matching_login_list.append(loginInfo)

	return matching_login_list

def lookup_username(username):
	matching_login_list = []
	for loginInfo in loginInfoObjects:
		if loginInfo.username == username:
			matching_login_list.append(loginInfo)

	return matching_login_list

def store_master_password(masterpassword):
	#find a more secure way to do this!
	salt = Random.get_random_bytes(8)
	generated_key = PBKDF2(masterpassword, salt, AES.block_size, 1000)
	h = SHA256.new()
	h.update(generated_key)
	key_to_store = h.digest()
	key_to_store = key_to_store + salt
	infofile = open(logininfofile, 'w')
	infofile.write(KEY_CREATED + key_to_store) # + some form of masterpassword# +'\b')
	infofile.close()







