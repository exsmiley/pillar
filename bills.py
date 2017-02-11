import requests

def get_recent_bills():
	"""
	Gets the 20 most recent bills in the House and Senate and
	maps each committee to the bills associated with them
	"""
	api_key = "dNCaDByvPa8s2y9CjdNh15tDKOvQ3HS730R2GFJH"

	congress = "115"
	chambers = ["house", "senate"]
	status = "introduced"
	committees = {}

	# populates each committee with the recent bills for it
	for chamber in chambers:
		url = "https://api.propublica.org/congress/v1/%s/%s/bills/%s.json" % (congress, chamber, status)

		headers = {'X-API-Key': api_key}

		results = requests.get(url, headers=headers).json()['results'][0]

		print results['num_results']

		for r in results['bills']:
			c = r['committees'].replace('House', '').replace('Senate', '').replace('&#39;', '\'').strip()
			try:
				committees[c].append(r)
			except:
				committees[c] = [r]

	return committees