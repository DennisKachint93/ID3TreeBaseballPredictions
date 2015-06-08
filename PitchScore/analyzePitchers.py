__author__ = 'dgotbaum'
from PitcherYear import PitcherYear
from Year import Year
from id3 import *

birthYears = {}
headers = {}
years = {}

def populateYears():
    pitchingFile = open('Pitching.csv', 'r')
    ageFile = open('Master.csv', 'r')

    #This gets the birth years for all playerIDS
    for line in ageFile:
        line = line.split(',')
        id = line[0]
        birthYear = line[1]
        if len(birthYear) > 1:
            birthYears[id] = birthYear

    #this creates a PitcherYear for each row in Pitching.csv and adds it to the appropriate Year in the years list
    for line in pitchingFile:
        line = line.split(",")
        if line[0] == "playerID":
            for i in range(len(line)):
                headers[line[i]] = i
        else:
            playerID = line[headers["playerID"]]
            IP = int(line[headers["IPouts"]])/3
            if IP >=162 and playerID in birthYears:
                yearID = int(line[headers["yearID"]])
                age = yearID - int(birthYears[playerID])
                BB = int(line[headers["BB"]])
                SO = int(line[headers["SO"]])
                H = int(line[headers["H"]])
                ERA = float(line[headers["ERA"]])
                player = PitcherYear(playerID,SO,BB,ERA,IP,H,yearID,age)
                if yearID not in years:
                    year = Year(yearID)
                    year.enterPitcher(player)
                    years[yearID] = year
                else:
                    years[yearID].enterPitcher(player)
def main():
    populateYears()
    data = []
    test = [1,1,1]
    category_names = [
            ["age", "young", "low-prime", "high-prime", "old"],
            ["ERA", "elite", "good", "poor", "horrible"],
            ["WHIP", "elite", "good", "poor", "horrible"],
            ["SOW", "elite", "good", "poor", "horrible"],
        ]

    for year in years:
        print(year)
        for player in years[year].pitchers:
            print("    ", player)
            data.append(player.list_categories())

    print(data)
    pitcher_tree = buildTreeFromData(data, category_names)
    print(classifyDat(test, category_names, pitcher_tree))
       # for item in data:
         #   if item[2] == 4:
          #      print(item)

main()