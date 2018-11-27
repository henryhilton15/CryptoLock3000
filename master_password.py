import sys, getopt
import random
from Crypto.Protocol.KDF import PBKDF2

#First decision is whether the user is creating a master password, adding a new password, or getting a password

masterpassword = ""
operation = "create"
logininfofile = "infofile.txt"

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
	if (master password has already been created):
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


if (operation == "add"):
	inputmpw = ""
	print("Enter master password")
	inputmpw = input()
	#if (inputmpw == masterpassword):
	if (inputmpw == )
		mode = "e"
		password = ""
		username = ""
		URL = ""
		print("Adding new password:")
		print("Enter 'e' to add a password for an existing account. Enter 'n' to generate a password for a new account.")
		mode = input()
		if (mode != "e") and (mode != "n"):
			print("Error! Enter e/n")
		elif mode == "e":
			print("Enter password to be encrypted")
			password = input()
			print("Enter username associated with password")
			username = input()
			print("Enter URL associated with password")
			URL = input()
		elif mode == "n":
			print("Enter username")
			username = input()
			print("Enter URL")
			URL = input()
			password = random_pw_gen()
			print("Password generated.")


if (operation == "get"):
	inputmpw = ""
	print("Enter master password")
	inputmpw = input()
	if (inputmpw == masterpassword):
		username = ""
		print("Enter username/URL associated with password")
		username = input()


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





