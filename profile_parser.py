import time
import requests
from bs4 import BeautifulSoup


def profile_parse(data):
    for item in data:
        try:
            profile_link = "https://steamcommunity.com/profiles/" + \
                item["steam_link"].split("/")[4]
            print(profile_link)
            text = requests.get(profile_link).text
            result = text.find("https://steamcommunity.com/tradeoffer/")
            if result != -1:
                print("\tFounded")
                item["trade_link"] = True
        except:
            print("Bad link")
        time.sleep(0.5)

    return data


if __name__ == "__main__":
    profile_parse(
        "http://steamcommunity.com/profiles/76561199046915102/sa/")
