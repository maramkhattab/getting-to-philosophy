import sys
import requests
import re
import time
from bs4 import BeautifulSoup


# ٌRandom
#url = "https://en.wikipedia.org/wiki/Special:Random"
# Loop
#url = "https://en.wikipedia.org/wiki/Greek_language"
# dead-end
url = "https://en.wikipedia.org/wiki/Great_American_Song_Contest"


def get_first_link(paragraphs):
    for paragraph in paragraphs:
        for ignored_child in paragraph.find_all(['span', 'small', 'sup', 'i']):
            ignored_child.replace_with("")

        # removing content within parentheses
        paragraph_text = str(paragraph)
        paragraph_text = re.sub(r' \(.*?\)', '', paragraph_text)
        paragraph = BeautifulSoup(paragraph_text, 'html.parser')
        links = paragraph.find_all("a")
        for link in links:
            if link.get('href') and "wiki" in link.get("href"):
                url = 'http://en.wikipedia.org' + link.get('href')
                return url

    return None


def get_to_philosophy(url):

    visited_urls = []
    while(1):

        response = requests.get(url)
        print(response.url)

        if visited_urls.count(response.url):
            print("Stuck in loop")
            return

        visited_urls.append(response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        if soup.find(id='firstHeading').text == 'Philosophy':
            print("Reached Philosophy")
            return

        content = []
        if soup.find_all("div", class_="mw-parser-output"):
            content = soup.find_all("div", class_="mw-parser-output")[0]

        for table in content.find_all("table"):
            table.replace_with("")

        paragraphs = content.find_all("p")
        url = get_first_link(paragraphs)

        if not url:
            print("No outbound links")
            break

        time.sleep(0.5)


if len(sys.argv) > 1:
    print(sys.argv[1])
    get_to_philosophy(sys.argv[1])
else:
    get_to_philosophy("https://en.wikipedia.org/wiki/Special:Random")
