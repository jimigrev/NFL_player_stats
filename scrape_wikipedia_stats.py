# scrape_wikipedia_stats.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_nfl_stats(wikipedia_url: str, player_name: str):
    # Fetch and parse the page
    response = requests.get(wikipedia_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create output folder
    os.makedirs("data", exist_ok=True)

    # Find all tables under "NFL career statistics" section
    career_header = soup.find('span', string='NFL career statistics')
    if not career_header:
        print("Couldn't find NFL career statistics section.")
        return

    stats_section = career_header.find_parent('h2').find_next_siblings()
    tables = []
    for tag in stats_section:
        if tag.name == 'h2':
            break  # End of section
        if tag.name == 'table' and 'wikitable' in tag.get('class', []):
            tables.append(tag)

    if not tables:
        print("No stats tables found.")
        return

    # Assume first is regular season, second is postseason
    table_labels = ['regular_season', 'postseason']
    for i, table in enumerate(tables[:2]):
        df = pd.read_html(str(table))[0]
        filename = f"data/{player_name.lower().replace(' ', '_')}_{table_labels[i]}.tsv"
        df.to_csv(filename, sep='\t', index=False)
        print(f"Saved: {filename}")

if __name__ == "__main__":
    # Example: Josh Allen
    url = "https://en.wikipedia.org/wiki/Josh_Allen_(quarterback)"
    player = "Josh Allen"
    scrape_nfl_stats(url, player)
