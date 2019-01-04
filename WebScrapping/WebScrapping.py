import pandas as pd
import requests
from bs4 import BeautifulSoup
import html5lib
import lxml

from urllib.request import urlopen as uReq

def WebScrappingBasics():
    page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
    soup = BeautifulSoup(page.content,'html.parser')
    print(soup)
    print("End---------------------------------------------")
    #print(soup.find_all('p',class_='outer-text'))
    #print(soup.find_all(id="first"))
    print(soup.select("div p"))

#getting the data from a class
def WebScrapping():
    page = requests.get("https://forecast.weather.gov/MapClick.php?lat=44.565&lon=-123.2635#.XAWX23VKi0s")
    soup = BeautifulSoup(page.content,'html.parser')
    seven_day_id = soup.find(id="seven-day-forecast")
    forecast_items = seven_day_id.find_all(class_="tombstone-container")
    tonight = forecast_items[0]
    print(tonight.prettify())
    period = tonight.find(class_="period-name").get_text() #get_text() extracts the
    short_desc = tonight.find(class_="short-desc").get_text()
    temp = tonight.find(class_="temp").get_text()
    img = tonight.find("img")
    desc = img['title']

    print(period)
    print(short_desc)
    print(temp)
    print(desc)


#getting the data from multiple classes and putting in a DataFrame
def WeatherExample():
    page = requests.get("https://forecast.weather.gov/MapClick.php?lat=44.565&lon=-123.2635#.XAWX23VKi0s")
    soup = BeautifulSoup(page.content,'html.parser')
    seven_day_id = soup.find(id="seven-day-forecast")

    period_tags = seven_day_id.select(".tombstone-container .period-name") #select all the items with the class period-name inside an item with the class tombstone-container
    periods = []
    for pt in period_tags:
        periods.append(pt.get_text())

    #another short way of adding items in a list
    short_desc = [sd.get_text() for sd in seven_day_id.select(".tombstone-container .short-desc")]
    temperature = [tmp.get_text() for tmp in seven_day_id.select(".tombstone-container .temp")]
    desc_img_title = [desc['title'] for desc in seven_day_id.select(".tombstone-container img ")] #select all items with img tag inside the class tombstone-container (and extract the title attribute from each tag)


    #combining into pandas Dataframe
    weather = pd.DataFrame({
        "period": periods,
        "short-desc": short_desc,
        "temperature": temperature,
        "description": desc_img_title
    })
    print(weather)

def displayCriminalRecords():
    # url = 'https://www.fbi.gov/wanted/fugitives'
    # Client = uReq(url)
    page = requests.get("https://www.fbi.gov/wanted/fugitives")
    soup = BeautifulSoup(page.content, "lxml")
    id = soup.find(id="visual-wrapper")
    query_results =  id.find_all(class_="portal-type-person castle-grid-block-item")
    allNames = id.find_all('p', class_="name")
    #print(len(allNames))

    criminal_PageAddr = []
    for i in range(0,len(allNames)):
        for criminalInfo in allNames[i].find_all('a', href=True):
            x = criminalInfo['href']
        criminal_PageAddr.append(x)
    #print(criminal_PageAddr[39])

    allCrimPages = [requests.get(addR) for addR in criminal_PageAddr]

    # soup = BeautifulSoup(allCrimPages[0].content,'html.parser')
    MetaTable = []
    for crimPage in range(len(allCrimPages)):
        MetaTable.append(ExtractCrimData(crimPage,allCrimPages))

    uploadToPanda(MetaTable)


def ExtractCrimData(crimPage,allCrimPages):
    souped_crimPage = BeautifulSoup(allCrimPages[crimPage].content,'html.parser')
    dataTable = []
    name = souped_crimPage.find('h1', class_="documentFirstHeading").get_text()
    summary = souped_crimPage.find('p', class_="summary").get_text()
    #aliasX = souped_crimPage.find('div', class_="wanted-person-aliases")
    aliases = [x.get_text() for x in souped_crimPage.select(".wanted-person-aliases p")]

    dataTable.append(['name',name])
    dataTable.append(['summary',summary])
    dataTable.append(['aliases',aliases])

    #table extract
    crimTable = souped_crimPage.find('table', class_="table table-striped wanted-person-description")
    crimTable_body = crimTable.find('tbody')

    rows = crimTable_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.get_text() for ele in cols]
        dataTable.append([ele for ele in cols if ele])

    return dataTable


def uploadToPanda(MetaTable):
    # for Criminal in MetaTable:
    #     MegaTable = pd.DataFrame({
    #         "name", MetaTable[Criminal][0][0],
    #         "summary", MetaTable[Criminal][1][0],
    #         "alias", MetaTable[Criminal][2][0],
    #         "dob", MetaTable[Criminal][3][0]
    #     })
    for i in range(len(MetaTable)):
        #print(MetaTable[i])
        for j in range(len(MetaTable[i])):
            print(MetaTable[i][j])
        print("----------------------------------")