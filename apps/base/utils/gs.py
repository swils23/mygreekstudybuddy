import os
import time
import requests
import json
from bs4 import BeautifulSoup


class GreekStudy:
    userID = None
    users = None
    r = None

    def __init__(self) -> None:
        pass

    def login(self, email: str, password: str) -> None:
        post_url = "https://mygreekstudy.com/login.php"
        payload = {
            "username": email,
            "password": password,
        }
        self.r = requests.post(post_url, data=payload)
        # TODO make sure the login was successful, we could try to get the user id

    def get_users(self) -> list:
        if self.r is None:
            raise Exception("You must login first")

        # get the request headers
        session = requests.Session()
        headers = self.r.request.headers
        url = "https://mygreekstudy.com/data.php"
        self.r = session.get(url, headers=headers)
        data = json.loads(self.r.text)
        # data = [{'id': '265609', 'member': 'Dylan Gunn', 'hours': '13.23'}, {'id': '220046', 'member': 'Josh Mercer', 'hours': '12.50'} ...
        # want to transform into a list of dicts
        """
            [
            {
                "first": "Dylan",
                "last": "Gunn",
                "id": 265609,
                "hours": 13.23
            },
            {
                "first": "Josh",
                "last": "Mercer",
                "id": 220046,
                "hours": 12.50
            }
        ]
        """
        users = []
        for user in data:
            # for some reason there are some names with 2 spaces 'member': 'First  Last', causing more than 2 items in the split
            first = user["member"].strip().split(" ")[0].capitalize()
            last = user["member"].strip().split(" ")[-1].capitalize()
            id = user["id"]
            hours = user["hours"]
            users.append({"first": first, "last": last, "id": id, "hours": hours})

        # alphabetize the users by first name
        users.sort(key=lambda x: x["first"])
        self.users = users

        return users

    def get_user_id(self) -> int:
        # since the ID isn't associated with the user on the client side, we'll have to do this hack
        # login to the site
        if self.r is None:
            raise Exception("You must login first")

        # get the request headers
        headers = self.r.request.headers
        cookies = self.r.cookies
        url = "https://mygreekstudy.com/welcome.php"
        self.r = requests.get(url, headers=headers, cookies=cookies)

        bs = BeautifulSoup(self.r.text, "html.parser")
        try:
            first, last = bs.select("#nav-accordion > div > h5")[0].text.strip().split(" ")
        except:
            return "error"

        # now that we have the first and last name, we can get the user id with the dump_users function
        # we don't need this function, just iterate though

        self.userID = self.get_user(userID=None, first=first, last=last)["id"]

        return self.userID

    def get_user(self, userID: int = None, first: str = None, last: str = None):
        if self.users is None:
            self.get_users()

        if userID:
            for user in self.users:
                if user["id"] == str(userID):
                    return user
        if first and last:
            for user in self.users:
                if user["first"] == first and user["last"] == last:
                    return user
        if first:
            for user in self.users:
                if user["first"] == first:
                    return user
        if last:
            for user in self.users:
                if user["last"] == last:
                    return user
        return False

    # def get_user(self, userID: int = None):
    #     r = self.login()
    #     # get the request headers
    #     session = requests.Session()
    #     headers = r.request.headers
    #     url = "https://mygreekstudy.com/data.php"
    #     r = session.get(url, headers=headers)
    #     data = json.loads(r.text)
    #
    #     if userID:
    #         for user in data:
    #             if user["id"] == userID:
    #                 return user
    #         return "User not found"
    #     return data

    # def get_user_by_id(self, id: int):
    #     # get the users
    #     users = self.get_users()
    #     # find the user with the matching name
    #     for user in users:
    #         if user.id == id:
    #             return user
    #     return None

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
