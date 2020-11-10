import requests
from bs4 import BeautifulSoup
import json

##############################################################################################
class Film:
    def __init__(self, posterLink, title, year, rating, cast):
        self.posterLink = posterLink
        self.title = title
        self.year = year
        self.rating = rating
        self.cast = cast

##############################################################################################

def createJsonFile(filmData):
    with open("ImdbTop250.json","w") as file:
        json.dump(filmData, file)

##############################################################################################
def getCastList(castURL):
    htmlCast = requests.get(castURL).content
    bSoupForCast = BeautifulSoup(htmlCast,"html.parser")
    castList = bSoupForCast.find("div", {"id":"titleCast"}).find_all("tr",{"class":"odd"})
    castList = castList + bSoupForCast.find("div", {"id":"titleCast"}).find_all("tr",{"class":"even"})
    cast = {}
    for character in castList:
        name = character.find("td",{"class":"primary_photo"}).find("img")["title"]
        role = character.find("td",{"class":"character"}).find("a").text
        #TO DO: It gives error because some of role names are not link. Write try except block
        cast[role]=name
    return cast

##############################################################################################
def createDictionaryFromData(filmList):
    filmData = {}
    for idx, film in enumerate(filmList):
        posterLink = film.find("td",{"class":"posterColumn"}).find("img")["src"]
        title = film.find("td",{"class":"titleColumn"}).find("a").text
        year = film.find("td",{"class":"titleColumn"}).find("span").text.strip("()")
        rating = film.find("td",{"class":"ratingColumn imdbRating"}).find("strong").text
        castURL = "https://www.imdb.com"+film.find("td",{"class":"titleColumn"}).find("a")["href"]
        castData = getCastList(castURL)
        f = Film(posterLink, title, year, rating, castData)
        filmData[idx] = f.__dict__
    
    return filmData
##############################################################################################

url = "https://www.imdb.com/chart/top/"
html = requests.get(url).content
bSoup = BeautifulSoup(html, "html.parser")
filmList = bSoup.find("tbody", {"class":"lister-list"}).find_all("tr",limit=5)
createJsonFile(createDictionaryFromData(filmList))
