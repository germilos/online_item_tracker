from flask import request, jsonify, make_response
from app import app
from app import item_scraper
from app.errors import InvalidUsageError
from app.models import ItemToTrack, OnlineShopper
from functools import wraps

import json
import flask_bcrypt


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            user_id = OnlineShopper.decode_auth_token(token)
            user = OnlineShopper.objects(id=user_id).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)

    return decorator


@app.route('/item-info')
def get_item_info():
    url = request.args.get('url')
    item = item_scraper.scrape(url)
    return json.loads(item.to_json())


@app.route('/items', methods=['POST'])
@token_required
def track_item():
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(' ')[1]
        shopper_id = OnlineShopper.decode_auth_token(token)

    # Get convert request to item
    item_to_track = ItemToTrack.from_json(request.data)
    item_to_track.shopper_id = shopper_id
    # Put item in database
    item_to_track.save()
    return f'Item with id: {item_to_track.id} is now being tracked!'


@app.route('/items/<item_id>', methods=['GET'])
@token_required
def get_tracked_item(item_id):
    tracked_item = ItemToTrack.objects(id=item_id).first()
    return json.loads(tracked_item.to_json())


@app.route('/auth/register', methods=['POST'])
def register_user():
    post_data = request.get_json()
    user = OnlineShopper.objects(email=post_data.get('email')).first()

    if not user:
        try:
            user = OnlineShopper.create_user(
                email=post_data.get('email'),
                password=post_data.get('password')
            )
            # insert the user
            user.save()

            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'message': 'Successfully registered!',
                'auth_token': auth_token  # tutorial says auth_token.decode()
            }

            return make_response(jsonify(response_object)), 201
        except Exception as e:
            response_object = {
                'message': 'An error has occurred while trying to register the user. Please try again.'
            }
            return make_response(jsonify(response_object)), 401
    else:
        responseObject = {
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


@app.route('/auth/login', methods=['POST'])
def login():
    post_data = request.get_json()
    try:
        # fetch the user data
        user = OnlineShopper.objects(email=post_data.get('email')).first()
        if user and flask_bcrypt.check_password_hash(
                user.password, post_data.get('password')
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
