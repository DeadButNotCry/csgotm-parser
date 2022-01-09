import requests
from bs4 import BeautifulSoup
import json

result = []


def parse_id(link):
    response = requests.get(link)
    data = response.text
    defindex = data.split('"defindex":')[1].split(",")[0]
    paintindex = data.split('"paintindex":')[1].split(",")[0]
    return defindex, paintindex


def parse_tmlinks(item_link):
    print(item_link)
    response = requests.get(item_link)
    soup = BeautifulSoup(response.text, "lxml")
    same_items = soup.find_all("div", class_="sameitem")
    for item in same_items:
        name = soup.find('div', class_="item-h1").find('h1').text.split(" (")[0]
        item_link = "https://market.csgo.com" + item.find("a").get("href")
        item_float = item.find("div", class_="sameitem-floatnum").find("span").get("title")
        price = item.find("button").text.strip()
        defindex, paintindex = parse_id(item_link)

        result.append({
            "name": name,
            "link": item_link,
            "item_float": item_float,
            "price": price,
            "Link_to_csgofloat_db": f"https://csgofloat.com/db?defIndex={defindex}&paintIndex={paintindex}&min={round(float(item_float), 5)}&max={round(float(item_float), 5) + 0.00001}",
            "defindex": defindex,
            "paintindex": paintindex
        })

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    parse_tmlinks(
        "https://market.csgo.com/item/4691595247-188530139-%E2%98%85%20%D0%9A%D0%BE%D0%B3%D0%BE%D1%82%D1%8C%20%7C%20%D0%97%D1%83%D0%B1%20%D1%82%D0%B8%D0%B3%D1%80%D0%B0%20(%D0%9F%D1%80%D1%8F%D0%BC%D0%BE%20%D1%81%20%D0%B7%D0%B0%D0%B2%D0%BE%D0%B4%D0%B0)/"
    )


if __name__ == '__main__':
    main()
