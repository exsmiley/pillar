from pymongo import MongoClient
import hashlib
import json

def get_main_db(read_only=True):
    """
    Gets DB object to be able insert into
    read_only: creates a user with write permissions if False
    """
    user = "master"
    pwd = "m4st3r"

    if read_only:
        user = "read"
        pwd = "r34d"

    dbname = "pillar"

    client = MongoClient("ds149059.mlab.com", 49059)
    db = client[dbname]
    db.authenticate(user, pwd)
    return db

# import facebook # pip install facebook-sdk

# graph = facebook.GraphAPI(access_token='406864109667730|9b6FiIu7UHbRIRo3U2yUD9fFGYM')

def add_new_user(email, pwd, phone, zipcode, name):
    """
    Creates a new user in the database
    @return True if created new user
    """
    hash_object = hashlib.sha256(pwd)
    hash_pwd = hash_object.hexdigest()
    user = {"email": email, "pwd": hash_pwd, "phone": phone, "topics": [], "zipcode": zipcode, "name": name}

    db = get_main_db(read_only=False)
    users = db.users

    total = users.find({"email": email})

    if total.count() != 0:
        return False

    users.insert_one(user)
    print "Made " + email
    return True

def add_topics_for_user(email, topics):
    """
    Adds the topics for the user
    """
    db = get_main_db(read_only=False)
    users = db.users
    users.update_one({"email": email}, {"$set": {"topics": topics}})


def get_topics_for_user(email):
    """
    Adds the topics for the user
    """
    db = get_main_db()
    users = db.users
    results = users.find({"email": email})

    for i in results:
        return json.dumps(i['topics'])


def validate_user(email, pwd):
    """
    Checks if user exists in the database
    """
    hash_object = hashlib.sha256(pwd)
    hash_pwd = hash_object.hexdigest()
    db = get_main_db(read_only=False)
    users = db.users
    exists = users.find({"email": email, "pwd": hash_pwd})
    return exists.count() == 1


def user_zipcode(email):
    db = get_main_db()
    users = db.users
    results = users.find({"email": email})

    for i in results:
        return i['zipcode']


add_topics_for_user("bob@bob.com", ['Ways and Means', 'Finance', "Indian Affairs"])