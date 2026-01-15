# scrapes rotowire website for NBA games, lineups, and active players for given day
import requests
from bs4 import BeautifulSoup

url = "https://www.rotowire.com/basketball/nba-lineups.php"
page = requests.get(url)
# print(page.text) # testing if page is being accessed correctly
soup = BeautifulSoup(page.content, "html.parser")

games_blocks = soup.select("div.lineups > div.lineup")
games = []

def get_data(games_blocks):
    for block in games_blocks:
        classes = block.get("class", [])
        # filter out unwanted classes, looking for lineup is-nba class
        if "is-nba" not in classes:
            continue
        if "is-tools" in classes or "is-picks" in classes:
            continue
        if "lineup-gdc" in classes:
            continue
        if "is-ad" in classes or "hide-until-lg" in classes:
            continue
        
        box = block.select_one("div.lineup__box")
        if not box:
            continue

        # extract team names 
        top_block = box.select_one("div.lineup__top")
        teams = top_block.select_one("div.lineup__teams")
        team_names = []

        visitor_logo = teams.select_one(".lineup__team.is-visit .lineup__abbr")
        home_logo = teams.select_one(".lineup__team.is-home .lineup__abbr")
        away_abbr = visitor_logo.get_text(strip=True)
        team_names.append(away_abbr)
        home_abbr = home_logo.get_text(strip=True)
        team_names.append(home_abbr)
        
        # extract players + status tags
        main_block = box.select_one("div.lineup__main")


get_data(games_blocks)

