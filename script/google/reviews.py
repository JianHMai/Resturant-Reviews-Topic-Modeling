from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
import time
import re

def write_into_csv(filename, header, data, type = 'w'):
  with open("./dataset/google/" + filename + ".csv", type, encoding='UTF8') as f:
    f.write(header)
    f.write('\n')

    for row in data:
      f.write(", ".join(row))
      f.write('\n')

def sort_by_newest_reviews(driver):
  # sort by newest reviews
  print("Sorting")
  sort_btn = driver.find_elements(By.CSS_SELECTOR, "button.S9kvJb")
  sort_btn[2].click()
  time.sleep(2)
  newest_option = driver.find_elements(By.CSS_SELECTOR, "li.nbpPqf-menu-x3Eknd")
  newest_option[1].click()
  time.sleep(3)

def scroll_to_bottom(driver, total_number_of_reviews):
  # Find scroll layout
  print("Scrolling")
  scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.section-scrollbox')
  scroll_val = total_number_of_reviews/4 if total_number_of_reviews < 260 else min((total_number_of_reviews/10 - 1), 40)

  # Scroll as many times as necessary to load all reviews
  for i in range(0,(round(scroll_val))):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    time.sleep(1)

def expand_all_reviews(driver):
  more_btns = driver.find_elements(By.CSS_SELECTOR, "button.ODSEW-KoToPc-ShBeI.gXqMYb-hSRGPd")
  for btn in more_btns:
    btn.click()
    time.sleep(1)

def get_restaurants_details(driver):
  # Get restaurant details
  name = driver.find_elements(By.CSS_SELECTOR, "h1.x3AX1-LfntMc-header-title-title>span")
  rating = driver.find_elements(By.CSS_SELECTOR, "div.x3AX1-LfntMc-header-title-ij8cu-haAclf span.aMPvhf-fI6EEc-KVuj8d")
  review_btn = driver.find_elements(By.CSS_SELECTOR, "div.x3AX1-LfntMc-header-title-ij8cu-haAclf button.Yr7JMd-pane-hSRGPd")
  cuisine = driver.find_elements(By.CSS_SELECTOR, "div.x3AX1-LfntMc-header-title-ij8cu-haAclf>div>div:nth-child(2)>span>span>button.Yr7JMd-pane-hSRGPd")
  address = driver.find_elements(By.CSS_SELECTOR, "div.dqIYcf-RWgCYc-text button div.QSFF4-text")
  safety_measure = driver.find_elements(By.CSS_SELECTOR, "div.dqIYcf-RWgCYc-text button div.QSFF4-text span:nth-child(2)")

  name = name[0].text if len(name) > 0 else ""
  rating = rating[0].text if len(rating) > 0 else ""
  total_number_of_reviews = "".join(re.findall(r'\d+', review_btn[0].text)) if len(review_btn) > 0 else ""
  cuisine = cuisine[0].text if len(cuisine) > 0 else ""
  address = re.sub(r',', '', address[0].text) if len(address) > 0 else ""
  safety_measure = safety_measure[0].text if len(safety_measure) > 0 else ""
  # restaurant_details.append([name, rating, total_number_of_reviews, cuisine, address, safety_measure])
  restaurant_details = [[name, rating, total_number_of_reviews, cuisine, address, safety_measure]]
  write_into_csv("restaurants-details", "name, rating, reviews, cuisine, address, safety measures", restaurant_details, type = 'a')
  return name, review_btn, total_number_of_reviews

def get_restaurants_with_reviews(driver, restaurants):
  try:
    for restaurant_url in restaurants:
      driver.get(restaurant_url)
      time.sleep(3)

      # Get restaurant details
      # name, review_btn, total_number_of_reviews = get_restaurants_details(driver)
      name = driver.find_elements(By.CSS_SELECTOR, "h1.x3AX1-LfntMc-header-title-title>span")
      name = name[0].text if len(name) > 0 else ""
      review_btn = driver.find_elements(By.CSS_SELECTOR, "div.x3AX1-LfntMc-header-title-ij8cu-haAclf button.Yr7JMd-pane-hSRGPd")
      total_number_of_reviews = "".join(re.findall(r'\d+', review_btn[0].text)) if len(review_btn) > 0 else ""

      print("======================================================")
      print(name)
      print("======================================================")

      # open review page
      if len(review_btn) > 0:
        review_btn[0].click()
        time.sleep(1)
      else:
        continue

      sort_by_newest_reviews(driver)
      scroll_to_bottom(driver, int(total_number_of_reviews))
      print("Expand all reviews")
      expand_all_reviews(driver)

      soup = BeautifulSoup(driver.page_source, 'html.parser')
      review_list = soup.select("div.siAUzd-neVct>div.ODSEW-ShBeI")
      reviews = []
      print("Reading Reviews", len(review_list))
      for review in review_list:
        author = review.select("div.ODSEW-ShBeI-title>span")[0].get_text()
        text = review.select("div.ODSEW-ShBeI-ShBeI-content>span.ODSEW-ShBeI-text")[0].get_text()
        date = review.select("span.ODSEW-ShBeI-RgZmSc-date")[0].get_text()
        rating = review.select("div.ODSEW-ShBeI-jfdpUb>span.ODSEW-ShBeI-H1e3jb>img.ODSEW-ShBeI-fI6EEc-active")
        reviews.append([author, date, str(len(rating)), repr(text)])
        time.sleep(1)

      write_into_csv('reviews/' + slugify(name), "author, date, rating, text", reviews)
      print("Fetched reviews for {}".format(name))
  except Exception as e:
    print("Error occurred", e)

if __name__ == "__main__":
  print("======== SCRAPE GOOGLE REVIEWS =========")
  t0 = time.time()

  # Chrome Web driver
  # chromeOptions = webdriver.ChromeOptions()
  # chromeOptions.add_argument("--headless") # open chrome in headless mode
  # driver = webdriver.Chrome(executable_path="script/google/chromedriver" , options=chromeOptions)

  # Safari Webdriver
  driver = webdriver.Safari()

  driver.implicitly_wait(3)  # set implict wait

  restaurants = None
  with open("./dataset/google/restaurants.csv", 'r') as f:
    restaurants = f.readlines()

  # get_restaurants_with_reviews(driver, restaurants)
  get_restaurants_with_reviews(driver, restaurants[111:112])

  t1 = time.time()
  print(f"{t1-t0} seconds.")

  driver.quit()
