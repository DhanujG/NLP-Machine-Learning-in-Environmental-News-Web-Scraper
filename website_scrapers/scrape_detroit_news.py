from bs4 import BeautifulSoup
import requests
import unicodedata

def scrape_detroit_news():
    website = 'https://www.detroitnews.com/news/'
    
    # get html from website
    html = requests.get(website).text

    # parse html to find the link
    soup = BeautifulSoup(html, features="html.parser")
    all_link_tags = soup.find_all("a", class_="gnt_m_flm_a")
    print(all_link_tags)
    # make an empty dictionary to contain articles to return later
    articles = {}

    for tag in all_link_tags:
      # ignore tags that do not contain anything
      #if tag.string is None:
      #  continue
        #tag headline can be obtained at tag.string
        #tag url stored in the attribute "href", accessed with tag["href"] 
      #title = tag.find_all({"data-c-br":"")
      if len(tag["class"]) > 1:
        continue
      if not tag.has_attr("href"):
        return

      title = unicodedata.normalize("NFKD", tag["data-c-br"])
      articles[title] = "https://www.detroitnews.com" + tag["href"]
    return articles

print( scrape_detroit_news() )