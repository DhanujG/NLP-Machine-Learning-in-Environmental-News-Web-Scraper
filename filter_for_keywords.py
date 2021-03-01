# currently this only lowercases the title
# so stuff like "polar" and "Polar" match
# but other stuff like removing whitespace
# or more can be added later if needed
def normalize(title):
    return title.lower()


"""
articles is a { dictionary } of {"article title": "article url"}
keywords is a [ list ] of keywords

filter_for_keywords will return a new dictionary which only contains the articles
whose titles contain at least 1 of the keywords
"""
def filter_for_keywords(articles, keywords):
    # make an empty dictionary, which we will return at the end
    filtered_articles = {}
    
    for title, url in articles.items():
        # normalize ensures that two strings are in the same format
        # currently it only lowercases, them but it could be expanded to do more
        # like removing whitespace, etc...
        # this function is needed so stuff like "polar" and "Polar" match

        # normalize the title outside of the loop so its only done one time, and not once per keyword
        normalized_title = normalize(title)

        for keyword in keywords:
            # if keyword not in title, then try again with the next keyword
            if normalize(keyword) not in normalized_title:
                continue

            # if the code reaches here, then there was a successful keyword/title match
            # so add the title,url pair to the filtered dictionary
            # make sure to use the actual title and not the normalized version
            filtered_articles[title] = url

            # exit the loop early, no need to continue and go over every other keyword remaining
            break
    
    return filtered_articles