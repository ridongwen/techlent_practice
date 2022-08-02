import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import time
from random import random

class Crawler:
    def __init__(self, zipcode):
        self.head = "https://www.har.com"
        self.zipcode = zipcode
        self.houses = []

    def get_total_page_count(self):
        tail = "/zipcode_{0}/realestate/for_sale".format(self.zipcode)
        url = self.head+tail
        req = requests.get(url)
        return BeautifulSoup(req.text, 'html.parser').find_all('a', attrs={"class": "page-link pages_a"})[-1].get_text()

    def append_houses_by_page_number(self, page=0):
        tail = "/zipcode_{0}/realestate/for_sale?page={1}".format(self.zipcode, page)
        url = self.head+tail
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        house_list = soup.find_all('div', attrs={"class": "cardv2--landscape__content__body__details"})
        house_list_len = len(house_list)

        for i in range(house_list_len):
            house = {'address': (re.sub(r'[\ \n]{2,}', ', ', house_list[i].find('div', attrs={"class": "cardv2--landscape__content__body__details_address_left_add"}).get_text().strip())),
                     'price': (house_list[i].find('div', attrs={"class": "cardv2--landscape__content__body__details_price"}).get_text().strip())}

            items = house_list[i].find_all('div', attrs={"class": "cardv2--landscape__content__body__details_features_item"})
            house['bedroom'] = " "
            house['building_size'] = " "
            house['bath'] = " "
            house['lot_size'] = " "
            house['stories'] = " "
            house['has_private_pool'] = " "
            house['year_built'] = " "

            if len(items) == 2:
                house['lot_size'] = items[0].get_text().strip()
                house['stories'] = items[1].get_text().strip()
            elif len(items) == 4:
                house['bedroom'] = items[0].get_text().strip()
                house['building_size'] = items[1].get_text().strip()
                house['bath'] = items[2].get_text().strip()
                house['stories'] = items[3].get_text().strip()
            elif len(items) == 5:
                house['bedroom'] = items[0].get_text().strip()
                house['building_size'] = items[1].get_text().strip()
                house['bath'] = items[2].get_text().strip()
                house['stories'] = items[3].get_text().strip()
                house['year_built'] = items[4].get_text().strip()
            elif len(items) == 6:
                house['bedroom'] = items[0].get_text().strip()
                house['building_size'] = items[1].get_text().strip()
                house['bath'] = items[2].get_text().strip()
                house['lot_size'] = items[3].get_text().strip()
                house['stories'] = items[4].get_text().strip()
                house['year_built'] = items[5].get_text().strip()
            elif len(items) == 7:
                house['bedroom'] = items[0].get_text().strip()
                house['building_size'] = items[1].get_text().strip()
                house['bath'] = items[2].get_text().strip()
                house['lot_size'] = items[3].get_text().strip()
                house['stories'] = items[4].get_text().strip()
                house['has_private_pool'] = items[5].get_text().strip()
                house['year_built'] = items[6].get_text().strip()

            self.houses.append(house)

    def write_to_csv(self, file_name):
        if(self.houses):
            df = pd.DataFrame(self.houses)
            df.to_csv(file_name, encoding='utf-8', index=False)

def crawler_har(zipcode):
    crawler = Crawler(zipcode)
    page_count = crawler.get_total_page_count()

    for n in range(1, int(page_count)+1):
        crawler.append_houses_by_page_number(n)
        t = 1 + 2 * random()
        time.sleep(t)

    crawler.write_to_csv("Sample_data.csv")

if __name__ == "__main__":
    crawler_har("77080")


