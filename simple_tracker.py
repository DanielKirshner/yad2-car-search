# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

from yad2_config import(
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    build_url,
    CARS_MODELS,
    FILTERS,
    BASE_URL,
    DIRECTORY
)

class Yad2CarAPI:
    def __init__(self, base_url, cars_models, filters, with_image, with_price):
        self.base_url = base_url
        self.cars_models = cars_models
        self.price = filters['price']
        self.year = filters['year']
        self.areas = filters['area']
        self.gears = filters['gear']
        self.with_image = with_image,
        self.with_price = with_price
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)


    def run(self):
        print("Starting Script.....")
        print(f"Looking for {self.cars_models}...")
        products = self.get_product()
        with open('output.json', 'w', encoding='utf8') as outfile:
            json.dump(products, outfile, ensure_ascii=False)
        time.sleep(3)
        self.driver.quit()
        print('FINISHED!!!')
        

    def get_product(self):
        done = False
        self.driver.get(build_url(self.base_url, self.price, self.year, self.cars_models, self.areas, self.gears, self.with_image, self.with_price))
        time.sleep(1)
        products = { }
        while not done:
            result_list = self.driver.find_elements(By.CLASS_NAME, 'feeditem')  # Updated for Selenium 4
            for element in result_list:
                try:
                    element.click()
                    time.sleep(3)
                    feed = element.find_element(By.XPATH, './/div')  # Updated for Selenium 4
                    id = feed.get_attribute('id').split('_')[2]
                    feed2 = self.driver.find_element(By.ID, f'accordion_wide_{id}').find_element(By.ID, 'share_item_new-tab').find_element(By.XPATH, './/a')  # Updated for Selenium 4
                    link = feed2.get_attribute('href')
                    title = feed.find_element(By.CLASS_NAME, 'title').text  # Updated for Selenium 4
                    year = feed.find_element(By.ID, f'data_year_{id}').text  # Updated for Selenium 4
                    hand = feed.find_element(By.ID, f'data_hand_{id}').text  # Updated for Selenium 4
                    price = feed.find_element(By.ID, f'feed_item_{id}_price').text  # Updated for Selenium 4
                    engine_size = feed.find_element(By.ID, f'data_engine_size_{id}').text  # Updated for Selenium 4
                    location = feed.find_element(By.CLASS_NAME, 'upper_info_text').text  # Updated for Selenium 4
                    subtitle = ' '.join(feed.find_element(By.CLASS_NAME, 'subtitle').text.split(' ')[1:4])  # Updated for Selenium 4
                    color = feed.find_element(By.ID, 'more_details_color').find_element(By.XPATH, './/span').text  # Updated for Selenium 4
                    owner = feed.find_element(By.ID, 'more_details_ownerID').find_element(By.XPATH, './/span').text  # Updated for Selenium 4
                    kilometer = feed.find_element(By.ID, 'more_details_kilometers').find_element(By.XPATH, './/span').text  # Updated for Selenium 4
                    detail = feed.find_element(By.CLASS_NAME, 'details_text').text  # Updated for Selenium 4
                    # on_road = feed.find_element_by_id('more_details_month').find_element_by_xpath('.//span').text
                    # test = feed.find_element_by_id('more_details_testDate').find_element_by_xpath('.//span').text
                    p = [{
                                'Description': subtitle,
                                'Link': link,
                                'Year': year,
                                'Hand': hand,
                                'Price': price,
                                'Location': location,
                                'Engine Size': engine_size,
                                'Kilometer': kilometer,
                                'Owner': owner,
                                'Color': color,
                                'Details': detail,
                                # 'On Road Since': on_road,
                                # 'Test date': test,
                        }]
                    if title in products:
                        products[title].append(p)
                    else:
                        products[title] = p

                except Exception as e:
                    print(e)
                    pass
            try:    
                nextButon = self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/main/div/div[4]/div[6]/div[2]/div[4]/a[2]')  # Updated for Selenium 4
                nextPage = nextButon.get_attribute('href')
                if nextPage == self.driver.current_url:
                    done = True
                else:
                    self.driver.get(nextPage)
            except Exception:
                done = True
        return products


if __name__ == "__main__":
    with_image = True
    with_price = True
    yad2 = Yad2CarAPI(BASE_URL, CARS_MODELS, FILTERS, with_image, with_price)
    yad2.run()