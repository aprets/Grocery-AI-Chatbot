import typing
import json, base64, re, pickle
# from bs4 import BeautifulSoup
from pprint import pprint
from product_helper import menu_item
user_agent = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'menu_item':
            return menu_item
        return super().find_class(module, name)

with open("product/sainsburys_dump.pkl", "rb") as fp:
    menu: typing.List[menu_item] = CustomUnpickler(fp).load()