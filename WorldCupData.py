from bs4 import BeautifulSoup
import requests
import csv

# Retrive data source/website
url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


# Locate the title of the data set
year = soup.find('h1', id='firstHeading').get_text()

# Establish team dictionaries

uniqueTeams = []
chartTitles= ["Home Team", "Score", "Away Team"]
column = 1

# Print title and headers of chart
print(year)
print(f"{'':-<50}")
print(f"{chartTitles[0]: <20}{chartTitles[1]: <15}{chartTitles[2]}")
print(f"{'':-<50}")

# Identify the common html elemnt that all games are within on the webpage
games = soup.find_all('div', class_='footballbox')

# Loop through all 'footballboxes' to select team names, score, and date of match
for game in games:
    teamA = game.find('th', class_='fhome').get_text().strip()
    if teamA not in uniqueTeams:
        uniqueTeams.append(teamA)

    teamB = game.find('th', class_='faway').get_text().strip()

    score = game.find('th', class_='fscore').get_text()

    goalsA = score.split('–')[0]

    goalsB = score.split('–')[1]

    date = game.find(("div", "fdate")).get_text()

    print(f"{teamA: <20}{score: <15}{teamB}")

    # Import data into a csv file
    with open('WorldCupData.csv', mode='a', newline='', encoding='utf-8') as outputFile:
        worldCupCSV = csv.writer(outputFile, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)

        if column == 1:
            worldCupCSV.writerow(['year', 'teamA', 'teamB', 'goalsA', 
                'goalsB', 'date'])
            column += 1

        worldCupCSV.writerow([year, teamA, teamB, goalsA, 
                goalsB, date])