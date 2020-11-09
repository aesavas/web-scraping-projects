import requests
from bs4 import BeautifulSoup
import json

def getCastList(castURL):
    htmlCast = requests.get(castURL).content
    bSoupForCast = BeautifulSoup(htmlCast,"html.parser")
    castList = bSoupForCast.find("div", {"id":"titleCast"}).find_all("tr",{"class":"odd"})
    castList = castList + bSoupForCast.find("div", {"id":"titleCast"}).find_all("tr",{"class":"even"})
    cast = {}
    for character in castList:
        name = character.find("td",{"class":"primary_photo"}).find("img")["title"]
        role = character.find("td",{"class":"character"}).find("a").text
        cast[role]=name
    return cast


url = "https://www.imdb.com/chart/top/"
html = requests.get(url).content
bSoup = BeautifulSoup(html, "html.parser")

filmList = bSoup.find("tbody", {"class":"lister-list"}).find_all("tr",limit=1)

for film in filmList:
    posterLink = film.find("td",{"class":"posterColumn"}).find("img")["src"]
    title = film.find("td",{"class":"titleColumn"}).find("a").text
    year = film.find("td",{"class":"titleColumn"}).find("span").text.strip("()")
    rating = film.find("td",{"class":"ratingColumn imdbRating"}).find("strong").text
    castURL = "https://www.imdb.com"+film.find("td",{"class":"titleColumn"}).find("a")["href"]
    
    print(title.ljust(70,".")+ " - " + year+ " ----> "+ rating+ " ----> "+ castURL)
    getCastList(castURL)
    print("------------------------------------------------------------------------")

