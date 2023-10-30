import requests
import json
import os
from bs4 import BeautifulSoup

"""
TODO Handle login errors such as incorrect username/password
"""
def login(u:str, p:str) -> requests.Response:
    post_url = "https://mygreekstudy.com/login.php"
    payload = {
        "username": u,
        "password": p,
    }
    r = requests.post(post_url, data=payload)
    return r

""" DEPRECATED
def get_hours(r) -> (float, float):
    url = "https://mygreekstudy.com/welcome.php"
    if r.url != url:
        return "Not on welcome page... got: " + r.url
    

    bs = BeautifulSoup(r.text, "html.parser")
    selector = "#nav-accordion > div > h4"
    try:
        hours = [float(h) for h in bs.select(selector)[0].text[13:].split(" of ")]
    except:
        return "Error parsing hours, are we logged in?"
    return hours
"""

def post_hours(hours:int, minutes:int, locationID:int, sentUserID:int):
    post_url = "https://mygreekstudy.com/newManualProc.php"
    payload = {
        "hour": str(hours),
        "sendEmail": "admin@mygreekstudy.com",
        "locationID": locationID,
        "sentUserID": sentUserID,
        "minute": str(minutes),
    }
    r = requests.post(post_url, data=payload)

def get_credentials() -> dict:
    # check for a .creds file
    creds = {}
    if os.path.exists(".creds"):
        with open(".creds", "r") as f:
            creds = json.load(f)
    else:
        # create a .creds file?
        choice = input("No .creds file found, would you like to create one? (y/n): ")
        if choice.lower() == "y":
            username = input("Enter your email: ")
            password = input("Enter your password: ")
            creds = {
                "username": username,
                "password": password,
            }
            with open(".creds", "w") as f:
                json.dump(creds, f)
        else:
            print("Manual login required.")
            username = input("Enter your email: ")
            password = input("Enter your password: ")
            creds = {
                "username": username,
                "password": password,
            }
    return creds

# wow... they dont even authenticate, we can just post hours as long as we know their id, and everyone's info is WIDE OPEN??
def dump_users(name:str=None, userID:int=None):
    creds = get_credentials()
    r = login(creds["username"], creds["password"])
    # get the request headers
    session = requests.Session()
    headers = r.request.headers
    url = "https://mygreekstudy.com/data.php"
    r = session.get(url, headers=headers)
    data = json.loads(r.text)
    users = []
    for user in data:
        if not userID and not name:
            users.append("{}: {} ({}hrs)".format(user["member"], user["id"], user["hours"]))
        elif userID and user["id"] == str(userID):
            users.append("{}: {} ({}hrs)".format(user["member"], user["id"], user["hours"]))
        elif name and name.lower() in user["member"].lower():
            users.append("{}: {} ({}hrs)".format(user["member"], user["id"], user["hours"]))
    print("\n".join(users))


def main():
    print("1) Add hours to a user\n*2) List all users\n*3) List specific user(s) by name\n*4) List specific user(s) by ID\n(* = requires login)")
    choice = input("Enter choice: ")
    if choice == "1":
        userID = input("Enter userID: ")
        hours = input("Enter hours to add in HH:MM format: ")
        hours = hours.split(":")
        hours = [int(h) for h in hours]
        post_hours(hours=hours[0], minutes=hours[1], locationID=4311, sentUserID=userID)
    elif choice == "2":
        dump_users()
    elif choice == "3":
        name = input("Enter name: ")
        dump_users(name=name)
    elif choice == "4":
        userID = input("Enter userID: ")
        dump_users(userID=userID)
    return

if __name__ == "__main__":
    main()