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

    list_urls=[]
    i=1
    big_list=[]


    for matches in matchresults:
        link = matches.find_all('td', class_="ds-min-w-max ds-text-right")[4].a.get("href")
        url = 'https://www.espncricinfo.com' + str(link)
        embed_source = requests.get(url)
        embed_source.raise_for_status()
        embed_soup = BeautifulSoup(embed_source.text,'html.parser')
        team1 = embed_soup.find(class_='ds-inline-flex ds-items-center ds-bg-ui-fill ds-text-typo-primary ds-border ds-border-ui-stroke-primary ds-h-6 ds-px-2 ds-rounded-full ds-font-medium ds-cursor-pointer ds-whitespace-nowrap').span.text[:-7]  
        team2 = embed_soup.find(class_='ds-inline-flex ds-items-center ds-bg-ui-fill-alternate ds-text-typo ds-h-6 ds-px-2 ds-rounded-full ds-font-medium ds-cursor-pointer ds-whitespace-nowrap').span.text[:-7]
        if(team2=='Mat'):
            continue
        else:
                
            team1_innings = embed_soup.find(class_='ds-text-title-xs ds-font-bold ds-text-typo').span.text
            team2_innings = embed_soup.find(class_='ds-text-title-xs ds-font-bold ds-text-typo').span.text
            scorecardnumber = "T20 #" + str(i)
            i+=1
            
            
            team1battingscorecard = embed_soup.find_all('tbody')[0].find_all('tr')
            team2battingscorecard = embed_soup.find_all('tbody')[2].find_all('tr')
            first_innings_row =[row for row in team1battingscorecard if len(row.find_all('td'))==8]
            second_innings_row =[row for row in team2battingscorecard if len(row.find_all('td'))==8]
            
            battingpos1=1
            battingpos2=1
            
            json_list=[]
            
            for battingcards1 in first_innings_row:
                cols1 = battingcards1.find_all('td')
                batsman1 = cols1[0].get_text().replace('†','').replace('(c)','').strip()
                dismissal1 = cols1[1].get_text().strip().replace('†','')
                runs1 = cols1[2].get_text().strip()
                balls1 = cols1[3].get_text().strip()
                fours1 = cols1[5].get_text().strip()
                sixes1 = cols1[6].get_text().strip()
                strikerate1 = cols1[7].get_text().strip()
                battingpos1+=1
                json_member1={}
                json_member1['matchid'] = scorecardnumber
                json_member1['match'] = team1.strip() + " vs " + team2.strip()
                json_member1['teamInnings'] = team1.strip()
                json_member1['battingPos'] = battingpos1
                json_member1['batsmanName'] = batsman1
                json_member1['dismissal'] = dismissal1
                json_member1['runs'] = runs1
                json_member1['balls'] = balls1
                json_member1['fours'] = fours1
                json_member1['sixes'] = sixes1
                json_member1['strikrate'] = strikerate1
        
                json_list.append(json_member1)
                

 
            for battingcards2 in second_innings_row:
                cols2 = battingcards2.find_all('td')
                batsman2 = cols2[0].get_text().replace('†','').replace('(c)','').strip()
                dismissal2 = cols2[1].get_text().strip().replace('†','')
                runs2 = cols2[2].get_text().strip()
                balls2 = cols2[3].get_text().strip()
                fours2 = cols2[5].get_text().strip()
                sixes2 = cols2[6].get_text().strip()
                strikerate2 = cols2[7].get_text().strip()
                battingpos2+=1
                
            
                json_member2={}

                json_member2['matchid'] = scorecardnumber
                json_member2['match'] = team1.strip() + " vs " + team2.strip()
                json_member2['teamInnings'] = team2.strip()
                json_member2['battingPos'] = battingpos2
                json_member2['batsmanName'] = batsman2
                json_member2['dismissal'] = dismissal2
                json_member2['runs'] = runs2
                json_member2['balls'] = balls2
                json_member2['fours'] = fours2
                json_member2['sixes'] = sixes2
                json_member2['strikerate'] = strikerate2
        
                json_list.append(json_member2)
                
            battingsummary={}
            battingsummary['battingSummary'] = json_list
            big_list.append(battingsummary)
  
            
            finaljson = json.dumps(big_list, indent = 4)
            
            with open("batting.json", "w") as outfile:
                outfile.write(finaljson)
            

                    
            
                    
                  
    
    
    

    

  
        
      

except Exception as e:
    print(e)

