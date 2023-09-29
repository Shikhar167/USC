

from bs4 import BeautifulSoup
import requests
import json


    
try:
    source = requests.get('https://www.espncricinfo.com/records/tournament/team-match-results/indian-premier-league-2023-15129')
    source.raise_for_status()
# always good practice when website is not reachable or invalid url to use raise for status method
    soup = BeautifulSoup(source.text,'html.parser')
#    print(soup)
    matchresults = soup.find('tbody').find_all('tr')
# need to add underscore after class because it is a keyword in python. Otherwise we dont need to add the underscore
    i=1
   
    json_list=[]
    
    

    for matches in matchresults:
        if((matches.find_all('td', class_="ds-min-w-max ds-text-right")[1].text)=='no result'):
            continue
        else:
            matchSummary=[]
            team1 = matches.find('td', class_="ds-min-w-max").span.a.span.text
            team2 = matches.find('td', class_="ds-min-w-max ds-text-right").span.a.span.text
            winner = matches.find_all('td', class_="ds-min-w-max ds-text-right")[1].text
            margin = matches.find_all('td', class_="ds-min-w-max ds-text-right")[2].text
            ground = matches.find_all('td', class_="ds-min-w-max ds-text-right")[3].span.a.span.text
            date = matches.find('td', class_="ds-min-w-max ds-text-right ds-whitespace-nowrap").span.text
            scorecard = "T20 #" + str(i)
            i=i+1
            json_member={}
            json_member['Team1'] = team1
            json_member['Team2'] = team2
            json_member['Winner'] = winner
            json_member['Margin'] = margin
            json_member['Ground'] = ground
            json_member['Date'] = date
            json_member['Scorecard'] = scorecard
            json_list.append(json_member)
    
    json_dictfinal  = {'matchSummary' : json_list}
    final_list = []
    final_list.append(json_dictfinal)
    
    finaljson = json.dumps(final_list, indent = 4)
    
    with open("matches.json", "w") as outfile:
        outfile.write(finaljson)
    

  
        
      

except Exception as e:
    print(e)

