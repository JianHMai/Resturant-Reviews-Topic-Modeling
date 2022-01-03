import urllib.parse
import requests
import json
import re

UNWRANGLE_API_KEY = "cf98ca70e84876fa56ccca58db02c1e30041608f"
YELP_HEADERS = {'Authorization': 'Bearer 0rbqP6l7tlYejcq31zupON3mjMJJTZ4SWUhP5SOXUNzxYH-MVh3hRieJ8EAWclOIKclyoJmNAIwZjPXe-BfEHC_8OvchUnvXa9S2Rkiojcq4_xqm01K2-wk5u9aBYXYx'}

ALIASES = [
  'fiore-deli-of-hoboken-hoboken', 'the-cuban-restaurant-and-bar-hoboken-2', 'la-isla-restaurant-hoboken', 'karma-kafe-hoboken', 'vitos-italian-deli-hoboken', 'mamouns-falafel-hoboken-hoboken-2', 'amandas-restaurant-hoboken-2', 'm-and-p-biancamano-hoboken', 'pilsener-haus-and-biergarten-hoboken', 'anthony-davids-hoboken', 'bwè-kafe-hoboken', 'zacks-oak-bar-and-restaurant-hoboken', 'grand-vin-hoboken', 'ali-baba-hoboken-2', 'choc-o-pain-hoboken-9', 'benny-tudinos-pizzeria-hoboken', 'elysian-cafe-hoboken', 'margheritas-hoboken', 'la-casa-hoboken', 'los-tacos-no-1-new-york', 'satay-malaysian-cuisine-hoboken-2', 'otto-strada-hoboken-3', 'saku-hoboken-2', 'empire-coffee-and-tea-company-hoboken', 'antique-bar-and-bakery-hoboken-2', 'grimaldis-hoboken', 'old-german-bakery-hoboken', 'carlos-bakery-hoboken-9', 'sweet-hoboken', 'black-rail-coffee-hoboken', 'johnny-pepperoni-hoboken', 'tony-boloneys-hoboken-hoboken', 'alfalfa-hoboken', 'augustinos-hoboken', 'baking-mama-hoboken', 'turning-point-of-hoboken-hoboken', 'onieals-hoboken', 'court-street-restaurant-and-bar-hoboken', 'robongi-hoboken', 'okinawa-sushi-and-grill-hoboken-2', 'chango-kitchen-hoboken', 'the-brass-rail-hoboken-hoboken', 'il-tavolo-di-palmisano-hoboken-2', 'rosticeria-da-gigi-hoboken', 'carpe-diem-pub-and-restaurant-hoboken-2', 'barbès-restaurant-hoboken', 'halifax-hoboken-2', 'tosti-cafe-and-kitchen-hoboken', 'morans-hoboken', 'arthurs-steaks-hoboken', 'bin-14-hoboken', 'bareburger-hoboken-hoboken', 'napolis-pizza-hoboken-2', 'purely-juiced-hoboken', 'seven-valleys-hoboken', 'san-giuseppe-hoboken', 'midtown-philly-steaks-hoboken-2', 'hidden-grounds-coffee-hoboken-6', 'o-bagel-hoboken', 'muteki-ramen-hoboken', 'bluestone-lane-hoboken', 'shaka-bowl-hoboken', 'illuzion-hoboken', 'leos-grandevous-hoboken', 'del-friscos-grille-hoboken', 'orale-mexican-kitchen-hoboken', 'la-isla-restaurant-uptown-hoboken', 'bean-vault-coffee-hoboken', 'piki-poké-hoboken-2', 'frank-sinatra-park-hoboken', 'south-street-fish-and-ramen-co-hoboken', 'house-of-que-hoboken-2', 'gogi-grill-hoboken-hoboken-2', 'sushi-lounge-hoboken', 'zero-otto-uno-cafe-hoboken', 'green-pear-cafe-hoboken', 'wafels-and-dinges-new-york', 'greektown-hoboken-3', 'chicken-factory-hoboken-2', 'kung-fu-tea-hoboken', 'empyrean-indian-kitchen-and-bar-hoboken-2', 'mikie-squared-bar-and-grill-hoboken', 'pier-c-hoboken', 'dino-and-harrys-steak-house-hoboken-5', 'happy-vegans-hoboken-2', 'alessios-cafe-gelato-pizza-hoboken', 'luca-brasis-deli-hoboken-151', 'mulligans-hoboken', 'cafe-michelina-hoboken', 'napolis-pizza-hoboken', 'the-madison-bar-and-grill-hoboken', 'panello-hoboken', 't-thai-hoboken', 'keming-restaurant-hoboken-2', 'piccolos-cheesesteaks-hoboken-hoboken', 'quality-greens-kitchen-hoboken', 'acai-ya-later-hoboken', 'vivi-bubble-tea-hoboken', 'blue-eyes-restaurant-hoboken', 'sorellina-hoboken', 'curry-up-now-hoboken', 'dozzino-hoboken', 'gong-cha-hoboken', 'ayame-hibachi-and-sushi-hoboken', 'northern-soul-kitchen-and-bar-hoboken', 'gfg-bakery-cafe-hoboken', 'dolce-and-salato-hoboken', 'pier-a-park-hoboken', 'city-bistro-hoboken', 'cucina-saporito-hoboken', 'la-bouche-hoboken-3', 'apulia-hoboken', 'black-bear-bar-and-grill-hoboken', 'hoboken-hot-bagels-hoboken', 'honeygrow-hoboken', 'losurdos-italian-bakery-and-deli-hoboken', 'the-lobster-place-new-york-2', 'ritas-italian-ice-hoboken', 'juns-macaron-gelato-hoboken', 'cork-city-hoboken', 'mojo-coffee-company-hoboken', 'belo-bar-hoboken', 'lo-fatt-chow-hoboken', 'the-stewed-cow-hoboken', 'touch-the-heart-hoboken', 'sri-thai-thai-restaurant-hoboken', 'ainsworth-hoboken-hoboken', 'precious-japanese-and-chinese-cuisine-hoboken', 'east-la-hoboken', 'djura-grill-jersey-city', 'lolas-hoboken', 'stingray-lounge-uptown-hoboken-2', 'giovannis-pizzeria-and-restaurant-hoboken-6', 'mango-mango-hoboken', 'pizza-republic-hoboken', 'shokudo-hoboken', 'doms-bakery-grand-hoboken', 'tenth-street-pasta-and-pizza-hoboken', 'union-hall-hoboken', 'mr-wraps-hoboken', 'pho-nomenon-noodle-and-grill-hoboken', 'finnegans-pub-hoboken-2', 'prato-bakery-hoboken-2', '10th-and-willow-bar-and-grill-hoboken', 'yeung-ii-sushi-asian-cuisine-hoboken-61', 'urban-coalhouse-pizza-bar-hoboken-4', 'chart-house-weehawken', 'basiles-pizza-hoboken', 'malatesta-trattoria-new-york', 'me-casa-foods-jersey-city', 'the-brick-fire-baked-pizza-hoboken-3', 'amanda-bananas-hoboken', 'marios-classic-pizza-hoboken', 'south-lions-hoboken-2', 'jeffersons-coffee-hoboken-6', 'thomas-ice-cream-cafe-hoboken-2', 'employees-only-new-york', 'wicked-wolf-tavern-hoboken', 'the-hive-hoboken', 'jeju-noodle-bar-new-york', 'baja-mexican-cuisine-hoboken-2', 'jps-bagel-express-hoboken', 'ben-and-jerry-s-hoboken', 'louise-and-jerrys-hoboken', 'malibu-diner-hoboken', 'the-shepherd-and-the-knucklehead-of-hoboken-hoboken-2', 'andrea-salumeria-jersey-city', 'pico-taco-hoboken-2', 'madd-hatter-hoboken-3', 'cafe-vista-hoboken-2', 'frying-pan-new-york', 'shaka-bowl-hoboken-2', 'griot-cafe-jersey-city', 'ds-soul-full-cafe-hoboken', 'scotts-pizza-tours-new-york', 'the-cliff-jersey-city', 'royal-grill-halal-food-new-york-2', 'modcup-coffee-jersey-city-2', 'en-japanese-brasserie-new-york', 'perry-st-new-york', 'hidden-grounds-coffee-hoboken-4', '16-handles-hoboken', 'dark-side-of-the-moo-jersey-city-jersey-city', 'dulce-de-leche-bakery-jersey-city', 'farside-tavern-hoboken', 'jeffersons-coffee-hoboken', 'fig-and-olive-new-york-12', 'remi-flower-and-coffee-new-york-2', 'ubu-hoboken', 'corto-jersey-city', 'shoprite-of-hoboken-hoboken', 'lisas-italian-deli-hoboken', 'mysttik-masaala-new-york-13', 'willie-mcbrides-hoboken', 'hudson-river-waterfront-walkway-hoboken', 'bangkok-city-thai-restaurant-hoboken', 'catch-nyc-new-york', '9-11-tribute-museum-new-york', 'sirenetta-seafood-and-raw-bar-hoboken', 'the-little-grocery-hoboken-3', 'fox-and-crow-jersey-city', 'monroes-hoboken', 'yukis-coffee-and-bakery-hoboken', 'milk-sugar-love-jersey-city-2', 'bang-cookies-jersey-city-3', 'decoy-new-york', 'rumba-cubana-jersey-city', 'stk-steakhouse-downtown-new-york', 'green-rock-tap-and-grill-hoboken', 'pastrami-house-hoboken', 'mcswiggans-pub-hoboken', 'texas-arizona-hoboken', 'el-chilango-taqueria-jersey-city-3', 'mémé-mediterranean-new-york-4', 'panera-bread-hoboken', 'rh-rooftop-restaurant-new-york-new-york-2', 'rumbas-cafe-jersey-city', 'adoro-lei-new-york', 'the-hamilton-inn-jersey-city', 'the-ale-house-hoboken-2', 'insomnia-cookies-hoboken', 'the-roost-outpost-hoboken-3', 'city-of-saints-coffee-roasters-hoboken', 'whitney-museum-of-american-art-new-york-4', 'artichoke-basilles-pizza-new-york-9', 'the-tippler-new-york', 'l-arte-del-gelato-new-york-4', 'the-hutton-jersey-city', 'grubbs-take-away-hoboken', 'tornas-pizzeria-hoboken', 'simò-pizza-new-york-4', 'intersect-by-lexus-nyc-new-york', 'lelabar-new-york-2', 'corkscrew-bar-jersey-city', 'hudson-clearwater-new-york', 'the-clam-new-york', 'joboken-cafe-hoboken-2', 'renatos-pizza-masters-jersey-city', 'westville-hudson-new-york', 'the-standard-grill-new-york-3']

def get_restaurants(total=240, limit=40, call_api=False, write_to_csv=False):
  scraped_bizs = []
  if(call_api):
    pages = int(round(total/limit))
    start = 0
    end = pages - 1
    while(start <= end):
      offset = start * limit
      parameters = { 'location':'Hoboken', 'limit' : limit, 'offset': offset }
      query_url = "https://api.yelp.com/v3/businesses/search"

      response = requests.get(query_url, headers=YELP_HEADERS, params=parameters)
      data=json.loads(response.text)

      businesses = data['businesses']
      for biz in businesses:
        try:
          bizObj = {
            'alias': biz['alias'] if 'alias' in biz else '',
            'name': biz['name'] if 'name' in biz else '',
            'review_count': biz['review_count'] if 'review_count' in biz else '',
            'price': biz['price'] if 'price' in biz else '',
            'rating': biz['rating'] if 'rating' in biz else '',
            'transactions':" ".join(biz['transactions']),
            'location': " ".join(biz['location']['display_address']),
            'cuisine': " ".join([category['alias'] for category in biz['categories']])
            }
          scraped_bizs.append(bizObj)
        except Exception as err:
          print(err)
      start += 1

  if(write_to_csv):
    with open("./dataset/yelp/restaurant_list.csv", 'w', encoding='UTF8') as f:
      f.write("name,alias,review_count,price,rating,location,transactions,cuisine")
      f.write('\n')

      for biz in scraped_bizs:
        alias = biz["alias"]
        name = biz["name"]
        review_count = biz["review_count"]
        price = biz["price"]
        rating = biz["rating"]
        location = re.sub(r",", "", biz["location"])
        transactions = biz["transactions"]
        cuisine = biz["cuisine"]

        row = "{0},{1},{2},{3},{4},{5},{6},{7}".format(name, alias, review_count, price, rating, location, transactions, cuisine)
        f.write(row)
        f.write('\n')

  return [biz['alias'] for biz in scraped_bizs] if call_api else ALIASES

def get_restaurant_reviews(pages=40, call_api = False, write_to_csv = False):
  restaurant_aliases = ALIASES

  # for each restaurant fetch reviews and store reviews in separate file labelled by restaurant name
  if(call_api):
    for alias in restaurant_aliases:
      print("=============================================")
      print("reading from api~!! for " + alias)
      start = 1
      end = pages
      # call this api when all set because it consumes free credits
      while(start <= end):
        scraped_reviews = []
        print("reading page number " + str(start) + "!!!")
        try:
          encoded_url = urllib.parse.quote("https://www.yelp.com/biz/"+alias)
          url = "https://data.unwrangle.com/api/getter/?url="+encoded_url+"&lang=en&page="+str(start)+"&api_key="+UNWRANGLE_API_KEY
          response = requests.get(url)
          if(response and response.status_code == 200):
            data = json.loads(response.text)
            reviews = data["reviews"]

            if (len(reviews) < 1):
              break

            for review in enumerate(reviews):
              scraped_reviews.append(
                {
                "date": review[1]["date"],
                "text": review[1]["review_text"],
                "rating": review[1]["rating"]
                }
              )

            if(write_to_csv):
              filename= "./dataset/yelp/reviews/" + alias + "_reviews.csv"
              with open(filename, 'a', encoding='UTF8') as f:
                print("writing " + str(len(scraped_reviews)) + " reviews to csv !! ===> " + filename)
                for review in scraped_reviews:
                  date = review["date"]
                  rating = review["rating"]
                  text = review["text"]
                  row = "{0},{1},{2}".format(date, rating, text)
                  f.write(row)
                  f.write('\n')

        except Exception as error:
          print(error)
        start += 1
      print("=============================================")
  else:
    print("If you want to scrape the data, check and pass the parameters very carefully")

if __name__ == "__main__":
  print("======== SCRAPE YELP REVIEWS =========")
  get_restaurant_reviews(pages=50)
  # get_restaurant_reviews(pages=50, call_api=True, write_to_csv=True)
