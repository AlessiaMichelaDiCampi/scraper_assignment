import logging
import requests
from datetime import datetime

from abc import ABC


class AbstractScraper(ABC):
    
    def __init__(self, retailer, country):
        self.retailer = retailer
        self.country = country
        self.logger = logging.getLogger(__name__) 

    # implement methods for sending GET and POST requests
    # these methods should be able to handle sending requests to the url with headers, cookies, params & json (POST requests only)
     #Alessia: I dont use it
    def get(url, headers=None):
        session = requests.Session()
        if headers:
            session.headers.update(headers)
        response = session.get(url)
        return response
    
      #Alessia: I dont use it
    def send_post_request(self, url, headers=None, cookies=None, json=None):
        try:
            response = requests.post(url, headers=headers, cookies=cookies, json=json)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response
        except requests.RequestException as e:
            self.logger.error(f"POST request to {url} failed: {e}")
            return None
        
    #Creation of the log file
    def setup_logger():
        logging.basicConfig(
            filename='scraping.log',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    def log_info(message):
        logging.info(message)

    def log_error(message):
        logging.error(message)

    # feel free to add any other methods you think you might need or could be useful