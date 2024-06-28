import requests
from bs4 import BeautifulSoup
import csv
import re


def collect(url: str) -> BeautifulSoup:
    """Perform GET request and return soup object

    keyword arguments:
    - url: str = the https url
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    return soup


def find_computers(soup: BeautifulSoup) -> tuple:
    """Find every elements in the soup object"""
    containers = soup.find_all(class_="pdt-item")

    # Instrouvable sur le html de la page
    # prices = [c.find_all(class_="basket") for c in containers]

    names = [c.find("h3").text for c in containers]
    descriptions = [c.find(class_="desc").text for c in containers]
    stars = [r.find("span")["class"] for r in containers]
    reviews = [c.find(class_="ratingClient").text for c in containers]

    computers = tuple(
        {
            "NAME": n,
            "DESCRIPTION": descriptions[i],
            "STARS": stars[i],
            "NUMBER REVIEWS": reviews[i],
        }
        for i, n in enumerate(names)
    )

    return computers


def unpack_config(computer):
    """Extract informations about computer's configuration and store them in the dict"""

    # NAME part
    name = computer["NAME"]
    # Explanation : Brand | Model
    pattern_n = r"^(\w+) (.+)"
    match_n = re.search(pattern_n, name)
    config = {}
    if match_n:
        config["BRAND"] = match_n.group(1)
        config["MODEL"] = match_n.group(2)

    # DESCRIPTION part
    description = computer["DESCRIPTION"]
    # Explanation : Processor | RAM | Storage | Size screen
    pattern_d = r'(.+) ([0-9].+o) (\w+ [0-9].+o) ([0-9.]+")'
    match_d = re.search(pattern_d, description)
    if match_d:
        config["PROCESSOR"] = match_d.group(1)
        config["RAM"] = match_d.group(2)
        config["STORAGE"] = match_d.group(3)
        config["SIZE SCREEN"] = match_d.group(4)

    return config


def transform_number_review(computer: dict) -> dict:
    dictionnaire = {}

    # REVIEW part
    number_reviews = computer["NUMBER REVIEWS"]
    pattern = "([0-9]+)"
    match_r = re.search(pattern, number_reviews)
    if match_r:
        dictionnaire["NUMBER REVIEWS"] = match_r.group(1)
    elif not match_r:
        dictionnaire["NUMBER REVIEWS"] = "0"

    # STARS part
    stars = computer["STARS"][0]
    match_s = re.search(pattern, stars)
    if match_s:
        dictionnaire["STARS"] = match_s.group(1)
    elif not match_s:
        dictionnaire["STARS"] = "0"
    return dictionnaire


def keep_keys(computer):
    """Keep some keys and return the clean computer dict"""
    keys = [
        "BRAND",
        "MODEL",
        "PROCESSOR",
        "RAM",
        "STORAGE",
        "SIZE SCREEN",
        "NUMBER REVIEWS",
        "STARS",
    ]
    cleaned = {k: computer[k] for k in keys}
    return cleaned


def load_computers(computers):  #: tuple[dict[str, str]]) -> None:
    """Load the output of transformations"""

    # Build fields according to first dict
    fields = [k for k in computers[0].keys()]

    # Save to paretn folder
    with open("/home/sdvbigdata/SDV-DonneesDistribuees/computers.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(computers)

    return None


url = "https://www.ldlc.com/informatique/ordinateur-portable/pc-portable/c4265/"
soup = collect(url)
computers_raw = find_computers(soup)
computers_config = tuple(dict(c, **unpack_config(c)) for c in computers_raw)
computers_reviews = tuple(
    dict(c, **transform_number_review(c)) for c in computers_config
)
computers_cleaned = tuple(keep_keys(c) for c in computers_reviews)
load_computers(computers=computers_cleaned)
