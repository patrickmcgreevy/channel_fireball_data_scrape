import requests
from bs4 import BeautifulSoup
from re import sub
from datetime import datetime
import pandas as pd


class Item:
    def __init__(self, vid, name, card_id, price, mtg_set, variant):
        self.vid = vid
        self.name = name
        self.id = card_id
        self.price = price
        self.mtg_set = mtg_set
        self.variant = variant

    def __init__(self, form):
        self.vid = form['data-vid']
        self.name = form['data-name']
        self.id = form['data-id']
        self.price = sub(r'[$,]', '', form['data-price'])
        self.mtg_set = form['data-category']
        self.variant = form['data-variant']

    def print(self):
        print('name: ', self.name)
        print('v_id: ', self.vid)
        print('id: ', self.id)
        print('price: ', self.price)
        print('MTG set: ', self.mtg_set)
        print('variant: ', self.variant)

    def get_member_names(self):
        return 'Name', 'vID', 'ID', 'Price', 'MTG Set', 'Variant'

    def get_member_values(self):
        return self.name, self.vid, self.id, self.price, self.mtg_set, self.variant

buylist_url_template = "https://store.channelfireball.com/advanced_search?buylist_mode=1&commit=Search&page=1&search%5Bbuy_price_gte%5D=1.00&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=0&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bsort%5D=buy_price&search%5Btags_name_eq%5D=&utf8=%E2%9C%93"
selllist_url_template ="https://store.channelfireball.com/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D=&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=1&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bsort%5D=sell_price&search%5Bdirection%5D=descend&commit=Search&search%5Bcatalog_group_id_eq%5D="
def build_buylist_url(pageNum, minPrice):
    start = "https://store.channelfireball.com/advanced_search?buylist_mode=1&commit=Search&page=" # insert page
    mid = "&search%5Bbuy_price_gte%5D="
    end = "&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=0&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bsort%5D=buy_price&search%5Btags_name_eq%5D=&utf8=%E2%9C%93"

    return start + str(pageNum) + mid + str(minPrice) + end

def get_soup(url):
    headers = {'Accept-Encoding': 'identity'}
    return BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')


def get_add_forms(soup):
    return soup.find_all('form', class_='add-to-cart-form')


def form_list_to_buylistItem_list(form_list):
    return [Item(i) for i in form_list]


#Pass in the url and the buylist/selllist function you want to use
def get_buyitem_list(url):
    soup = get_soup(url)
    form_list = get_add_forms(soup)
    return form_list_to_buylistItem_list(form_list)

def scrape_all_buy_list(minPrice):
    item_list = []
    i = 1
    print('Scraping buy list')
    while True:
        url = build_buylist_url(str(i), minPrice)
        cItem_list = get_buyitem_list(url)
        if not cItem_list:
            print('Completed.')
            break
        else:
            item_list += cItem_list
            print('Page ' , i, 'scraped')
        i += 1

    return item_list

def build_sell_list_url(pageNum, minPrice):
    front = "https://store.channelfireball.com/advanced_search?buylist_mode=0&commit=Search&page="
    mid = "&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=0&search%5Bsell_price_gte%5D="
    end = "&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=1&search%5Bsell_price_gte%5D=1&search%5Bsell_price_lte%5D=&search%5Bsort%5D=sell_price&search%5Btags_name_eq%5D=&utf8=%E2%9C%93"
    return front + str(pageNum) + mid + str(minPrice) + end

def scrape_all_sell_list(minPrice):
    item_list = []
    i = 1
    print('Scraping sell list')
    while True:
        try:
            url = build_sell_list_url(str(i), minPrice)
            cItem_list = get_buyitem_list(url)
        except:
            pass

        if not cItem_list:
            print('Completed.')
            break
        else:
            item_list += cItem_list
            print('Page ', i, 'scraped')
        i += 1

    return item_list

def bucketCount(list):
    priceBuckets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in list:
        p = float(i.price[1:])
        if p <= 100:
            priceBuckets[0] += 1
        elif p <= 200:
            priceBuckets[1] += 1
        elif p <= 300:
            priceBuckets[2] += 1
        elif p <= 400:
            priceBuckets[3] += 1
        elif p <= 500:
            priceBuckets[4] += 1
        elif p<=600:
            priceBuckets[5] += 1
        elif p<=700:
            priceBuckets[6] += 1
        elif p<=800:
            priceBuckets[7] += 1
        elif p<= 900:
            priceBuckets[8] += 1
        elif p <= 1000:
            priceBuckets[9] += 1
        else:
            priceBuckets[10] += 1

    for i in priceBuckets:
        print(i, end=' ')

    for i in priceBuckets:
        print(i/len(list), end=' ')

def add_prices(df, bList, sList):


def _add_prices_helper(df, pList, col):
    for item in pList:
        row = df


sList = scrape_all_sell_list(20)

bList = scrape_all_buy_list('20')
bucketCount(bList)

#headers = {'Accept-Encoding': 'identity'} # Prevents the info gotten by .get to be zipped
#page = requests.get(build_buylist_url('1', '20'), headers=headers)
#soup = BeautifulSoup(page.content, 'html.parser')

#url = build_buylist_url('2', '20')
#soup = get_soup(url)
#forms = get_add_forms(soup)
#buyList = form_list_to_buylistItem_list(forms)

#for i in buyList:
 #   i.print()
  #  print('')

