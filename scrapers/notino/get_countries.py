from bs4 import BeautifulSoup
import requests
import json

#Once this file has been run, it fills the info.json file with the information of all notino dealers. It will then be useful for scraping the toothpastes (but also others) for each one.

url = 'https://www.notino.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

info_list = []

flags_div = soup.find_all('div', class_='flags')

for div in flags_div:
    flag_links = div.find_all('a')
    for link in flag_links:
        url = link.get('href')
        hreflang = link.get('hreflang')
        flag_name = link.find('span', class_='flag__name').text
        info_list.append({"url": url, "abbreviation": hreflang})

with open('info.json', 'w') as f:
    json.dump(info_list, f, indent=4)
