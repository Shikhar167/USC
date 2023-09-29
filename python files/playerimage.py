import requests
from bs4 import BeautifulSoup
import json
url='https://www.espncricinfo.com'
try:
  source=requests.get('https://www.espncricinfo.com/records/tournament/team-match-results/indian-premier-league-2023-15129')
  source.raise_for_status()
  soup=BeautifulSoup(source.text,'html.parser')
  records=soup.find('tbody').find_all('tr') 
  links=[]
  for record in records:
      tds=record.find_all('td')
      if(tds[2].text =='no result'):
          pass
      else:
          links.append(url+tds[6].a['href'])
 
 
  res=[]
  summary=[]
  playerlinks={}
  
  for link in links:
      sub_source=requests.get(link)
      sub_source.raise_for_status()
      sub_soup=BeautifulSoup(sub_source.text,'html.parser')
      divs=sub_soup.find('div',class_="ds-relative ds-w-full ds-scrollbar-hide ds-py-2").div.find_all('div')
      team1=divs[0].span.span.span.text.split('Innings')[0].strip()
      team2=divs[1].span.span.span.text.split('Innings')[0].strip()
      #print(link)
     
     
    
      
     
      #BATTING
     
      inn_tables=sub_soup.find_all('table',class_='ci-scorecard-table')
    
      #team1
      rows=inn_tables[0].find('tbody').find_all('tr')
      first_innings_rows=[row for row in rows if len(row.find_all('td'))==8]
     
      for i,frow in enumerate(first_innings_rows):
          tds=frow.find_all('td')
          batsmanName= tds[0].get_text().strip()
          playerlinks[tds[0].a['href']]=[team1,batsmanName]
          
     
      
         
      #team2
      rows2=inn_tables[1].find('tbody').find_all('tr')
      sec_innings_rows=[row2 for row2 in rows2 if len(row2.find_all('td'))==8]
      
      for i,srow in enumerate(sec_innings_rows):
          tds=srow.find_all('td')
          batsmanName= tds[0].get_text().strip()
          playerlinks[tds[0].a['href']]=[team2, batsmanName]
            
      
        

      


       #BOWLING team2
      inn_tables_bowl=sub_soup.find_all('table',class_='ds-w-full ds-table ds-table-md ds-table-auto')
      rows=inn_tables_bowl[0].find('tbody').find_all('tr')
      first_innings_rows=[row for row in rows if len(row.find_all('td'))==11]
      
      for i,frow in enumerate(first_innings_rows):
          tds=frow.find_all('td')
          bowlerName=tds[0].get_text().strip()
          playerlinks[tds[0].a['href']]=[team2,bowlerName]
         
         
      
  
        
        
 
       #team1
      rows2=inn_tables_bowl[1].find('tbody').find_all('tr')
      sec_innings_rows=[row2 for row2 in rows2 if len(row2.find_all('td'))==11]
      
      for i,srow in enumerate(sec_innings_rows):
          tds=srow.find_all('td')
          bowlerName=tds[0].get_text().strip()
          playerlinks[tds[0].a['href']]=[team1,bowlerName]
         
      
          
  #print(playerlinks)
  
  for key_link in playerlinks:
      web_link=url+key_link
      player_source=requests.get(web_link)
      player_source.raise_for_status()
      player_soup=BeautifulSoup(player_source.text,'html.parser')
      divs=player_soup.find('div',class_='ds-grid').find_all('div')
      
      image=player_soup.find(itemprop="image")
      image_link=image['content']
     
      div_desc=player_soup.find('div',class_="ci-player-bio-content")       
      desc=""
       #print(len(divs))
      if(div_desc):
          desc=div_desc.p.text
      battingStyle=''
      bowlingStyle=''
      playingRole=''
   
      for div in divs:
          if(div.find('p',text='Batting Style')):
              battingStyle=div.span.text
          elif(div.find('p',text='Bowling Style')):
              bowlingStyle=div.span.text
          elif(div.find('p',text='Playing Role')):
              playingRole=div.span.text
        
        
  
  
    
    
      res.append( {
            "name": playerlinks[key_link][1],
            "team": playerlinks[key_link][0],
            "battingStyle": battingStyle,
            "bowlingStyle": bowlingStyle,
            "playingRole":  playingRole,
            "description": desc,
            "image":image_link
                 
            })
      print(res)
      
      
        
        
          
     
     
      
     
   
     
     
  with open("players_withimages.json", "w") as writeJSON:
      json.dump(res, writeJSON, ensure_ascii=False)
              
      
          
     
  
except Exception as e:
  print(e)
