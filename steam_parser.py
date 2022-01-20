from lib2to3.pgen2 import driver
from ssl import DER_cert_to_PEM_cert
import time
import pickle

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EС


def login():
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(
        executable_path="/home/tm_full_killer/geckodriver", options=options)
    try:
        driver.get("https://steamcommunity.com/openid/login?openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.mode=checkid_setup&openid.ns=http://specs.openid.net/auth/2.0&openid.realm=https://csgofloat.com&openid.return_to=https://csgofloat.com/")
        login = driver.find_element_by_id("steamAccountName")
        password = driver.find_element_by_id("steamPassword")
        login.send_keys("mija_zxc")
        password.send_keys("0SFTN2q0J586qGKbTG6")
        login_btn = driver.find_element_by_id("imageLogin")
        login_btn.click()
        two_factor = driver.find_element_by_id("twofactorcode_entry")
        code = input("Code: ")
        two_factor.send_keys(code)
        WebDriverWait(driver, 5).until(EС.element_to_be_clickable(
            (By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div[4]/div[1]/div[1]/div[2]"))).click()
        time.sleep(5)
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit


def steam_parse(data):
    # login()
    try:
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(
            executable_path="/home/tm_full_killer/geckodriver", options=options)

        for i, item in enumerate(data):
            driver.get(item["Link_to_csgofloat_db"])
            if i == 0:
                for cookie in pickle.load(open("cookies", "rb")):
                    print(cookie)
                    driver.add_cookie(cookie)
                time.sleep(2)
                driver.refresh()
            time.sleep(2)
            try:
                link = driver.find_element_by_xpath(
                    "/html/body/app-root/div/div[2]/app-float-db/div/div/app-float-dbtable/div/div/table/tbody/tr/td[7]/div/app-steam-avatar/a")
                print(link.get_attribute('href'))
                item["steam_link"] = link.get_attribute('href')
            except:
                print("Error link: ", item["Link_to_csgofloat_db"])
            time.sleep(1)
    except Exception as ex:
        print(ex)
    driver.quit()
    return data


def main():
    steam_parse()


if __name__ == "__main__":
    main()
