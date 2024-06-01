# Scraping practical task

## General Info

Scrape data from Notino website about toothpastes and transform them.

 - use Python
 - it is recommended to use file structure in this repository, but it is not mandatory. Up to your creativity.
 - you can use any libraries you want. Output should be csv file.
 - *clone this repository and after you are done with the task send link to your github or solution over to petr@forloop.ai and dominik@forloop.ai*

## File structure

 `abstract/abstract_scraper.py` - Base class for scrapers.
  - implement logger, sending get and post requests
  - you can implement any other additional methods and features you consider useful

 `notino/scraper.py` - Scraper for Notino - raw data.
  - Choose any language mutation of Notino and scrape toothpastes
  - https://www.notino.cz/zubni-pasty/ // https://www.notino.co.uk/toothpaste/ // https://www.notino.de/zahnpasten/ ... Notino is present in 28 countries
  - get info about products | mandatory: product name, brand, price, url, image 
  - any additional info is welcomed
  - save result to csv file `notino_raw.csv`

`notino/transformation.py` - Transformation of raw data to final format
  - add country (str), currency (str) and scraped_at (datetime) columns
  - add discount amount column (difference between price and price before sale or promocode) 
  - save result to csv file `notino_transformed.csv`



