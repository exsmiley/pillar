import requests
import copy
from pymongo import MongoClient


def get_state_senators(stateAbbrv):
    """
    Gets the state senators information for the state
    """
    api_key = "dNCaDByvPa8s2y9CjdNh15tDKOvQ3HS730R2GFJH"
    
    state = stateAbbrv
    chamber = "senate"
    senators = {}
    
    url = "https://api.propublica.org/congress/v1/members/%s/%s/current.json" % (chamber, state)

    headers = {'X-API-Key': api_key}

    results = requests.get(url, headers=headers).json()['results']
    
    for r in results:
        c = r["name"]
        try:
            senators[c].append(r)
        except:
            senators[c] = [r]

    return senators


def load_recent_bills():
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

        for r in results['bills']:
            c = r['committees'].replace('House', '').replace('Senate', '').replace('&#39;', '\'').strip()
            bill_uri = r['bill_uri']
            content = requests.get(bill_uri, headers=headers).json()
            info = content['results'][0]

            """ EXAMPLE
            {u'votes': [], u'latest_major_action': u'Referred to the House Committee on Armed Services.', 
            u'committees': u'House Armed Services Committee', u'house_passage_vote': None, 
            u'congress': u'115', u'title': u'To exempt certain Department of Defense civilian positions from any furlough as a result of a lapse in discretionary appropriations, and for other purposes.', 
            u'sponsor_uri': u'https://api.propublica.org/congress/v1/members/C001053.json', u'bill': u'H.R.989', u'actions': [{u'description': u'Referred to the House Committee on Armed Services.', 
            u'datetime': u'2017-02-09 00:00:00 UTC'}], u'introduced_date': u'2017-02-09', u'bill_uri': u'https://api.propublica.org/congress/v1/115/bills/hr989.json', 
            u'gpo_pdf_uri': u'', u'primary_subject': u'', u'sponsor': u'Tom  Cole', u'latest_major_action_date': u'2017-02-09', 
            u'versions': [], u'senate_passage_vote': None, u'cosponsors': u'4'}
            """

            # add the information to the dict
            try:
                committees[c].append(info)
            except:
                committees[c] = [info]

    return committees


def get_main_db():
    """
    Gets DB object to be able insert into
    """
    user = "master"
    pwd = "m4st3r"
    dbname = "pillar"

    client = MongoClient("ds149059.mlab.com", 49059)
    db = client[dbname]
    db.authenticate(user, pwd)
    return db


def add_recent_bills(committee_map):
    """
    Clears all recent bills and replaces them. Adds to the collection of all bills
    """
    db = get_main_db()
    recent = db.recent
    bills = db.bills

    # clear all old bills in recent
    recent.delete_many({});

    # add all new ones
    for _, bill_list in committee_map.iteritems():
        for bill in bill_list:
            recent.insert_one(bill)

            # add to main bill collection, update if exists otherwise insert
            bill_copy = copy.deepcopy(bill)
            del bill_copy["_id"]
            result = bills.update_one({"bill": bill['bill']}, {"$set": bill_copy})

            if result.matched_count == 0:
                bills.insert_one(bill)


def get_all_recent_bills():
    """
    Gets a list of dicts of all of the recent bills
    """
    db = get_main_db()
    recent = db.recent
    bills = []
    cursor = recent.find()
    for b in cursor:
        bills.append(b)
    return bills


def main():
    # com = load_recent_bills()
    # add_recent_bills(com)
    print len(get_all_recent_bills())

main()