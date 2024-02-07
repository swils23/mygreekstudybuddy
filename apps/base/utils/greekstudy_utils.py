import os
import time
import requests
import json
from bs4 import BeautifulSoup


class GreekStudyClient:
    username = ""
    password = ""
    userID = None

    users = []

    def __init__(self) -> None:
        self.get_credentials()
        # self.get_user_id_from_creds()
        self.get_users()
        # for user in self.users:
        #     print(user)

    def get_credentials(self) -> dict:
        # check for a .creds file
        creds = {}
        if os.path.exists(".creds") and os.path.getsize(".creds") > 0:
            with open(".creds", "r") as f:
                creds = json.load(f)
                self.username = creds["username"]
                self.password = creds["password"]
                self.userID = getattr(creds, "userID", None)
        else:
            # create a .creds file?
            choice = input(
                "No .creds file found, would you like to create one? (y/n): "
            )
            if choice.lower() == "y":
                self.username = input("Enter your email: ")
                self.password = input("Enter your password: ")
                creds = {
                    "username": self.username,
                    "password": self.password,
                    "userID": self.get_user_id_from_creds(),
                }
                with open(".creds", "w") as f:
                    json.dump(creds, f)
            else:
                print("Manual login required.")
                self.username = input("Enter your email: ")
                self.password = input("Enter your password: ")
                self.userID = self.get_user_id_from_creds()

    def get_user_id_from_creds(self) -> int:
        # since the ID isn't associated with the user on the client side, we'll have to do this hack
        # login to the site

        r = self.login()
        # get the request headers
        headers = r.request.headers
        cookies = r.cookies
        url = "https://mygreekstudy.com/welcome.php"
        r = requests.get(url, headers=headers, cookies=cookies)

        bs = BeautifulSoup(r.text, "html.parser")
        selector = "#nav-accordion > div > h4"
        try:
            first, last = (
                bs.select("#nav-accordion > div > h5")[0].text.strip().split(" ")
            )
        except:
            return "error"

        # now that we have the first and last name, we can get the user id with the dump_users function

        self.userID = self.get_user_by_name(name=first + " " + last).id

        return self.userID

    def get_user_by_name(self, name):
        # get the users
        users = self.get_users()
        # find the user with the matching name
        for user in users:
            if user.first + " " + user.last == name:
                return user
        return None

    def get_users(self):
        r = self.login()
        # get the request headers
        session = requests.Session()
        headers = r.request.headers
        url = "https://mygreekstudy.com/data.php"
        r = session.get(url, headers=headers)
        data = json.loads(r.text)

        users = []
        for user in data:
            first = user["member"].split(" ")[0].strip().capitalize()
            last = user["member"].split(" ")[1].strip().capitalize()
            id = user["id"]
            hours = user["hours"]

            users.append(User(first, last, id, hours))

        # alphabetize the users by first name
        users.sort(key=lambda x: x.first)
        self.users = users

        # log the users
        self.log_users(users)
        return users

    def get_user(self, userID:int = None):
        r = self.login()
        # get the request headers
        session = requests.Session()
        headers = r.request.headers
        url = "https://mygreekstudy.com/data.php"
        r = session.get(url, headers=headers)
        data = json.loads(r.text)

        if userID:
            for user in data:
                if user["id"] == userID:
                    return user
            return "User not found"
        return data

    def get_user_by_id(self, id: int):
        # get the users
        users = self.get_users()
        # find the user with the matching name
        for user in users:
            if user.id == id:
                return user
        return None

    @staticmethod
    def log_users(users: list):
        users = [user.__dict__ for user in users]
        users = sorted(users, key=lambda x: x["first"])
        for user in users:
            del user["hours"]

        if not os.path.exists(".users") or os.path.getsize(".users") == 0:
            with open(".users", "w") as f:
                json.dump(users, f, indent=4)
            return

        with open(".users", "r") as f:
            existing_users = json.load(f)
            for user in users:
                if user not in existing_users:
                    existing_users.append(user)
                    print("New user found: {}".format(user))
            with open(".users", "w") as f:
                json.dump(existing_users, f, indent=4)

    def post_hours(self, hours: int, minutes: int, locationID: int, sentUserID: int):
        # We can only post up to 10 hours at a time
        if hours > 10 or (hours == 10 and minutes > 0):
            print("You can only add 10 hours at a time. Will fix this eventually")
            # TODO, add a way to add 10 hours at a time by posting multiple times
            return

        post_url = "https://mygreekstudy.com/newManualProc.php"
        payload = {
            "hour": str(hours),
            "sendEmail": "admin@mygreekstudy.com",
            "locationID": locationID,
            "sentUserID": sentUserID,
            "minute": str(minutes),
        }
        r = requests.post(post_url, data=payload)

    """
    TODO Handle login errors such as incorrect username/password
    """

    def login(self, u: str = None, p: str = None) -> requests.Response:
        if not u:
            u = self.username
        if not p:
            p = self.password

        if not u or not p:
            print("No username or password provided.")
            return None
        post_url = "https://mygreekstudy.com/login.php"
        payload = {
            "username": u,
            "password": p,
        }
        r = requests.post(post_url, data=payload)
        return r


class User:
    def __init__(self, first: str, last: str, id: int, hours: int) -> None:
        self.first = first
        self.last = last
        self.id = id
        self.hours = hours

    def __str__(self) -> str:
        if getattr(self, "hours", None):
            return "{} {} ({}) - {} hours".format(
                self.first, self.last, self.id, self.hours
            )
        else:
            return "{} {} ({})".format(self.first, self.last, self.id)
