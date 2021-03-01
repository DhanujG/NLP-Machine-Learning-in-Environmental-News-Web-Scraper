''' 
pythonanywhere has a whitelist of sites
and free users are only allowed to request html from those
whitelisted sites

either ask pythonanywhere to add sites to whitelist or
check out how to deploy on AWS instead maybe:

https://victormerino.medium.com/running-a-python-script-24-7-in-cloud-for-free-amazon-web-services-ec2-76af166ae4fb
'''

# folder that the scrapers are in
SCRAPERS_FOLDER_NAME = 'website_scrapers'

"""
To add new scrapers, put the scraping function into its own file in the website_scrapers folder.

See the existing examples in the website_scrapers folder for clarification.

Next, add the name of the file and function names that the scraper is in to the array below.
"""
# file name first, then function name
SCRAPERS = [
  ['scrape_bbc.py', 'scrape_bbc'],
  ['scrape_detroit_news.py', 'scrape_detroit_news'],
  ['scrape_mlive.py', 'scrape_mlive']
]

KEYWORDS = [
  "ocean",
  "polar",
  "electric",
  "nature",
  "iceberg",
  "biodiversity",
  "green",
  "warm",
  "biology",
  "plant",
  "living",
  "carbon",
  "coronavirus",
  'abatement',
  'acid',
  'air pollution',
  'air quality',
  'algae',
  'algal blooms',
  'alternative energy sources',
  'amenities',
  'atmosphere',
  'backyard burning',
  'ber',
  'biodegradable waste',
  'biodiversity',
  'bioenergy',
  'biofuels',
  'biomass',
  'biosphere',
  'black bin (grey bin)',
  'bring bank',
  'brown bin',
  'bye-law',
  'carbon',
  'carpooling',
  'cfcs',
  'cfl bulbs',
  'civic amenity site',
  'climate',
  'climate change',
  'compost',
  'compostable',
  'composting',
  'conservation',
  'cryptosporidium',
  'deforestation',
  'development plan',
  'dioxins',
  'disposal',
  'domestic charges',
  'domestic waste',
  'draught proofing',
  'dumping',
  'ecosystem',
  'ecotourism',
  'effluent',
  'electric vehicle',
  'emissions',
  'emissions projections',
  'emssions trading allowance',
  'end-of-life vehicle',
  'energy efficiency',
  'energy rating',
  'energy star',
  'environmental impact statement',
  'flora and fauna',
  'fossil fuels',
  'fuel poverty',
  'global warming',
  'green bin',
  'green design',
  'greener homes scheme',
  'greenhouse effect',
  'greenhouse gases',
  'ground water',
  'habitat',
  'hazardous waste',
  'home energy saving scheme',
  'household waste',
  'incinerator',
  'insulation',
  'kyoto protocol',
  'kyoto agreement',
  'landfill',
  'litter',
  'mbt',
  'mulch',
  'municipal waste',
  'noise pollution',
  'npws',
  'nss',
  'noxious gases',
  'oil spill',
  'organic food',
  'organic',
  'organism',
  'ozone layer',
  'particulate matter',
  'pay by weight',
  'pesticides',
  'permits',
  'planning permission',
  'plastic bag levy',
  'post-consumer waste',
  'radiation',
  'radioactive',
  'radon',
  'recycle',
  'reforestation',
  'refuse',
  'renewable',
  'reuse',
  'river basin',
  'sewage',
  'smog',
  'smokeless fuel',
  'solar panel',
  'standing charges',
  'surface water',
  'sustainable',
  'toxic',
  'toxin',
  'traffic calming',
  'traffic management',
  'tidy towns',
  'utility',
  'un framework convention on climate change',
  'unesco world heritage site',
  'ventilation',
  'warmer homes scheme',
  'waste management',
  'waste prevention',
  'water vapour',
  'weee',
  'wind energy',
  'wind turbine',
  'zero emissions',
]

################################################################
# Configuration Stuff Above, Main Code Below
################################################################

# flask: web framework for rendering website
from flask import Flask, render_template

# importlib: dynamically import scrapers (no need to add new functions and stuff below when additional scrapers are made)
from importlib import import_module 

from filter_for_keywords import filter_for_keywords

# dynamically imports the scraper functions from the scrapers array (each scraper in the array is itself an array where the first item is the name of the file the scraper is in and the second item the name of the scraping function within that file)
# returns a list of all the imported scraper functions
def import_scraper_functions(folder_name, scrapers):
  # list to be returned at end containing all the imported scraper functions
  all_scraper_functions = []

  # import each scraper_function, and use it to
  # scrape and filter articles from each website
  # and finally add every article into all_articles
  for file_name, function_name in scrapers:
    # remove the .py from end if its included in original file_name
    # this is because import_module only takes in the file_name without any .py extension
    if file_name.endswith('.py'):
      file_name = file_name[:-3]

    # format the filepath so that it can be imported by import_module
    formatted_filepath = folder_name + '.' + file_name

    # import the file containing the scraping function
    scraper_file = import_module(formatted_filepath)

    # get the actual scraping function from the imported file
    scraper_function = getattr(scraper_file, function_name)


    # add newly imported scraper function to the overarching list
    all_scraper_functions.append(scraper_function)

  return all_scraper_functions

# runs all the scraper functions in the list given to it
# and uses them to scrape, and filter, the articles from each website
# finally, it returns a giant dictionary containing all the scraped and filtered articles across all the websites
# this function may need to be made async in the future, if it takes too much time to run all the scrapers 1-by-1
def get_articles(scraper_functions, keywords):
  # will use this to return combined filtered articles dictionary across all websites
  # keys are article titles, vals are article url's
  all_articles = {}

  for scraper_function in scraper_functions:
    # run the scraper
    scraped_articles = scraper_function()
    filtered_articles = filter_for_keywords(scraped_articles, keywords)
    # add scraped & filtered articles from a particular website to all_articles
    all_articles.update(filtered_articles)
  
  return all_articles

app = Flask('app')

@app.route('/')
def main():
  # import the various scraper functions we made
  scraper_functions = import_scraper_functions(SCRAPERS_FOLDER_NAME, SCRAPERS)

  # run the scraper functions, and filter the scraped articles, and combine all articles into one dictionary
  articles = get_articles(scraper_functions, KEYWORDS)

  # make the actual website
  return render_template('main.html', articles=articles )

@app.route('/generalized_scraper')
def run_generalized_scraper():
  import generalized_scraper

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
    }
  ]

  articles = generalized_scraper.get_articles(scraper_inputs)

  articles = filter_for_keywords(articles, KEYWORDS)

  return render_template('main.html', articles=articles)

app.run(host='0.0.0.0', port=8080)