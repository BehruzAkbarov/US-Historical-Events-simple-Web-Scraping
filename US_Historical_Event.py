# BIGGEST EVENTS IN USA HISTORY


#####################
# Import Libraries  #
#####################
from bs4 import BeautifulSoup as soup
import requests
import re
import pandas as pd


###################
#   WEB SCRAPING  #
###################


##Request the web content and save it as a BeautifulSoup object
URL = ['https://www.historycentral.com/Today/Index.html', 'https://www.historycentral.com/Today/21st.html']
html_pages = []
for link in URL:
    r = requests.get(link)
    html_pages.append(soup(r.content))


##Use BeautifulSoup method to extract the year and events
biggest_events = []
for page in html_pages:
    table = page.find('table')
    biggest_events += [row.find('a').string for row in table.find_all('tr') if row.find('td') and row.find('a').string]


#########################
#  REGULAR EXPRESSIONS  #
#########################


## Turn dash(-) into " " and split the year and event
events = [re.sub('-'," ",event) for event in biggest_events]
events = [event.split(' ', 1) for event in events]
events


# PANDAS
## Make a data frame with year and events as columns
df = pd.DataFrame(events, columns=['Year', 'Event'])


##Locate row 15 and fixed the year and event. Event = 'Assassination Attempt on Reagan' and Year = "1981"
df.loc[15].Year = '1981'
df.loc[15].Event = 'Assassination Attempt on Reagan'


#Used Replace method to turn '983' to '1983'
df= df.replace('983', '1983')


#Strip the event column
df['Event'] = df.Event.str.strip()


#Group all the events in same year
df = df.groupby('Year')['Event'].apply(' / '.join).reset_index()


#Save as SCV
df.to_csv('biggest-events-US.csv', index=False)


#Read SCV
df = pd.read_csv('biggest-events-US.csv')
print(df)
