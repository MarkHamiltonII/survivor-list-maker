import requests
from bs4 import BeautifulSoup
import json

# NOTE: THIS NEEDS TO BE DONE BEFORE THE SEASON TO PROPERLY SCRAPE ONCE THE TABLE POPULATES, IT WON'T WORK

base_url = "https://survivor.fandom.com"
url = "https://survivor.fandom.com/wiki/Survivor_45"

response = requests.get(url)
html_raw = response.text
soup = BeautifulSoup(html_raw, 'html.parser')

rows = soup.find_all('tr')
smalls = soup.find_all('small')
titles = soup.find_all("title")

castaways = []
index = 1

def getTribeFromColor(color):
    if color == '#4caae6':
        return 'Belo'
    if color == '#ff4148':
        return 'Reba'
    if color == '#fcdd31':
        return 'Lulu'

for row in rows:
    if len(castaways) == 18:
        break
    castaway = {}
    tds = row.find_all('td')
    if tds:
        for td in tds:
            links = td.find_all('a')
            if links:
                for link in links:
                    if '44' in link.get('title'):
                        break
                    if td.get('align'):
                        info = td.find('small').text.split(", ")
                        castaway['name'] = link.get('title')
                        castaway['age'] = info[0]
                        castaway['currentResidence'] = info[1] + info[2][0:2]
                        castaway['occupation'] = info[2][2:]
                        castaway['pageURL'] = f'{base_url}{link.get("href")}'
                    else:
                        castaway['tribeColor'] = td.get('style')[11:18]
                        castaway['tribe'] = getTribeFromColor(castaway['tribeColor'])
                        img = link.find('img')
                        if img.get('data-src'):
                            castaway['iconURL'] = img.get('data-src')
                        else:
                            castaway['iconURL'] = img.get('src')
    if castaway:
        castaway['id'] = index
        index += 1
        castaways.append(castaway)

with open("season_45_castaways.json", 'w') as outfile:
    json.dump(castaways, outfile, indent=4)