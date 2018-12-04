

class LoginInfo:
	def __init__(self, username, url, password):
		self.username = str(username)
		self.url = str(url)
		self.password = str(password)

	def toString():
		return "Username: " + self.username + " | URL: " + self.url


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
	salt = Random.get_random_bytes(16) #changed salt from 8 to 16 bytes for more security
	generated_key = PBKDF2(masterpassword, salt, AES.block_size, 1000)
	h = SHA256.new()
	h.update(generated_key)
	key_to_store = h.digest()
	key_to_store = key_to_store + salt
	infofile = open(logininfofile, 'w')
	infofile.write(KEY_CREATED + key_to_store) # + some form of masterpassword# +'\b')
	infofile.close()

def verify_inputmpw(inputmpw):
	salt = get_salt()
	input_key = PBKDF2(inputmpw, salt, AES.block_size, 1000)
	h = SHA256.new()
	h.update(input_key)
	input_key = h.digest()
	masterkey = get_master_key()
	if inputkey == masterkey:
		return 1
	else:
		return 0

def get_salt():
	infofile = open(logininfofile, 'r')
	firstline = infofile.readline()
	salt = firstline[-16:]
	return salt

def get_master_key():
	infofile = open(logininfofile, 'r')
	firstline = infofile.readline()
	masterkey = firstline[firstline.find(' ')+1:firstline.find(' ')+1+AES.block_size]
	return masterkey