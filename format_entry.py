
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
