# coding=utf-8
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
    with open("ImdbTop250.json","w",encoding='utf-8') as file:
        json.dump(filmData, file, ensure_ascii=False)

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
        filmData[idx+1] = f.__dict__
        print(f"Film {idx+1} done!")
    
    return filmData
##############################################################################################
def scrapDataFromImdbWebsite():
    url = "https://www.imdb.com/chart/top/"
    html = requests.get(url).content
    bSoup = BeautifulSoup(html, "html.parser")
    filmList = bSoup.find("tbody", {"class":"lister-list"}).find_all("tr")
    return filmList

def getCastList(castURL):
    htmlCast = requests.get(castURL).content
    bSoupForCast = BeautifulSoup(htmlCast,"html.parser")
    castList = bSoupForCast.find("div", {"id":"titleCast"}).find_all("tr",{"class":"odd"})
    castList = castList + bSoupForCast.find("div", {"id":"titleCast"}).find_all("tr",{"class":"even"})
    cast = {}
    for character in castList:
        try:
            name = character.find("td",{"class":"primary_photo"}).find("img")["title"].strip()
            role = character.find("td",{"class":"character"}).find("a").text
        except AttributeError:
            role = " ".join(character.find("td",{"class":"character"}).text.replace("\n","").strip().split())
        finally:
            cast[role]=name
    return cast

##############################################################################################
##### MAIN SECTION #####
while True:
    print("Menu".center(50, "*"))
    data = []
    choice = input("1 - Scrap data from IMDB website\n2 - Export data as a JSON file\n3 - Search data\n4 - Exit")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        print("Exiting.....")
        break
    else:
        print("Please enter valid value !")
