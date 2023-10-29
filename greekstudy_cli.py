import requests
import json
import os
from bs4 import BeautifulSoup

"""
TODO Handle login errors such as incorrect username/password
"""
def login(u:str, p:str, cookies=None) -> requests.Response:
    post_url = "https://mygreekstudy.com/login.php"
    payload = {
        "username": u,
        "password": p,
    }
    r = requests.post(post_url, data=payload)
    return r

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

def post_hours(r, hours:int, minutes:int):
    post_url = "https://mygreekstudy.com/newManualProc.php"
    payload = {
        "hour": str(hours),
        "sendEmail": "test@gmail.com",
        "locationID": "4311",
        "sentUserID": "000000",
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
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            creds = {
                "username": username,
                "password": password,
            }
            with open(".creds", "w") as f:
                json.dump(creds, f)
        else:
            print("Manual login required.")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            creds = {
                "username": username,
                "password": password,
            }
    return creds

def main():
    creds = get_credentials()
    r = login(creds["username"], creds["password"])

    hours = get_hours(r)
    print(f"Current hours: {hours[0]} of {hours[1]}")
    hours_to_add = input("Enter hours to add in HH:MM format: ")
    hours_to_add = hours_to_add.split(":")
    hours_to_add = [int(h) for h in hours_to_add]

    post_hours(r, hours=hours_to_add[0], minutes=hours_to_add[1])

    r = login(creds["username"], creds["password"])
    hours = get_hours(r)
    print(f"New hours: {hours[0]} of {hours[1]}")
    
    



    



if __name__ == "__main__":
    main()
