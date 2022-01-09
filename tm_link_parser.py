import requests
from bs4 import BeautifulSoup
import json



def parse_id(link):
    response = requests.get(link)
    data = response.text
    defindex = data.split('"defindex":')[1].split(",")[0]
    paintindex = data.split('"paintindex":')[1].split(",")[0]
    return defindex, paintindex


def parse_tmlinks(item_link):
    result = []
    response = requests.get(item_link)
    soup = BeautifulSoup(response.text, "lxml")
    same_items = soup.find_all("div", class_="sameitem")
    for item in same_items:
        name = soup.find(
            'div', class_="item-h1").find('h1').text.split(" (")[0]
        item_link = "https://market.csgo.com" + item.find("a").get("href")
        item_float = item.find(
            "div", class_="sameitem-floatnum").find("span").get("title")
        price = item.find("button").text.strip()
        try:

            defindex, paintindex = parse_id(item_link)

            result.append({
                "name": name,
                "link": item_link,
                "item_float": item_float,
                "price": price,
                "Link_to_csgofloat_db": f"https://csgofloat.com/db?defIndex={defindex}&paintIndex={paintindex}&min={float(item_float)}&max={float(item_float)}",
                "defindex": defindex,
                "paintindex": paintindex
            })
        except Exception:
            print(f"Link {item_link} just broke")
    return result
