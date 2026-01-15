# scrapes rotowire website for NBA games, lineups, and active players for given day
import requests
from bs4 import BeautifulSoup

url = "https://www.rotowire.com/basketball/nba-lineups.php"
page = requests.get(url)
# print(page.text) # testing if page is being accessed correctly
soup = BeautifulSoup(page.content, "html.parser")

games_blocks = soup.select("div.lineups")
games = []

def get_data(games_blocks):
    for block in games_blocks:
        classes = block.get("class", [])

        # filter out unwanted classes, looking for lineup is-nba class
        if "lineup is-nba" not in classes:
            continue
        if "lineup is-nba is-tools is-picks" in classes:
            continue
        if "lineup-gdc" in classes:
            continue
        if "lineup is-ad hide-until-lg" in classes:
            continue
        if "lineup is-nba is-tools" in classes:
            continue
        
        box = block.select_one("lineup__box")
        if not box:
            continue
        

