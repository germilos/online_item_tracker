from app.item_scraper import scrape
import pytest


@pytest.mark.vcr()
def test_should_scrape_metropolis_music_online_item_info_when_given_item_url():
    item = scrape('https://www.metropolismusic.rs/vs.6218155.html')
    assert item.url == 'https://www.metropolismusic.rs/vs.6218155.html'
    assert item.name == 'Vs. - Pearl Jam'
    assert item.price.amount == 3499.00
    assert item.available is True
