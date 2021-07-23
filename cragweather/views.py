from django.shortcuts import render
from django.http import HttpResponse
import logging, coloredlogs, requests, re, geonamescache
import time, schedule
from bs4 import BeautifulSoup
from .models import weatherModel, locationModel, cragModel

DATA_FOR_SCRAPING_URL='https://www.mountainproject.com/'

coloredlogs.install()

# Create your views here.

#admin views

#guest user views

#View to weather object to database

#Build an object and add it to the database
def addToDatabase():
  wmod = weatherModel(month=1, day=15, year=2021, current_temp=45, daily_high_temp=999, daily_low_temp=10, precip_ammount=0)
  wmod.save()

def buildListOfStatesAndCountries():
    countryAndStateList = []
    INCONSISTENTLABELSCHEMES = ['International', "Antarctica", "Australia", "Africa", "Europe", "North America", "Asia",
                                "South America", "Oceania", "* In Progress"]

    gc = geonamescache.GeonamesCache()
    states = gc.get_us_states_by_names().keys()
    countries = gc.get_countries_by_names().keys()

    for state in states:
        countryAndStateList.append(str(state))

    for country in countries:
        countryAndStateList.append(str(country))

    return countryAndStateList + INCONSISTENTLABELSCHEMES


def getLocationInformation(webLink):
    response = requests.get(webLink)
    soup = BeautifulSoup(response.text, 'html.parser')
    locations = set(soup.findAll('a', {'style': "max-width:70%;", "class": "text-truncate float-xs-left"}))
    locationList = buildListOfStatesAndCountries()

    for place in locations:
        if place.text in locationList:
            key = locationList.index(place.text)
            #print(count, place.text, place.get('href'))
            buildLocationInDatabase(place.text, place.get('href'), key)


def adjustName(name):
    name = name.split()
    firstName = name[-1]
    name.remove(firstName)
    name.insert(0, firstName)
    correctedNameWithComma = " ".join(name)
    correctedName = re.sub(",", "", correctedNameWithComma)
    return correctedName

def getCoordinates(areaHttpsLink):
    climbingAreaPageResponse = requests.get(areaHttpsLink).text
    climbingAreaSoup = BeautifulSoup(climbingAreaPageResponse, 'html.parser')
    tableData = climbingAreaSoup.findAll('td')

    for index, line in enumerate(tableData):
        if line.text == "GPS:":
            coordinates = re.sub("[A-z \n·]", "", tableData[index + 1].text.strip())
            return coordinates

# Using a web link, this method will get all of the information about a State, or a climbing area
def getAreaInformation(areaHttpsLink):
    stateResponse = requests.get(areaHttpsLink)
    stateSoup = BeautifulSoup(stateResponse.text, 'html.parser')
    climbingAreas = stateSoup.findAll('div', {'class': 'lef-nav-row'})
    coordinates = getCoordinates(areaHttpsLink)
    areaName = ''
    areaLink = ''
    
    for area in climbingAreas:
        areaAttributes = area.find('a')
        areaName = areaAttributes.text
        areaLink = areaAttributes.get('href')

        if "," in areaName:
            areaName = adjustName(areaName)
        print(areaName, ":", coordinates, " ", areaLink)
        
        buildSingleAreaInDatabase(areaName, areaLink, coordinates)  



def buildSingleAreaInDatabase(areaName, areaWebLink, coordinates):
  try:
    logging.warning("UPDATING OR CREATING AREA IN {}".format(areaName))
    
    coordinateArray = extrapolateCoordinates(coordinates)
    lattitude = coordinateArray[0]
    longitude = coordinateArray[1]

    # Build Database Object
    obj, created = cragModel.objects.update_or_create(crag_name = areaName, crag_link = areaWebLink, crag_lattitude = lattitude, crag_longitude = longitude)
  
  except:
    logging.warning("SOMETHING WENT WRONG WHEN ACCESSING MODEL LOCATIONS")


def extrapolateCoordinates(coordinatesString):
  coordinates = coordinatesString.split(",")
  return [coordinates[0].strip(), coordinates[1].strip()]


def buildLocationInDatabase(locationName, locationWebLink, locationKey):
    logging.warning("UPDATING OR CREATING LOCATION ENTRY: {}".format(locationName))
    obj, created = locationModel.objects.update_or_create(location_key = locationKey, location_name = locationName, location_web_link = locationWebLink)

def buildAllAreasInDataBase():
  for model in locationModel.objects.all():
    getAreaInformation(model.location_web_link)



# update the repositories every 12 hours
twelveHours = 43200

def updateDatabase():
  getLocationInformation(DATA_FOR_SCRAPING_URL)


# Initialize the database
getLocationInformation(DATA_FOR_SCRAPING_URL)
buildAllAreasInDataBase()


 



