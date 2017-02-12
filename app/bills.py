import requests
import copy
import json
from dbagent import *
from sms import *


api_key = "dNCaDByvPa8s2y9CjdNh15tDKOvQ3HS730R2GFJH"
headers = {'X-API-Key': api_key}


def get_state_senators(stateAbbrv):
    """
    Gets the state senators information for the state
    """
    state = stateAbbrv
    chamber = "senate"
    senators = {}
    
    url = "https://api.propublica.org/congress/v1/members/%s/%s/current.json" % (chamber, state)

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
    congress = "115"
    chambers = ["house", "senate"]
    status = "introduced"
    committees = {}

    # populates each committee with the recent bills for it
    for chamber in chambers:
        url = "https://api.propublica.org/congress/v1/%s/%s/bills/%s.json" % (congress, chamber, status)

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


def add_recent_bills(committee_map):
    """
    Clears all recent bills and replaces them. Adds to the collection of all bills
    """
    db = get_main_db(read_only=False)
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
        bill_copy = copy.deepcopy(b)
        del bill_copy["_id"]
        bills.append(bill_copy)
    return json.dumps(bills)


def get_recent_bills_by_committee():
    """
    Gets a list of dicts of all of the recent bills
    """
    db = get_main_db()
    recent = db.recent
    com = {}
    cursor = recent.find()

    for b in cursor:
        bill_copy = copy.deepcopy(b)
        del bill_copy["_id"]
        c = bill_copy['committees'].replace('House', '').replace('Senate', '').replace('&#39;', '\'').replace('Committee', "").strip()

        try:
            com[c].append(bill_copy)
        except:
            com[c] = [bill_copy]
    return json.dumps(com)


def get_my_reps(zipcode):
    """
    Gets all representatives/senators for the zip code
    """
    url = "http://whoismyrepresentative.com/getall_mems.php?zip=%s&output=json" % str(zipcode)

    people = requests.get(url).json()['results']

    reps = {}

    for person in people:
        if len(person['district']) > 0:
            chamber, state, district = "house", person['state'], person['district']
            url = "https://api.propublica.org/congress/v1/members/%s/%s/%s/current.json" % (chamber, state, district)
            results = requests.get(url, headers=headers).json()['results']
            for r in results:
                bleh = r['name'].split()
                n = " ".join([bleh[0], bleh[-1]])
                if person['name'] == n:
                    r.update(person)
                    reps[n] = r
        else:
            chamber, state = "senate", person['state']
            url = "https://api.propublica.org/congress/v1/members/%s/%s/current.json" % (chamber, state)
            results = requests.get(url, headers=headers).json()['results']
            for r in results:
                bleh = r['name'].split()
                n = " ".join([bleh[0], bleh[-1]])
                if person['name'] == n:
                    r.update(person)
                    reps[n] = r
    return reps.values()


def text_message_body(user, topics):
    """
    Gets the body of the text message based on the number of topics
    user: user object
    topics: list of updated topics
    @return string message
    """
    try:
        name = user['email'][:user['email'].index('@')]
        print name
    except:
        name = user['email']

    topic_str = ""

    if len(topics) == 1:
        topic_str = topics
    elif len(topics) == 2:
        topic_str = topics[0] + " and " + topics[1]
    else:
        topic_str = ", ".join(topics[:-1]) + ", and " + topics[-1]

    link = "https://pillarapp.herokuapp.com"
    message = "Hi %s! New developments in %s! %s" % (name, topic_str, link)
    return message


def send_texts_to_users():
    """
    Sends texts to all users based on all recent bills
    """
    comm = json.loads(get_recent_bills_by_committee())

    # now get all users
    db = get_main_db()
    users = db.users
    user_iter = users.find({"phone number": {"$ne": "null"}})
    
    for user in user_iter:
        topics = []

        for t in user["topics"]:
            if t in comm:
                topics.append(t)

        if len(topics) > 0:
            message = text_message_body(user, topics)
            print message
            try:
                send_message(user['phone'], message)
            except:
                pass


def text_sign_up(email):
    message = "Thank you for signing up for Pillar! We're excited to work with you in shaping American democracy!"

    db = get_main_db()
    users = db.users
    user_iter = users.find({"email": email})

    for user in user_iter:
        send_message(user['phone'], message)


def main():
    # load and update stuff
    comm = load_recent_bills()
    add_recent_bills(comm)
    send_texts_to_users()


if __name__ == '__main__':
    # send_texts_to_users()
    print get_my_reps(str("91042"))
