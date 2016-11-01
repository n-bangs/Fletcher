import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.ratebeer.com/Ratings/MostActiveBrewers.asp'

resp = requests.get(url)

soup = BeautifulSoup(resp.text,'lxml')

table = soup.find('table', {'class': 'maintable'})
hrefs = []

for tr in table.findAll('tr')[1:]:
    hrefs.append(tr.findAll('td')[1].find('a')['href'])

f  = open('brewery_hrefs.json', 'w')
j = json.dumps(hrefs)
f.write(j)
f.close()
