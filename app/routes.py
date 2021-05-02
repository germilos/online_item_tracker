from flask import request, make_response
from flask import jsonify
from app import app
from app import item_scraper
from app.errors import InvalidUsageError
from app.item import ItemToTrack
import json


@app.route('/item-info')
def get_item_info():
    url = request.args.get('url')
    item = item_scraper.scrape(url)
    return json.loads(item.to_json())


@app.route('/items', methods=['POST'])
def track_item():
    # Get convert request to item
    item_to_track = ItemToTrack.from_json(request.data)
    # Put item in database
    item_to_track.save()
    return f'Item with url: {item_to_track.url} is now being tracked!'

@app.route('/items', methods=['GET'])
def get_tracked_item():
    url = request.args.get('url')
    # Put item in database
    tracked_item = ItemToTrack.objects(url=url).first()
    return json.loads(tracked_item.to_json())


@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
