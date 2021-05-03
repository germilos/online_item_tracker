# Define all scraping functions here and put them in a Map
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from app.item import Item
from app.errors import NoHTMLElementFoundError
from app.util import CurrentPrice


# General scraping steps
def scrape(url):
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    page = requests.get(url, headers=user_agent)
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
        amount_and_currency = paragraphs[1].contents[1].string.split()
    else:
        amount_and_currency = paragraphs[1].string.string.split()
    price = CurrentPrice(amount=float(amount_and_currency[0].replace('.', '')), currency=amount_and_currency[1])
    available = True

    return Item(url, name, price, available, {})


def scrape_zara(url, page_to_scrap):
    container = page_to_scrap.find('div', class_='product-detail-info')
    if container is None:
        raise NoHTMLElementFoundError()

    name = container.h1.string
    price_span = container.find('span', class_='price__amount').string
    amount_and_currency = price_span.split()
    price = CurrentPrice(amount=float(amount_and_currency[0].replace(',', '')), currency=amount_and_currency[1])
    available = False

    selected_color_container = container.find('div', class_='product-detail-color-selector')
    selected_color = selected_color_container.p.contents[3]

    selected_size_container = container.find('div', class_='product-size-selector')
    size = selected_size_container.span.string

    return Item(url, name, price, available, {'color': selected_color, 'size': size})


def extract_website_name(url):
    domain = urlparse(url).netloc
    stripped_domain = domain[domain.index('.') + 1:domain.rfind('.')]

    return str(stripped_domain.split('.')[0])


#  TODO: Populate scraping functions map
scrape_map = {
    'metropolismusic': scrape_metropolis_music,
    'zara': scrape_zara
}
