from bs4 import BeautifulSoup
import requests

def scrape_mlive():
    website = "https://www.mlive.com/"

    # grab html from website
    html = requests.get(website).text

    # parse out the link tags (<a></a>) from the html
    # only select tags with attribute data-ga-content-type = article
    soup = BeautifulSoup(html, features="html.parser")
    all_link_tags = soup.find_all("a", {"data-ga-content-type":"article"})

    articles = {}

    #create dictionary mapping article titles to article links
    for tag in all_link_tags:
      # ignore tags that do not contain anything
      if tag.string is None:
        continue
        #tag headline can be obtained at tag.string
        #tag url stored in the attribute "href", accessed with tag["href"] 
      articles[tag.string] = tag["href"]
            
    return articles

print( scrape_mlive() )