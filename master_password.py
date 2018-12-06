import sys, getopt
import random
from Crypto.Protocol.KDF import PBKDF2
from PasswordHandler import *


#First decision is whether the user is creating a master password, adding a new password, or getting a password

operation = "create"
logininfofile = "infofile.txt"
KEY_CREATED = "Hash of master key:"
loginInfoObjects = []

try:
    opts, args = getopt.getopt(sys.argv[1:],'hcag')
except getopt.GetoptError:
    print("Usage: master_password.py [-c|-a|-g] -m <masterpassword> -u <username/URL>")
    sys.exit(2)

try:
	init_login_objects()
except FileNotFoundError:
	pass

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
	try:
		infofile = open(logininfofile, 'rb')
	# if infofile.readline() contains some word that lets us know password has been created
		firstline = infofile.readline()
		infofile.close()
	except FileNotFoundError:
		infofile = open(logininfofile, 'wb')
		infofile.close()
		firstline = "".encode('utf-8')

	#print(firstline)

	if (KEY_CREATED.encode('utf-8') in firstline):
		print("Master password has already been created. Type 'a' to add a password or 'g' to get a password.")
		switchoperation = ""
		switchoperation = input()
		while (switchoperation != "a") and (switchoperation != "g"):
			print("Error! Choose to add or get a password (a/g)")
			switchoperation = input()
		if switchoperation == "a":
			operation = "add"
		if switchoperation == "g":
			operation = "get"
	else:
		print("Create master password by entering it now.\nMaster password must be at least 8 chars long, contain an upper case letter, a lower case letter, and a digit")

		masterpassword = validate_pw()
		key_to_store = store_master_password(masterpassword)
		masterpassword = None

		infofile = open(logininfofile, 'wb')
		infofile.write(KEY_CREATED.encode('utf-8') + key_to_store + "\n".encode('utf-8'))
		infofile.close()
		key_to_store = None



if (operation == "add"):
	inputmpw = ""
	print("Enter master password.")
	inputmpw = input()
	login_attempts = 1
	while(verify_inputmpw(inputmpw) != 1 and login_attempts < 5):
		print("Incorrect master password entered. Try again.")
		inputmpw = input()
		login_attempts += 1
	if verify_inputmpw(inputmpw) == 1:
		print("here")
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

			masterkey = generate_master_key(inputmpw)
			newLogin = LoginInfo(username, URL, cbc_encrypt(masterkey, password))
			masterkey = None

			update_login_file(newLogin)

			print("Done")

		elif mode == "n":
			print("Enter username")
			username = input()
			print("Enter URL")
			URL = input()
			password = random_pw_gen()
			print("Password generated.")

			masterkey = generate_master_key(inputmpw)
			newLogin = LoginInfo(username, URL, cbc_encrypt(masterkey, password))
			masterkey = None

			update_login_file(newLogin)

	else:
		print("Too many incorrect guesses!")



if (operation == "get"):
	inputmpw = ""
	print("Enter master password.")
	inputmpw = input()
	login_attempts = 1
	while(verify_inputmpw(inputmpw) != 1 and login_attempts < 5):
		print("Incorrect master password entered. Try again.")
		inputmpw = input()
		login_attempts += 1
	if verify_inputmpw(inputmpw) == 1:
		mode = "url"
		print("Enter 'url' to look up accounts by URL. Enter 'user' to look up accounts by username.")
		mode = input()
		while (mode != "url") and (mode != "user"):
			print("Enter url/user")
			mode = input()
		if mode == "url":
			URL = ""
			print("Enter URL associated with password")
			URL = input()
			matchingURL = lookup_url(URL)
			print("Enter one of the above usernames to get its password")
			desiredUser = input()
			for loginInfo in matchingURL:
				if loginInfo.username[2:-1] == desiredUser:
					encrypted_password = loginInfo.password
					masterkey = generate_master_key(inputmpw)
					decrypted_password = cbc_decrypt(masterkey, encrypted_password)
					masterkey = None
					print("Test")
					print(decrypted_password)
		if mode == "user":
			username = ""
			print("Enter username associated with password")
			username = input()
			matchingUser = lookup_username(username)
			print("Enter one of the above URLs to get its password")
			desiredURL = input()
			for loginInfo in matchingUser:
				if loginInfo.url[2:-1] == desiredURL:
					encrypted_password = loginInfo.password
					masterkey = generate_master_key(inputmpw)
					decrypted_password = cbc_decrypt(masterkey, encrypted_password)
					masterkey = None
					print("Test")
					print(decrypted_password)
	else:
		print("Too many incorrect guesses!")
