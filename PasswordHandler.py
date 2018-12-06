import sys, getopt
import random
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random
from PasswordHandler import *
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding

logininfofile = "infofile.txt"
loginInfoObjects = []

class LoginInfo:
	def __init__(self, username, url, password):
		self.username = str(username)
		self.url = str(url)
		#self.password = str(password)
		self.password = password

	def toString():
		return "Username: " + self.username + " | URL: " + self.url


def validate_pw():
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
	if pwvalid == 1:
		print("Master password created")
		return attemptedpw


def random_pw_gen():
	s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
	pwlen = 16
	randompw = "".join(random.sample(s,pwlen))
	return randompw


SEPARATOR = b"|||"

def format_loginInfo(loginInfo):
	return loginInfo.username.encode('utf-8') + SEPARATOR + loginInfo.url.encode('utf-8') + SEPARATOR + loginInfo.password.encode('utf-8')

def parse_line(entry):
	first_sep = entry.find(SEPARATOR, 0, len(entry) - 1)
	second_sep = entry.find(SEPARATOR, first_sep + 3, len(entry) - 1)
	username = entry[:first_sep]
	url = entry[first_sep + 3 : second_sep]
	password = entry[second_sep + 3 : len(entry) - 1]
	newLogin = LoginInfo(username, url, password)
	return newLogin


def init_login_objects():

	loginInfoFile = open(logininfofile, 'rb')
	loginInfoFile.readline()
	for line in loginInfoFile:
		loginInfo = parse_line(line)
		loginInfoObjects.append(loginInfo)
		print("Retrieved password: ")
		print(loginInfo.password)
		print("Retrieved username: ")
		print(loginInfo.username)

def update_login_file(newLogin):
	loginInfoObjects.append(newLogin)

	print("Password stored:")
	print(newLogin.password)
	print("Username stored:")
	print(newLogin.username)

	infofile = open(logininfofile, 'ab')
	infofile.write(format_loginInfo(newLogin) + b"\n")
	infofile.close()


def cbc_encrypt(key, password):    

    if len(key) != 16:
        print('Error: Key must be 16 bytes')
        sys.exit(2)

    if len(password) == 0:
        print('Error: Password is missing.')
        sys.exit(2)

    # generate a random IV and encrypt it in ECB mode
    iv = Random.get_random_bytes(AES.block_size)
    #key = keystring.encode('utf-8')
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


def cbc_decrypt(key, encrypted):
    
    if len(key) == 0:
        print('Error: Enter key')
        sys.exit(2)

    if len(encrypted) == 0:
        print('Error: No password to decrypt')
        sys.exit(2)


    enc_iv = encrypted[:AES.block_size]
    #print(enc_iv.encode('utf-8')) #remove later
    #print("Is enc_iv.encode('utf-8') (above) a string?") #remove later
    #print(isinstance(enc_iv.encode('utf-8'), str)) #remove later
    #print(enc_iv) #remove later
    #print("Is enc_iv (above) a string?") #remove later
    #print(isinstance(enc_iv, str)) #remove later
    encrypted_password = encrypted[AES.block_size:]
	
    # decrypt iv using AES_ECB
    #key = keystring.encode('utf-8')
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

def lookup_url2(url):
	matching_url_list = []
	userString = ""
	for loginInfo in loginInfoObjects:
		if loginInfo.url[2:-1] == url:
			matching_url_list.append(loginInfo)
			userString += loginInfo.username[2:-1] + "  "
	print (userString)
	return matching_url_list


def lookup_username(username):
	matching_login_list = []
	for loginInfo in loginInfoObjects:
		if loginInfo.username == username:
			matching_login_list.append(loginInfo)

	return matching_login_list

def lookup_username2(username):
	#print("Input username is string?")
	#print(isinstance(username, str))
	#print("Input username encoded is string?")
	#print(isinstance(username.encode('utf-8'), str))
	#print (username.encode('utf-8')) # remove later
	matching_user_list = []
	URLString = ""
	#userString = ""
	for loginInfo in loginInfoObjects:
		#print (loginInfo.username[2:-1]) #remove later
		#print ("Above is string?")
		#print(isinstance(loginInfo.username, str))
		#if loginInfo.username.decode('utf-8') == username:
		#if loginInfo.username.encode('utf-8') == username:
		#if loginInfo.username.encode('utf-8') == username.encode('utf-8'):
		#if loginInfo.username == username.encode('utf-8'): #PROBLEM is here. LHS byte string is never equal to RHS byte string
		if loginInfo.username[2:-1] == username: #for some reason the fields of loginInfo objects are being treated as strings in the format b'string' where the b and ' ' are part of the string
		#if loginInfo.username.equal(username.encode('utf-8')):
			matching_user_list.append(loginInfo)
			URLString += loginInfo.url[2:-1] + "  "
		#userString += loginInfo.username + "  "
	print (URLString)
	#print(userString)

	return matching_user_list

def store_master_password(masterpassword):
	#find a more secure way to do this!
	salt = Random.get_random_bytes(16)
	generated_key = PBKDF2(masterpassword, salt, AES.block_size, 1000)
	h = SHA256.new()
	h.update(generated_key)
	key_to_store = h.digest()
	key_to_store = key_to_store + salt
	return key_to_store

def generate_master_key(masterpassword):
	salt = get_salt()
	masterkey = PBKDF2(masterpassword, salt, AES.block_size, 1000)
	return masterkey


def verify_inputmpw(inputmpw):
	salt = get_salt()
	input_key = PBKDF2(inputmpw, salt, AES.block_size, 1000)
	h = SHA256.new()
	h.update(input_key)
	input_key_hash = h.digest()
	masterkey_hash = get_master_key_hash()

	if input_key_hash == masterkey_hash:
		return True
	else:
		return False

def get_salt():
	infofile = open(logininfofile, 'rb')
	firstline = infofile.readline()
	infofile.close()
	salt = firstline[-17:-1]
	return salt

def get_master_key_hash():
	infofile = open(logininfofile, 'rb')
	firstline = infofile.readline()
	masterkey_hash = firstline[firstline.find(':'.encode('utf-8'))+1:firstline.find(':'.encode('utf-8'))+1+32]
	infofile.close()
	return masterkey_hash