from bs4 import BeautifulSoup
import requests
import json
from pprint import pprint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def fill_form(page_no):
    try:
        FORM_URL = "https://forms.gle/YtvWbnZpZ1mHx4en9"
        DRIVER_PATH = "/Users/utkarshvarma/Dropbox/My Mac (UTKARSHs-MacBook-Pro.local)/Documents/Development/chromedriver"
        final_prices = []
        final_urls = []
        final_addresses = []
        i = 0

        URL = f"https://duproprio.com/en/search/list?search=true&max_price=500000&rooms=3~3&is_for_sale=1&with_builders=1&parent=1&pageNumber={page_no}&sort=-published_at"

        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        def get_ld_json(url: str) -> dict:
            parser = "html.parser"
            req = requests.get(url)
            soup = BeautifulSoup(req.text, parser)
            return json.loads("".join(soup.find_all("script", {"type": "application/ld+json"})[1].contents))

        prices = soup.find_all(class_="search-results-listings-list__item-description__price")

        for price in prices:
            final_prices.append(str(price.text).strip())

        vals = get_ld_json(URL)['mainEntity'][0]['itemListElement']
        for val in vals:
            if i == 3 and len(final_prices)>10:
                pass
            else:
                final_urls.append(val['url'])
            i += 1
        i = 0

        addresses = soup.find_all(class_="search-results-listings-list__item-description__item "
                                         "search-results-listings-list__item-description__address")
        for address in addresses:
            if i == 3 and len(final_prices) > 10:
                pass
            else:
                final_addresses.append(str(address.text).strip())
            i += 1

        def make_final_file(addresses, prices, urls):
            final_file = {}
            for i in range(0, len(addresses)):
                final_file[i] = {"address": addresses[i], "price": prices[i], "url": urls[i]}

            return final_file

        print(len(final_addresses))
        print(len(final_prices))
        print(len(final_urls))
        final_data = make_final_file(final_addresses, final_prices, final_urls)
        pprint(f"final data is {final_data}")
        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(FORM_URL)

        for index in range(0, len(final_data)):
            sleep(5)
            current_add = final_data[index]['address']
            current_price = final_data[index]['price']
            current_url = final_data[index]['url']
            driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]'
                                         '/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(current_add)
            driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/'
                                         'div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(current_price)
            driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/'
                                         'div[2]/div/div[1]/div/div[1]/input').send_keys(current_url)
            driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span').click()
            sleep(4)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
    except:
        pprint(f"final data is {make_final_file(final_addresses, final_prices, final_urls)}")

        fill_form(page_no)
        # Bare Except on Purpose to cause recursion to overcome the request blocking due to bot detection


for page in range(0, 10):
    fill_form(page)
