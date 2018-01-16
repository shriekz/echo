import requests
from lxml import html
import json
import datetime


USERNAME = "ssrikanth77@gmail.com"
PASSWORD = "kaju2007"

BASE_REFERRER = "https://www.yokibu.com/signin?ut=pt"
LOGIN_URL="https://www.yokibu.com/ajax-signin"
POST_URL = "https://www.yokibu.com/ajax-getposts"
HOME_URL = "https://www.yokibu.com/home"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
JSON_AUTHENTICATOR = ")]}',"

ABHINAV = "Abhinav"
VIDHYUTH = "Vidhyuth"
ABHI_CLASS = "V Std C (2017)"
VIDHYUTH_CLASS = "I Std C (2017)"
NO_MESSAGE_TODAY = "You have no messages for today"


proscribed = [
	"<br>",
	"<br/>"
	"<italic>",
	"<italic/>"
]


def extractFromYokibu():

	# Create payload
	payload = {
	    "username": USERNAME, 
	    "password": PASSWORD,
	    "staysignedin":"TRUE",
	    "usertype":"pt",
	    "remme":"0",
	    "rdpage":""
	}

	post_payload = {
		"atkn" :"",
		"filtertype":"1"
	}

	headers1 = {
		"referer":BASE_REFERRER,
		"X-Requested-With": "XMLHttpRequest",
		"User-Agent":USER_AGENT
	}

	headers2 = {
		"referer":HOME_URL,
		"X-Requested-With": "XMLHttpRequest",
		"User-Agent":USER_AGENT
	}

	# Get the session objects
	session_requests = requests.session()

	# Perform login
	result = session_requests.post(LOGIN_URL, data = payload, headers = headers1)

	# scrape data from the home page
	result = session_requests.get(HOME_URL, headers=headers1)
	
	# Extract the token from the home page.
	tree = html.fromstring(result.text)
	
	#Get the atkn token, it is contained in token_1
	token = tree.xpath("//script[contains(., 'atkn')]/text()")
	token_1 = (token[0].split(","))[0]
	token_2 = token_1.split(":")[1]
	post_payload['atkn'] = token_2.strip('/"')
	#print(post_payload)

	#scrape data from post feed.
	result = session_requests.post(POST_URL, data=post_payload, headers=headers2)
	# string json authenticator put in to prevent hijacking.

	json_results = json.loads((result.text).replace(JSON_AUTHENTICATOR,""))
	#print(json_results)
	
	return getLatestMessage(json_results)

def replaceStrings(s):

	#print(s)
	str = s
	for x in proscribed:
		#print("In there..."+ x)
		str = str.replace(x,"")
		#print(str)
	return str

def getLatestMessage(json_results):


	#print(json_results)
	# read through the json file to identify the first two messages and also the latest message for abhi and vidhyuth.
	# for latest one, read the tag dmt
	today = datetime.datetime.now().strftime("%Y-%m-%d")

	abhiMsg = ""
	sweetMsg = ""	
	abhiPresent = False
	vidhyuthPresent = False	
	message = ""

	for post in json_results['content']['posts']:

		# Filter for messages from school alone, messages from parents are ignored.
		if (post['pa']['type'] != "School"): continue
		msg_date = post['dmt'].split(" ")[0]

		# Get all messages that were posted by school today and concatenate them.
		if ( today == msg_date):
			if (message != ""):
				message = "%s. Another message for today: %s " %(message, post['pc'])
			else:
				message = post['pc']

		# If we have all messages for today and the latest for Abhi and Vidhyuth, get out here.
		if (abhiPresent) and (vidhyuthPresent) and (today != msg_date): break

		msg_details = post['pc']
		# If Abhi's class is in the message and this is the latest one then get it.
		if ((ABHI_CLASS in post['pt']) and (abhiPresent == False)):
			abhiMsg = "Latest Message for %s, Message received on %s, %s" % (ABHINAV, msg_date, msg_details)
			abhiPresent = True;

		# Same for vidhyuth
		if ( (VIDHYUTH_CLASS in post['pt']) and (vidhyuthPresent == False)):
			sweetMsg = "Latest Message for %s, Message received on %s, %s" % (VIDHYUTH, msg_date, msg_details)
			vidhyuthPresent = True;
		

	if (message == ""): message = NO_MESSAGE_TODAY
	else: message = "Messages received today, " + message

	return replaceStrings("<p>"+ message+"</p> "+abhiMsg+sweetMsg)

def main():
	print(extractFromYokibu())

if __name__ == '__main__':
    main()
