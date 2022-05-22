import typing
import json, base64, re, pickle
# from bs4 import BeautifulSoup
from pprint import pprint

user_agent = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}

class menu_item():
  def __init__(self, id, 
               name, categoryId, 
               modifierIds, price, 
               popular, available, 
               descriptionUrl, imageUrl, 
               categories):
    
    self.id = id
    self.name = name
    self.categoryName = categories[categoryId]
    self.modifierIds = modifierIds
    self.price = price
    self.popular = popular
    self.available = available
    self.imageUrl = imageUrl


    self.s_labels = None
    self.s_rating = None
    self.s_brand = None
    self.s_reviews = None
    self.s_description = None
    self.s_origin_country = None
    self.s_ingredients = None
    self.s_nutrition = None


  def __str__(self):
    return ', '.join("%s: %s" % item for item in vars(self).items())



class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'menu_item':
            return menu_item
        return super().find_class(module, name)

with open("product/sainsburys_dump.pkl", "rb") as fp:
    menu: typing.List[menu_item] = CustomUnpickler(fp).load()