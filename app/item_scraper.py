# Define all scraping functions here and put them in a Map
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from app.item import Item
from app.errors import NoHTMLElementFoundError


# General scraping steps
def scrape(url):
    page = requests.get(url)
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    website_name = extract_website_name(url)
    try:
        return scrape_map[website_name](url, parsed_page)
    except NoHTMLElementFoundError as err:
        raise err


# Website specific
def scrape_metropolis_music(url, page_to_scrap):
    container = page_to_scrap.find('div', class_='productBoxTxt')
    if container is None:
        raise NoHTMLElementFoundError()

    record = container.h1.string
    paragraphs = container('p')
    artist = paragraphs[0].string
    name = f'{record} - {artist}'
    if len(paragraphs[1].contents) == 2:
        price = paragraphs[1].contents[1].string
    else:
        price = paragraphs[1].string
    available = True

    return Item(url, name, price, available, {})


def extract_website_name(url):
    domain = urlparse(url).netloc
    stripped_domain = domain[domain.index('.') + 1:domain.rfind('.')]

    return str(stripped_domain.split('.')[0])


#  TODO: Populate scraping functions map
scrape_map = {
    'metropolismusic': scrape_metropolis_music
}
