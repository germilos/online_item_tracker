from flask import request
from flask import jsonify
from app import app
from app import item_scraper
from app.errors import InvalidUsageError


@app.route('/item')
def get_item_info():
    url = request.args.get('url')
    item = item_scraper.scrape(url)
    return item.to_json()


@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response