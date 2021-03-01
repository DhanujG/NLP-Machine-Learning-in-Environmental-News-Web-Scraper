from bs4 import BeautifulSoup
import requests
import re

""" returns a scraped {title: link} dict from bbc """
def scrape_bbc():
    website = "https://www.bbc.com/news/science_and_environment"
    # pattern is a regular expression for something that the links we actually want will contain
    pattern = re.compile("/news/science-environment")

    """ actual code starts here: """

    # grab html from website
    html = requests.get(website).text

    # parse out the link tags (<a></a>) from the html
    soup = BeautifulSoup(html, features="html.parser")
    all_link_tags = soup.find_all("a", href=pattern)

    articles = {}
    for tag in all_link_tags:
        # article headline is inside <h3> tag inside <a> tag 
        headline_tag = tag.find("h3")

        # some links are not for article headlines and thus don't have <h3> tags inside
        # so ignore them and add the others to the articles dictionary
        if headline_tag is None:
            continue

        # if you made it this far, the headline_tag exists and can be added
        # grab the actual headline from the <h3> tag
        headline = headline_tag.contents[0]

        # href is the attribute inside which the actual link url is stored
        url = tag["href"]
        # scraped url's don't include the bbc.com stuff at start, so add that here
        url = f"https://www.bbc.com{url}"
        # finally, add the (headline, url) pair to our articles dictionary
        articles[headline] = url
            
    return articles

print( scrape_bbc() )