from flask import request, make_response
from flask import jsonify
from app import app
from app import item_scraper
from app.errors import InvalidUsageError
from app.item import ItemToTrack


@app.route('/item-info')
def get_item_info():
    url = request.args.get('url')
    item = item_scraper.scrape(url)
    return item.to_json()


@app.route('/items', methods=['POST'])
def track_item():
    # Get convert request to item
    item_to_track = ItemToTrack.from_json(request.data)
    # Put item in database
    item_to_track.save()
    return f'Item with url: {item_to_track.url} is now being tracked!'


@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
