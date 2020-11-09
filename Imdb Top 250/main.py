import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/top/"
html = requests.get(url).content
bSoup = BeautifulSoup(html, "html.parser")

filmList = bSoup.find("tbody", {"class":"lister-list"}).find_all("tr",limit=10)

for film in filmList:
    posterLink = film.find("td",{"class":"posterColumn"}).find("img")["src"]
    title = film.find("td",{"class":"titleColumn"}).find("a").text
    year = film.find("td",{"class":"titleColumn"}).find("span").text.strip("()")
    rating = film.find("td",{"class":"ratingColumn imdbRating"}).find("strong").text
    print(title.ljust(70,".")+ " - " + year+ " ----> "+ rating)
