from twilio.rest import TwilioRestClient

def send_message(number, message):
	"""
	Sends the message to the phone number
	"""
	account_sid = "AC156efdc4bccab2110a73fbce5f6de80c" # Your Account SID from www.twilio.com/console
	auth_token  = "4b3b92567bf0982a70227332b8e17188" 
	client = TwilioRestClient(account_sid, auth_token)

	message = client.messages.create(
		to=number, 
		from_="+19179246054",
	    body=message)