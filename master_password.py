import sys, getopt
from Crypto.Protocol.KDF import PBKDF2

#First decision is whether the user is creating a master password, adding a new password, or getting a password

masterpassword = ""
operation = "create"

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
	print("Create master password by entering it now.\nMaster password must be at least 10 chars long, contain an upper case letter, a lower case letter, a number, and a special character (!,@,#,$).")
	masterpassword = input()
	#check conditions on masterpassword
	# if (masterpassword doesn't meet above conditions):
	# print ("Error! Master password must be at least 10 chars long, contain an upper case letter, a lower case letter, a number, and a special character (!,@,#,$).")


if (operation == "add"):
	mode = "e"
	print("Adding new password:")
	print("Enter 'e' to add a password for an existing account. Enter 'n' to generate a password for a new account.")
	mode = input()
	if (mode != "e") and (mode != "n"):
		print("Error! Enter e/n")
	elif mode == "e":
		print("Enter password to be encrypted")
		encpw = input()
		print("Enter username/URL associated with password")
		username = input()






