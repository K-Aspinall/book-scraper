from bs4 import BeautifulSoup as bae
import requests

# -- Scrapping webpage --
# Specify URL
current_page = 'TODO ADD URL HERE'

while current_page is not None:
    # query the website and return the html response
    response = requests.get(current_page)
    # parse the html using beautiful soup and store as page
    page = bae(response.content, "html.parser")