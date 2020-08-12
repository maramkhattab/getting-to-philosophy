import sys
import requests
import re
from bs4 import BeautifulSoup

visited_urls = []
# ٌRandom
#url = "https://en.wikipedia.org/wiki/Special:Random"
# Loop
#url = "https://en.wikipedia.org/wiki/Greek_language"
# dead-end
url = "https://en.wikipedia.org/wiki/Great_American_Song_Contest"

while(1):

    response = requests.get(url)
    print(response.url)
    if visited_urls.count(response.url):
        print("Stuck in loop")
        break

    visited_urls.append(response.url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find(id='firstHeading').text == 'Philosophy':
        print("Reached Philosophy")
        break

    content = []
    if soup.find_all("div", class_="mw-parser-output"):
        content = soup.find_all("div", class_="mw-parser-output")[0]

    paragraphs = content.find_all("p")

    outbound_links = 0
    for paragraph in paragraphs:
        # print(paragraph)
        for ignored_child in paragraph.find_all(['span', 'small', 'sup', 'i', 'table']):
            # print(ignored_child)
            ignored_child.replace_with("")
        # print(paragraph)
        links = paragraph.find_all("a")
        for link in links:

            if link.get('href'):
                if "wiki" in link.get("href"):
                    url = 'http://en.wikipedia.org' + link.get('href')
                    outbound_links = 1
                    # print(url)
                    break
    if not outbound_links:
        print("No outbound links")
        break
