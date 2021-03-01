# This file contains a functional generalized news website scraper
# You can scrape essentially every news site in existence without writing a line of python

# if you want to scrape an unadded news site, simply add a dictionary with the
# neccessary keys to the scraper_inputs list below
# then run this file with: python3 generalized_scraper.py
# to get a dictionary of articles across every scraped site in the form {"headline": "url"}

# The magic occurs thanks to CSS Selectors, which allow us to scrape sites without writing
# custom python scraping code for each and every site. Instead a 1 line CSS selector pattern
# is enough to guide the generalized scraper through essentially any news site in existence

'''
    This is a list of websites to scrape. Each website is represented as a dictionary
    containing a human-readable 'name', the 'url' to access the website, a 'link_selector'
    and a 'headline_selector', and a 'prefix'.

    'prefix' is used because the links scraped from some websites (like BBC) are relative
    links (like '/news/science-environment-56133281'), but you need the full url to access
    that link outside of the BBC's website (like 
    'https://bbc.com/news/science-environment-56133281'). In this case, you would make the
    prefix 'https://bbc.com', and it'll get added to the start of each extracted link
    
    'link_selector' and 'headline_selector' contain CSS Selector Patterns that select for
    certain html elements in the html retrieved from the 'url'. The 'link_selector' 
    selects the (<a href=""></a>) tags containing the actual links to the articles on that
    website. 

    'link_selector' is run through BeautifulSoup.select() to return
    a list of link_tags. Then, for each link_tag, we run 'headline_selector' through 
    BeautifulSoup.select_one() to return the first matching headline_tag. A
    'headline_selector' of None indicates that the link_tag IS the headline_tag, aka the
    headline is merely text inside the link tag, like this: (<a href=""> Headline </a>).
    
    To be more specific, the 'headline_selector' selects the html tag whose sole inner 
    content is the actual headline for an article on the website. Since headlines are 
    usually included as children of the main link <a> tag, the 'headline_selector' is not
    a standalone selector from the root of the html tree. Instead, the 'headline_selector' 
    uses each selected <a> link tag as its starting point, and finds the first child of 
    that link tag which matches the 'headline_selector'. For instance, if the 
    'link_selector' is 'a[href ^= "/news"]' and the 'headline_selector' is 'h3', the value
    that will ultimately be returned is approximately equivalent to 
    'a[href ^= "/news"] h3', aka any <h3> tag that is the child of an <a> tag whose href 
    property starts with /news.

    For the selectors, please wrap the string with single-quotes ('') as much as possible 
    because the acutal css selectors heavily use double-quotes ("").
'''
scraper_inputs = [
    {
        'name': 'BBC Science & Environment',
        'url': 'https://www.bbc.com/news/science_and_environment',
        'prefix': 'https://bbc.com',
        'link_selector': 'a[href ^= "/news"].gs-c-promo-heading',
        'headline_selector': 'h3',
    },
    {
        'name': 'Detroit News',
        'url': 'https://www.detroitnews.com/news/',
        'prefix': 'https://www.detroitnews.com/story',
        'link_selector': 'a.gnt_m_flm_a',
        'headline_selector': None,
    },
    {
        'name': 'Mlive',
        'url': 'https://www.mlive.com/',
        'prefix': '',
        'link_selector': 'a[data-ga-content-type = "article"]',
        'headline_selector': None,
    },
]


#######################################################
## Configuration Ends Here, Actual Code Begins Below ##
#######################################################

import requests
from bs4 import BeautifulSoup
import sys


"""
    takes in strings

    returns a dictionary where each key is an article headline
    pointing to the url of that article
    {"headline": "url"}
"""
def scrape_website(url, prefix, link_selector, headline_selector):
    # create an empty dict to put stuff into
    # will look like {"headline" : "link"}
    # this will only include articles from a single website
    website_articles = {}
    
    # get the html from the website and pass it to BeautifulSoup
    # reason for using .content instead of .text: https://stackoverflow.com/a/24790752
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    # select all the article link tags
    article_link_tags = soup.select( link_selector )

    for link_tag in article_link_tags:
        # skip any link tags without an href attribute
        # as this results in them not linking to anything
        if not link_tag.has_attr('href'):
            continue

        # sometimes, the headline_tag IS the link_tag
        # for example, if the html looks like this:
        # <a href=""> The Headline </a>
        # In cases like this, mark the headline_selector as None
        # Otherwise, provide an actual headline_selector, and the
        # first child tag of the link tag matching that given headline_selector
        # will be made the headline_tag
        headline_tag = (
            link_tag if (headline_selector is None)
            else link_tag.select_one( headline_selector )
        )
        
        # extract headline from the headline_tag, and remove
        # whitespace, \n, \t from the left and right sides
        headline = headline_tag.get_text().strip()

        # make the actual article link url
        # prefix is in case site only uses relative links (e.g. BBC or Detroit News)
        link = prefix + link_tag['href']
        
        # add {headline:link} to the accumulative articles dictionary
        website_articles[headline] = link

    return website_articles


"""
    takes in a list of dictionaries
    each dict must have certain keys like url, prefix, link_selector, headline_selector

    get_articles returns a dictionary where each key is an article headline
    pointing to the url of that article
    {"headline": "url"}
"""
def get_articles(scraper_inputs):
    # create an empty dict to put stuff into
    # will look like {"headline" : "link"}
    # this will include articles from every single website scraped
    all_articles = {}

    for website in scraper_inputs:
        # use try/except blocks so that an error in scraping one website
        # will be overlooked and the loop will continue to the next website
        # instead of crashing the whole program
        try:
            # get new articles from a new website
            website_articles = scrape_website(
                url=website['url'],
                prefix=website['prefix'],
                link_selector=website['link_selector'],
                headline_selector=website['headline_selector']
            )
            # add the new articles to the accumulative articles dict
            all_articles.update(website_articles)

        except:
            print('Something went wrong with:')
            print(website)
            print('The error is:')
            print(sys.exc_info()[0])

    # after scraping every website, return the accumulative articles from every website
    return all_articles


articles = get_articles(scraper_inputs)
print(articles)

