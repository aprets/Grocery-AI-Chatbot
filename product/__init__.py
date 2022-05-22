import requests, json, base64, re, pickle
from bs4 import BeautifulSoup
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

    sainsburys_data = self.hitSainsburysAPI(descriptionUrl)

    if sainsburys_data is not None:
      self.s_labels = sainsburys_data["labels"]
      self.s_rating = sainsburys_data["rating"]
      self.s_brand = sainsburys_data["brand"]
      self.s_reviews = sainsburys_data["reviews"]
      self.s_description = sainsburys_data["description"]
      self.s_origin_country = sainsburys_data["origin_country"] 
      self.s_ingredients = sainsburys_data["ingredients"]
      self.s_nutrition = sainsburys_data["nutrition"]
    else:
      self.s_labels = None
      self.s_rating = None
      self.s_brand = None
      self.s_reviews = None
      self.s_description = None
      self.s_origin_country = None
      self.s_ingredients = None
      self.s_nutrition = None


  def toString(self):
    return ', '.join("%s: %s" % item for item in vars(self).items())


  def hitSainsburysAPI(self, product_url):
    if product_url is None:
      print("No product_url found for", self.name)
      return None

    if "gol-ui" not in product_url:
      print("Incompatible product_url found for", self.name)
      return None
    
    # Helper Functions
    def getLabels(data):
      # Get labels from all sources
      s_labels = []
      s_labels.append([x["label"] for x in data["breadcrumbs"]])
      s_labels.append([x["name"] for x in data["categories"]])

      s_labels.append(data["product_type"])
      s_labels.append(data["zone"])

      if data["is_alcoholic"] == "true":
          s_labels.append("alcoholic")

      if data["is_intolerant"] == "true":
          s_labels.append("intolerant")

      if data["is_mhra"] == "true":
          s_labels.append("mhra")

      return s_labels


    # Parse base64 html object returned by Sainsburys API
    def parseDescription(data):
      html = base64.b64decode(data)
      s_soup = BeautifulSoup(html, 'html.parser')

      def getAllTagContents(tagGroup):
        s = ""
        for tag in tagGroup.find(["p"]):
          s += str(tag.getText()).strip() + ". "

        return s.strip(" ").replace('\n', " ").replace('. .', ".")


      def getDesc(soup):
        desc = soup.find("h3", string="Description").find_next()
        s = ""
        for tag in desc.find(["p"]):
          s += str(tag.string).strip() + ". "

        return s.strip(" ").replace('\n', " ").replace('. .', ".")
        

      def getOrigin(soup):
        country_info = soup.find("h3", string="Country of Origin").find_next()
        s = ""
        for tag in country_info.find(["p"]):
          s += str(tag.string).strip() + ". "

        return s.strip(" ").replace('\n', " ").replace('. .', ".")


      def getIngredients(soup):
        ingredients = soup.find("h3", string="Ingredients").find_next()
        ingredients = getAllTagContents(ingredients)

        pattern = re.compile("ingredients", re.IGNORECASE)

        # Clean up the ingredients string and extract single tokens
        ingredients = re.sub(r'[^a-zA-Z ,]', '', ingredients)
        ingredients = pattern.sub("", ingredients).replace("  ", ",")
        ingredients = list(filter(lambda i: i not in ['', ' '], ingredients.split(",")))
        ingredients = [x.strip().lstrip() for x in ingredients]
        return ingredients


      def getNutrients(soup):
        nutrition_info = soup.find("h3", string="Nutrition").find_next()
        block = nutrition_info.find("ul", {"class": "lozengeBlock"})
        nutrients = {"ENERGY": None,
                    "FAT": None,
                    "SATURATES": None,
                    "SUGARS": None,
                    "SALT": None}
        if block:
          nutrients["ENERGY"] = str(block.find("li",{"class": "energy"}).find("div", {"class": "percentage"}).text).strip('%\n')
          nutrients["FAT"] = str(block.find("li",{"class": "fat"}).find("div", {"class": "percentage"}).text).strip('%\n')
          nutrients["SATURATES"] = str(block.find("li",{"class": "saturates"}).find("div", {"class": "percentage"}).text).strip('%\n')
          nutrients["SUGARS"] = str(block.find("li",{"class": "sugars"}).find("div", {"class": "percentage"}).text).strip('%\n')
          nutrients["SALT"] = str(block.find("li",{"class": "salt"}).find("div", {"class": "percentage"}).text).strip('%\n')

        return nutrients
        

      return getDesc(s_soup), getOrigin(s_soup), getIngredients(s_soup), getNutrients(s_soup)


    def getReviews(self, reviewId):
      # Get all product reviews as a concatenation of their title and body      
      reviews = []

      url = f"https://reviews.sainsburys-groceries.co.uk/data/reviews.json?ApiVersion=5.4&Filter=ProductId:{reviewId}-P&Offset=0&Limit=100"
      data = json.loads(str(requests.get(url, headers = user_agent).text))
      
      for review in data["Results"]:
        text = str(review["Title"]) + " " + str(review["ReviewText"])
        reviews.append(text)

      if len(reviews) == 0:
        reviews = None

      return reviews


    # Start scraping this product
    base_url = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]="

    try:
      query_string = product_url[product_url.index("/product/")+9:]
    except(Exception):
      query_string = product_url[product_url.index("/Product/")+9:]

    query_url = base_url + query_string

    data = requests.get(query_url, headers = user_agent).text

    if "CloudFront" in data:
      print("Oops, IP banned. Issue getting", query_string)
      return None

    data = json.loads(str(data))
    
    sainsburys_data = {}
    result = parseDescription(data["products"][0]["details_html"])
    sainsburys_data["description"] = result[0]
    sainsburys_data["origin_country"] = result[1]
    sainsburys_data["ingredients"] = result[2]
    sainsburys_data["nutrition"] = result[3] 

    sainsburys_data["labels"] = getLabels(data)
    sainsburys_data["rating"] = data["reviews"]["average_rating"]
    sainsburys_data["brand"] = [x for x in data["attributes"]["brand"]]
    sainsburys_data["reviews"] = getReviews(data["reviews"]["product_uid"])
    sainsburys_data["description"] = sainsburys_data["description"] + " " + " ".join([x for x in data["description"]])

    return sainsburys_data

with open("product/sainsburys_dump.pkl", "rb") as fp:
    menu = pickle.load(fp)