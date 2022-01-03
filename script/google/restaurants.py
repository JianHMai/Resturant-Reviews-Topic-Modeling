import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def write_into_csv(filename, header, data):
  unique_set = set(data)
  data = list(unique_set)
  with open("./dataset/" + filename + ".csv", 'w', encoding='UTF8') as f:
    f.write(header)
    f.write('\n')

    for name in data:
      f.write(name)
      f.write('\n')

def scroll_to_bottom(driver):
  # Find scroll layout
  scrollable_div = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')

  # Scroll as many times as necessary to load all reviews
  for i in range(0,(round(22))):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    time.sleep(2)

def get_restaurants(driver, page_url, limit = 3):
  try:
    restaurant_names = []
    driver.get(page_url)

    for x in range(limit - 1):
      time.sleep(3)

      scroll_to_bottom(driver)

      # Get restaurant names
      # list = driver.find_elements(By.CSS_SELECTOR, "div.qBF1Pd-haAclf>div>span")
      link = driver.find_elements(By.CSS_SELECTOR, "a.a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")

      for x in link:
        # restaurant_names.append(x.text)
        restaurant_names.append(x.get_attribute("href"))
        # print(x.get_attribute("href"))

      next_btn_url = driver.find_element(By.XPATH, '//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')
      if next_btn_url:
        next_btn_url.click()
      else:
        break

    write_into_csv("restaurants", "names", restaurant_names)
    print("created restaurants.csv file to save restaurants names from Hoboken")

  except Exception as e:
    print(e)
  return

if __name__ == "__main__":
  print("======== Test =========")

  driver = webdriver.Safari()
  driver.implicitly_wait(3)  # set implict wait

  page_url = 'https://www.google.com/maps/search/restaurants+in+Hoboken+City,+Hoboken,+NJ/@40.7475851,-74.0405987,15z'

  get_restaurants(driver, page_url, limit = 15)

  driver.quit()