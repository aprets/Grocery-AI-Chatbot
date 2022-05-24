import typing
import json, base64, re, pickle
# from bs4 import BeautifulSoup
from pprint import pprint
from .product_helper import menu_item, Menu

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'menu_item':
            return menu_item
        return super().find_class(module, name)

with open("product/sainsburys_dump.pkl", "rb") as fp:
    raw_menu: typing.List[menu_item] = CustomUnpickler(fp).load()

menu = Menu(raw_menu)