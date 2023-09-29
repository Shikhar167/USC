

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
        team1 = embed_soup.find(class_='ds-inline-flex ds-items-center ds-bg-ui-fill-alternate ds-text-typo ds-h-6 ds-px-2 ds-rounded-full ds-font-medium ds-cursor-pointer ds-whitespace-nowrap').span.text[:-7]    
        team2 = embed_soup.find(class_='ds-inline-flex ds-items-center ds-bg-ui-fill ds-text-typo-primary ds-border ds-border-ui-stroke-primary ds-h-6 ds-px-2 ds-rounded-full ds-font-medium ds-cursor-pointer ds-whitespace-nowrap').span.text[:-7]  
        if(team1=='Mat'):
            continue
        else:
                
            team1_bowling = embed_soup.find(class_='ds-text-title-xs ds-font-bold ds-text-typo').span.text
            team2_bwoling =  embed_soup.find(class_='ds-text-title-xs ds-font-bold ds-text-typo').span.text
            scorecardnumber = "T20 #" + str(i)
            i+=1
            
            
            team1bowling = embed_soup.find_all('tbody')[1].find_all('tr')
            team2bowling = embed_soup.find_all('tbody')[3].find_all('tr')
            
            first_innings_row =[row for row in team1bowling if len(row.find_all('td'))==11]
            second_innings_row =[row for row in team2bowling if len(row.find_all('td'))==11]
 


            


            json_list=[]
            
            for bowlingcards1 in first_innings_row:
                cols1 = bowlingcards1.find_all('td')
                bowler1 = cols1[0].get_text().replace('†','').replace('(c)','').strip()
                overs1 = cols1[1].get_text().strip()
                maidens1 = cols1[2].get_text().strip()
                runs1 = cols1[3].get_text().strip()
                wickets1 = cols1[4].get_text().strip()
                econ1 = cols1[5].get_text().strip()
                zeros1 = cols1[6].get_text().strip()
                fours1 = cols1[7].get_text().strip()
                sixes1 = cols1[8].get_text().strip()
                wides1 = cols1[9].get_text().strip()
                noballs1 = cols1[10].get_text().strip()

                json_member1={}
                json_member1['matchid'] = scorecardnumber
                json_member1['match'] = team2.strip() + " vs " + team1.strip()
                json_member1['bowlingTeam'] = team1.strip()
                json_member1['bowlerName'] = bowler1
                json_member1['overs'] = overs1
                json_member1['maidens'] = maidens1
                json_member1['runs'] = runs1
                json_member1['wickets'] = wickets1
                json_member1['economy'] = econ1
                json_member1['dotBalls'] = zeros1
                json_member1['fours'] = fours1
                json_member1['sixes'] = sixes1
                json_member1['wides'] = wides1
                json_member1['noBalls'] = noballs1

        
                json_list.append(json_member1)
                

             
            for bowlingcards2 in second_innings_row:
                cols2 = bowlingcards2.find_all('td')
                bowler2 = cols2[0].get_text().replace('†','').replace('(c)','').strip()
                overs2 = cols2[1].get_text().strip()
                maidens2 = cols2[2].get_text().strip()
                runs2 = cols2[3].get_text().strip()
                wickets2 = cols2[4].get_text().strip()
                econ2 = cols2[5].get_text().strip()
                zeros2 = cols2[6].get_text().strip()
                fours2 = cols2[7].get_text().strip()
                sixes2 = cols2[8].get_text().strip()
                wides2 = cols2[9].get_text().strip()
                noballs2 = cols2[10].get_text().strip()

              
               
                json_member2={}
                json_member2['matchid'] = scorecardnumber
                json_member2['match'] = team2.strip() + " vs " + team1.strip()
                json_member2['bowlingTeam'] = team2.strip()
                json_member2['bowlerName'] = bowler2
                json_member2['overs'] = overs2
                json_member2['maidens'] = maidens2
                json_member2['runs'] = runs2
                json_member2['wickets'] = wickets2
                json_member2['economy'] = econ2
                json_member2['dotBalls'] = zeros2
                json_member2['fours'] = fours2
                json_member2['sixes'] = sixes2
                json_member2['wides'] = wides2
                json_member2['noBalls'] = noballs2

        
                json_list.append(json_member2)
                

            bowlingsummary={}
            bowlingsummary['bowlingSummary'] = json_list
            big_list.append(bowlingsummary)
  
            
            finaljson = json.dumps(big_list, indent = 4)
            
            with open("bowling.json", "w") as outfile:
                outfile.write(finaljson)
            

                    
            
                    
                  
    
    
    

    

  
        
      

except Exception as e:
    print(e)

