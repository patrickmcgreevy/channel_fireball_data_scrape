import requests
from bs4 import BeautifulSoup
import pandas as pd


class buylistItem:
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
        self.price = form['data-price']
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

    return start + pageNum + mid + minPrice + end

def get_soup(url):
    headers = {'Accept-Encoding': 'identity'}
    return BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')


def get_add_forms(soup):
    return soup.find_all('form', class_='add-to-cart-form')


def form_list_to_buylistItem_list(form_list):
    return [buylistItem(i) for i in form_list]


#Pass in the url and the buylist/selllist function you want to use
def get_buyitem_list(url):
    soup = get_soup(url)
    form_list = get_add_forms(soup)
    return form_list_to_buylistItem_list(form_list)

def scrape_all_buy_list(minPrice):
    item_list = []
    i = 1
    while True:
        url = build_buylist_url(i, minPrice)
        cItem_list = get_buyitem_list(url)
        if not cItem_list:
            break
        else:
            item_list += cItem_list
        i += 1

    return item_list


#headers = {'Accept-Encoding': 'identity'} # Prevents the info gotten by .get to be zipped
#page = requests.get(build_buylist_url('1', '20'), headers=headers)
#soup = BeautifulSoup(page.content, 'html.parser')

url = build_buylist_url('2', '20')
soup = get_soup(url)
forms = get_add_forms(soup)
buyList = form_list_to_buylistItem_list(forms)

for i in buyList:
    i.print()
    print('')

