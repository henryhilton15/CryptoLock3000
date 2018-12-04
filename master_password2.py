import sys, getopt
import random
from Crypto.Protocol.KDF import PBKDF2
from PasswordHandler import *

#First decision is whether the user is creating a master password, adding a new password, or getting a password

masterpassword = ""
operation = "create"
logininfofile = "infofile.bin"
KEY_CREATED = "Hash of master key: "
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
	try:
		infofile = open(logininfofile, 'rb')
	# if infofile.readline() contains some word that lets us know password has been created
		firstline = infofile.readline()
		infofile.close()
	except FileNotFoundError:
		infofile = open(logininfofile, 'wb')
		infofile.close()

	#print(firstline)

	if (KEY_CREATED.encode('utf-8') in firstline):
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
		#masterpassword = input()
		masterpassword = validate_pw()
		# create a random salt

		# generate master key using PBKDF2 with masterpassword and salt

		# store the hash of the master key in the first line of the file
		# store the salt (unencrypted) in the second line of the file
		# as of now, store_master_password writes hashed master key and salt in first line together
		key_to_store = store_master_password(masterpassword)
		infofile = open(logininfofile, 'wb')
		infofile.write(KEY_CREATED.encode('utf-8'))
		infofile.write(key_to_store) # + some form of masterpassword# +'\b')
		infofile.close()



if (operation == "add"):
	inputmpw = ""
	print("Enter master password")
	inputmpw = input()
	if verify_inputmpw(inputmpw) == 1:
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
			newLogin = (username, URL, cbc_encrypt(get_master_key(), password))
			infofile = open(logininfofile, 'w')
			infofile.write("\n" + format_loginInfo(newLogin))
			infofile.close()
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
			infofile.close()


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
					cbc_decrypt(get_master_key(), encrypted_password)
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
					cbc_decrypt(get_master_key(), encrypted_password)
