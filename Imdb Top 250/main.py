# coding=utf-8
import requests
from bs4 import BeautifulSoup
import json

##### CLASS SECTION #####
"""
    I wanted to store the data as a class. So, I created this class.
    It includes poster link, title of movie, release year, rating and cast.
"""
class Film:
    def __init__(self, posterLink, title, year, rating, cast):
        self.posterLink = posterLink
        self.title = title
        self.year = year
        self.rating = rating
        self.cast = cast

#### FUNCTION SECTION #####
def scrapDataFromImdbWebsite():
    """
        This function scrap data from website. Firstly, get HTML content via requests module.
        After that, it parses html content via BeautifulSoup module. It does not take parameters.
    """
    url = "https://www.imdb.com/chart/top/"
    html = requests.get(url).content
    bSoup = BeautifulSoup(html, "html.parser")
    filmList = bSoup.find("tbody", {"class":"lister-list"}).find_all("tr")
    return filmList

def getCastList(castURL):
    """
        This function works like scrapDataFromWebsite() function. It scrapes data from given url.
        It takes a parameter. (URL for cast). Then, it returns a dictionary that includes cast.
    """
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

def createDictionaryFromData(filmList):
    """
        This function returns a dictionary that includes data about IMDB Top 250 movies. 
        It takes a parameter as scraped and parsed HTML content. It takes time when it is working.
    """
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
        print(f'Film {idx+1} done!')
    print("All films are ready to use!\n\n")
    return filmData

def printData(dictData):
    """
        This function prints data properly that created dictionary.
    """
    idx = 1
    for filmData in dictData.values():
        print(f'Film {idx}'.center(70,"."))
        print(f'Title : {filmData["title"]}\nYear : {filmData["year"]}\nRating : {filmData["rating"]}')
        print("Cast".center(70,"_"))
        for role,performer in filmData["cast"].items():
            print(f'Role : {role.ljust(35)} Performer : {performer}')
        print("\n")
        idx += 1

def createJsonFile(filmData):
    """
        This function export JSON file that I created.
    """
    with open("ImdbTop250.json","w",encoding='utf-8') as file:
        json.dump(filmData, file, ensure_ascii=False)

##### MAIN SECTION #####
data = []
dictData = {}
while True:
    print("Menu".center(32, "*"))
    choice = input("1 - Export data as a JSON file\n2 - Print data\n3 - Exit\nPlease enter choice : ")
    if choice == "3":
        print("Exiting.....")
        break
    else:
        if len(data) == 0:
            data = scrapDataFromImdbWebsite()
            dictData = createDictionaryFromData(data)
        if choice == "1":
            createJsonFile(dictData)
            print("JSON file is ready.")
        elif choice == "2":
            printData(dictData)
        else:
            print("Please enter valid value !")
