import requests
from lxml import html

USERNAME = "ssrikanth77@gmail.com"
PASSWORD = "kaju2007"

LOGIN_URL = "https://www.yokibu.com/signin?ut=pt/"
URL = "https://www.yokibu.com/home"

def main():

	print('Starting login process ...')
	session_requests = requests.session()

	# Create payload
	payload = {
	    "username": USERNAME, 
	    "password": PASSWORD
	}

	# Perform login
	result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

	print (result)
	# Scrape url
	result = session_requests.get(URL, headers = dict(referer = URL))
	#tree = html.fromstring(result.content)
	#bucket_names = tree.xpath("//div[@class='repo-list--repo']/a/text()")

	#print(bucket_names)

if __name__ == '__main__':
    main()