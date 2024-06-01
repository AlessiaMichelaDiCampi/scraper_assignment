import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
from deep_translator import GoogleTranslator
sys.path.append("C:/Users/Alexis/Desktop/scraper_assignment/scrapers")
from selenium import webdriver
from abstract.abstract_scraper import AbstractScraper
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import datetime
import json


class NotinoScraper(AbstractScraper):

    def __init__(self, retailer, country):
        super().__init__(retailer, country)
        self.base_url = f"{country}"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/"
        })

    def scrape_with_selenium(self, transl):


        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")  

        driver = webdriver.Firefox()
        url = f"{self.base_url}/"+transl+"/"
        driver.get(url)


        soup = BeautifulSoup(driver.page_source, 'html.parser')
        error_page = soup.find("div", class_="error-page")
        if error_page:
            AbstractScraper.log_error("Error: Page not found, word" + transl +" not correct - pass" )

        #accept cookies
        wait = WebDriverWait(driver, 10)

        try:
            AbstractScraper.log_info("Accepting cookies")
            accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_button.click()
        except TimeoutException:
            # Handle the case where the button is not found within the timeout period
            AbstractScraper.log_info("Accept button not found within the timeout period. Continuing...")
    
     

        products_data = []
        try:
            while True:
                
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-bSstmL.sc-bYpRZF.iJzxKb.llgfxg.styled__StyledProductTile-sc-1i2ozu3-0.dhBqlM')))
                #soup = BeautifulSoup(driver.page_source, 'html.parser')
                products = soup.find_all("div", class_="sc-bSstmL sc-bYpRZF iJzxKb llgfxg styled__StyledProductTile-sc-1i2ozu3-0 dhBqlM")
                #products details
                for product in products:
                    
                    brand_elem = product.find("h2", class_="sc-guDLey sc-jPpdYo kbBsIA dloLns")
                    product_name_elem = product.find("h3", class_="sc-dmyCSP sc-ftxyOh eDlssm icLilU")
                    description_elem = product.find("p", class_="sc-FjMCv hnrOiP")
                    price_elem = product.find("span", class_="sc-hhyKGa sc-gYrqIg iwwcvf dOVzXY")
                    currency_elem = product.find("span", class_="sc-hhyKGa sc-cCzLxZ jOWcPO idiEkB")
                    image_elem = product.find("img")
                    url_elem = product.find("a")
                    promo_elem = product.find("span", class_="styled__DiscountValue-sc-1b3ggfp-1 jWXmOz")
                    code_elem = product.find("span", class_="styled__StyledDiscountCode-sc-1i2ozu3-1 gfxrfw")
                    brand = brand_elem.text.strip() if brand_elem else ''
                    currency = currency_elem.text.strip() if currency_elem else ''
                    product_name = product_name_elem.text.strip() if product_name_elem else ''
                    description = description_elem.text.strip() if description_elem else ''
                    price = price_elem.get_text(strip=True) if price_elem else 'not_available' #when there is no price the product is not available
                    image = image_elem["src"] if image_elem else ''
                    url = url_elem["href"] if url_elem else ''
                    promo = promo_elem.text.strip() if promo_elem else ''
                    code = code_elem.text.strip() if code_elem else ''

                    products_data.append({
                        "Product Name": product_name,
                        "Brand": brand,
                        "Description": description,
                        "Price": price,
                        "Currency": currency,
                        "URL": url,
                        "Image": image,
                        "Country": self.country,
                        "Promo": promo,
                        "Code": code,
                        "Scraped At": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })

                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="page-button-wrapper"].nextPage'))
                    )
                    next_button.click()
                    AbstractScraper.log_info("Clicked next page")
                    time.sleep(2) 
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-bSstmL.sc-bYpRZF.iJzxKb.llgfxg.styled__StyledProductTile-sc-1i2ozu3-0.dhBqlM'))
                    )
                except TimeoutException:
                    AbstractScraper.log_info("End of pages")
                    break
               
        except TimeoutException:
            AbstractScraper.log_error("End of pages - Timeout")
            pass

        products_df = pd.DataFrame(products_data)

        driver.quit()
        return products_df


 #This function contains the list of many countries tha i want to scrap. 
 #The acronyms for each country are saved within a list that will be passed on and for each country I will output the translation of the word ‘toothpaste’ so that I can access as many Notinos as I want and visit the toothpaste page. 
def all_countries(countries):  
    translated= {}
    to_translate = 'dentifrici' #the original word
    for country in countries:
        translation = (GoogleTranslator(source='auto', target=country["abbreviation"]).translate(to_translate))
        translation = translation.replace(" ", "-")
        translated[country["url"]] = translation
    return translated



def main(retailer: str) -> pd.DataFrame:
    AbstractScraper.setup_logger()
    AbstractScraper.log_info("Reading the file with countries")

    #INFO.JSON contains all the countries of notino, use small.json to scrap only the countries you want
    ## pages not found are pages for which the machine translation may not be correct. They are often plural or singular names.
    # What I would do is that when a page is not found, you search with the translation made in the search and click on the first link.
    # This is not implemented at the moment because I did not know how far I had to go.

    #in any case, the log file also saves the words that do not give results and for which language

    #Improvement/increase of data search I suggest is to click on each element and go for information such as recommendations 
    #(although it is possible to calculate them from the width, I have noticed), but also other information more in depth.


    #with open('info.json', 'r') as f:
    #    countries = json.load(f)

    with open('small.json', 'r') as f:
        countries = json.load(f)

    AbstractScraper.log_info("Finished to load")
    names = all_countries(countries)
    AbstractScraper.log_info(names)

    for name, transl in names.items():
        
        scraper = NotinoScraper(retailer=retailer, country=name)
        try:
            AbstractScraper.log_info(f"Scraping started for country: {name}")
            products_df = scraper.scrape_with_selenium(transl)
            AbstractScraper.log_info(f"Scraping completed for country: {name}")
        except Exception as e:
            AbstractScraper.log_error(f"Error while scraping for country {name}: {str(e)}")
            continue
    return products_df



if __name__ == "__main__":
    df_raw = main(retailer="notino")
    try:
        df_raw.to_csv("notino_raw.csv", index=False)
        AbstractScraper.log_info("Saved on CSV")
    except Exception as e:
        AbstractScraper.log_error(f"An error occurred while saving to CSV: {str(e)}")