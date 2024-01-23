import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = 'https://fbref.com'
COMP_URL = '/en/comps/9/Premier-League-Stats'
DATA_DELAY = 1  # Adjust this as needed

def get_team_data(team_url, year):
    data = requests.get(team_url)
    soup = BeautifulSoup(data.text, 'html.parser')

    matches = pd.read_html(data.text, match='Scores & Fixtures')[0]
    links = [l.get('href') for l in soup.find_all('a')]
    links = [l for l in links if l and 'all_comps/shooting/' in l]
    data = requests.get(f'{BASE_URL}{links[0]}')
    shooting = pd.read_html(data.text, match='Shooting')[0]
    shooting.columns = shooting.columns.droplevel()

    try:
        team_data = matches.merge(shooting[['Date', 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']], on='Date')
    except ValueError:
        return None
    
    team_name = team_url.split('/')[-1].replace('-Stats','').replace('-','')
    team_data = team_data[team_data['Comp'] == 'Premier League']
    team_data['Season'] = year
    team_data['Team'] = team_name

    return team_data

def main():

    years = list(range(2024,2023, -1))
    all_matches=[]

    standings_url= BASE_URL + COMP_URL

    for year in years:
        try:
            data = requests.get(standings_url)
            data.raise_for_status() # Raise an exception for HTTP errors

            soup = BeautifulSoup(data.text, 'html.parser')

            standings_table = soup.select('table.stats_table')[0]

            links = [l.get('href') for l in standings_table.find_all('a')]
            links = [l for l in links if '/squads/' in l]
            team_urls = [f'https://fbref.com{l}' for l in links]
    
            previous_season = soup.select('a.prev')[0].get('href')
            standings_url = f'https://fbref.com{previous_season}'

            for team_url in team_urls:
                team_data = get_team_data(team_url, year)
                if team_data:
                    all_matches.append(team_data)


                time.sleep(DATA_DELAY)

        except requests.exceptions.RequestException as e:
            print(f'An error occurred: {e}')
            continue
        
    match_df = pd.concat(all_matches)

    match_df.to_csv('matches.csv')

if __name__ == '__main__':
    main()