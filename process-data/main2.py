import requests
from bs4 import BeautifulSoup

def collect(url: str) -> BeautifulSoup :
    """Perform GET request and return soup object

    keyword arguments:
    - url: str = the https url
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    content = response.content
    soup=BeautifulSoup(content, 'html.parser')
    return soup

def find_computers(soup: BeautifulSoup) -> list:
    """Find every elements in the soup object"""
    containers = soup.find_all(class_='pdt-item')
    names = [c.find('h3').text for c in containers]
    descriptions = [c.find(class_='desc').text for c in containers]
    #prices = [c.find_all(class_="basket") for c in containers] #price ne pourra pas être récupéré
    review = [c.find(class_ = 'ratingClient').text for c in containers]

    return names, descriptions, review


url = "https://www.ldlc.com/informatique/ordinateur-portable/pc-portable/c4265/"
soup = collect(url)
print(find_computers(soup)[2])
