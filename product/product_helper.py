import typing
from Levenshtein import distance

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


class Menu():
    def __init__(self, menu_data):
        self.items = menu_data
        self.attr_by_priority = ["name", "categoryName", "s_labels", "s_brand"]


    def get_top_n_items(self, partial_name: str, n: int = 10)-> typing.List[menu_item]:
        """ Return the top ten items in the menu which relate to the query"""
        items = []
        for c in self.attr_by_priority:
            items += [i for i in self.items if partial_name.lower() in str(getattr(i,c)).lower()]
            if len(items) >= n:
                break

        return sorted(items[:n], key=lambda i: i.s_rating if i.s_rating else 0, reverse=True)

    
    def select_most_likely(self, item_list, partial_name):
        return sorted(item_list, 
                        key=lambda i: distance(
                            i.name.lower(),partial_name.lower()) - \
                            abs(len(item_list)-len(partial_name)), 
                        reverse=True)[0]