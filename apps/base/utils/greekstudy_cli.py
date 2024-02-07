import os
import time
import requests
import json
from bs4 import BeautifulSoup


import argparse
import sys

# doesnt work since utils is already a name in use
# from utils import GreekStudy
# instead, we'll just import the class directly
from greekstudy_utils import GreekStudyClient


LOCATION_ID = 4311  # I believe this is the "location" for hours logged online with no real location


def interactive():
    # GreekStudy = GreekStudyClient()
    # print(
    #     "1) Add hours to a user\n"
    #     "*2) List all users\n"
    #     "*3) Get current user ID\n"
    #     "(* = requires login)"
    # )
    # choice = input("Enter choice: ")
    # if choice == "1":
    #     userID = input("Enter userID: ")
    #     hours = input("Enter hours to add in HH:MM format: ")
    #     hours = hours.split(":")
    #     hours = [int(h) for h in hours]
    #     GreekStudy.get_users(userID=userID)
    #     GreekStudy.post_hours(
    #         hours=hours[0], minutes=hours[1], locationID=LOCATION_ID, sentUserID=userID
    #     )
    #     time.sleep(1)
    #     # GreekStudy.get_users(userID=userID)
    # elif choice == "2":
    #     users = GreekStudy.get_users()
    #     for user in users:
    #         print(user)
    # elif choice == "3":
    #     print(GreekStudy.get_user_id_from_creds())

    # THIS is dumb, we should just have an easy mode

    # user should set their .creds file
    GreekStudy = GreekStudyClient()

    # now that we have the user's creds, we'll get the user's ID
    userID = GreekStudy.get_user_id_from_creds()
    if not userID:
        print("Unable to get userID using specified credentials.")
        return

    # get that user's hours
    user = GreekStudy.get_user(userID=userID)
    print(
        f"UserID: {user['id']}\n"
        f"Name: {user['member']}\n"
        f"Current Hours: {user['hours']}\n"
    )

    print("How many hours would you like to add? (0-9)")
    hours = -1
    while hours < 0 or hours > 9:
        hours = int(input("Enter hours: "))
        if hours < 0 or hours > 9:
            print("Invalid input. Please enter a number between 0 and 9.")
    minutes = -1
    while minutes < 0 or minutes > 59:
        minutes = int(input("Enter minutes: "))
        if minutes < 0 or minutes > 59:
            print("Invalid input. Please enter a number between 0 and 59.")

    GreekStudy.post_hours(
        hours=hours, minutes=minutes, locationID=LOCATION_ID, sentUserID=userID
    )
    time.sleep(1)
    user = GreekStudy.get_user(userID=userID)
    print(
        f"\nNew Hours: {user['hours']}\n"
    )







    return


def non_interactive():
    """args
    -A --add: add hours to a user
    -L --list: list all users
    """
    GreekStudy = GreekStudyClient()
    parser = argparse.ArgumentParser()

    # List all users

    # Add hours to a user, will be 2 arguments, userID and hours:minutes
    # -A --add -u 123456 -t 1:30

    arguments = [
        {
            "help": "list all users",
            "shortflag": "-L",
            "longflag": "--list",
            "action": "store_true",
        },
        {
            "help": "add hours to a user",
            "shortflag": "-A",
            "longflag": "--add",
            "action": "store_true",
        },
        {
            "help": "userID",
            "shortflag": "-u",
            "longflag": "--userID",
            "action": "store",
        },
        {
            "help": "hours:minutes",
            "shortflag": "-t",
            "longflag": "--time",
            "action": "store",
        },
    ]
    for arg in arguments:
        parser.add_argument(
            arg["shortflag"], arg["longflag"], help=arg["help"], action=arg["action"]
        )

    args = parser.parse_args()

    # List all users
    if args.list:
        GreekStudy.get_users()
        return

    # Add hours to a user
    if args.add:
        # validate userID and time arguments
        if args.userID and args.time:
            userID = int(args.userID)
            hours = int(args.time.split(":")[0])
            minutes = int(args.time.split(":")[1])

            GreekStudy.get_users()
            GreekStudy.post_hours(
                hours=hours, minutes=minutes, locationID=LOCATION_ID, sentUserID=userID
            )
            time.sleep(1)
            GreekStudy.get_users()

        # if hours are passed in but the userID is not, but there is a .creds file, use the userID from the .creds file

    # if userID and time are passed but not add, print help


def main():
    # if any args are passed, run non-interactive mode
    if sys.argv[1:]:
        non_interactive()
    else:
        interactive()
    # gs = GreekStudyClient()
    # print(gs.get_user_id_from_creds())


if __name__ == "__main__":
    main()
