# Define all scraping functions here and put them in a Map
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from app.models import Item, CurrentPrice
from app.errors import NoHTMLElementFoundError
from app.util import get_chrome_driver_with_options


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
    available = True

    driver = get_chrome_driver_with_options('--ignore-certificate-errors', '--incognito', '--headless')
    driver.get(url)

    # TODO: Refactor
    color_buttons = driver.find_elements_by_class_name("product-detail-color-selector__color-button")
    sizes_by_color = {}
    for button in color_buttons:
        driver.execute_script("arguments[0].click();", button)
        page = BeautifulSoup(driver.page_source, 'html.parser')

        container = page.find('div', class_='product-detail-info')

        colors_list = container.find('ul', class_='product-detail-color-selector__colors')
        selected_color_element = colors_list.find('li', class_='product-detail-color-selector__color product-detail-color-selector__color--is-selected')
        selected_color = selected_color_element.span.string

        selected_size_container = container.find('div', class_='product-size-selector')
        available_sizes = selected_size_container.find_all('li')
        size_numbers = []
        for size in available_sizes:
            if 'product-size-selector__size-list-item--out-of-stock' not in size.get('class'):
                size_numbers.append(size.span.string)

        sizes_by_color[selected_color] = size_numbers

    return Item(url, name, price, available, {'sizes_by_color': sizes_by_color})


def extract_website_name(url):
    domain = urlparse(url).netloc
    stripped_domain = domain[domain.index('.') + 1:domain.rfind('.')]

    return str(stripped_domain.split('.')[0])


#  TODO: Populate scraping functions map
scrape_map = {
    'metropolismusic': scrape_metropolis_music,
    'zara': scrape_zara
}
