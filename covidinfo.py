import os
import pandas as pd
import bs4
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep

def get_driver():
    opts = Options()
    opts.add_argument("headless")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_driver = os.getcwd() + "\chromedriver.exe"
    return webdriver.Chrome(options=opts, executable_path=chrome_driver)

def get_data(districts):
    district_list = []
    for d in districts[1:]:
        district_list.append([d.select("h5")[0].text,d.select("h2")[0].text])
    return district_list

def make_csv(district_list):
    district_data = pd.DataFrame(district_list)
    headers = ["Districts", "Active Cases"]
    district_data.to_csv("stateinfo.csv",index=False,header = headers)
    district_data.head()

def main():
    cdriver = get_driver()
    cdriver.get("https://www.covid19india.org/")
    search = cdriver.find_elements_by_css_selector(".search-input-wrapper > input[type=text]")[0]
    statename = input("Enter the State Name : ")
    search.send_keys(statename)
    print("Fetching data...")
    delay = 5
    try:
        results = WebDriverWait(cdriver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.results > a')))
    except TimeoutException:
        print("Please check the state name and try again")
        cdriver.quit()
        return
    results.click()
    sleep(3)
    try:
        button = cdriver.find_element_by_css_selector(".district-bar-bottom > button")
        button.click()
        sleep(3)
    except:
        pass
    covsoup = bs4.BeautifulSoup(cdriver.page_source, features="html.parser")
    districts = covsoup.select(".district")
    if len(districts)==1:
        print("District Wise data not available")
        print("Active Cases : {}".format(districts[0].select("h1 div")[0].text))
    else:
        district_list = get_data(districts)
        make_csv(district_list)
        print("District wise data of {} has been created in stateinfo.csv".format(statename))
    cdriver.quit()

if __name__=="__main__":
    main()
