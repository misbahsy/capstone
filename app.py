import os
from flask import Flask, request, abort, jsonify, render_template, session, url_for, redirect
import json 
from flask_cors import CORS 
from models import setup_db, Magician, Show, db
from auth import AuthError, requires_auth, requires_signed_in
from authlib.flask.client import OAuth


AUTH0_CALLBACK_URL = 'http://localhost:5000/callback'
AUTH0_CLIENT_ID = '8I3eP5XFElTZ71kFUtDp3GhZ0qIJ9lv2' 
AUTH0_CLIENT_SECRET =  'naB0-3lz6-EHpGQaUYt8zQs_bO9b1SqTVrm6Bnb7ewUNLln9RxyBGNOJ3sDPhcrk' 
AUTH0_DOMAIN = 'dev-v6tg4f3z.us.auth0.com' 
AUTH0_BASE_URL = 'https://' + 'dev-v6tg4f3z.us.auth0.com'
AUTH0_AUDIENCE = 'magic'


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    
    #taken from auth0 website instructions
    oauth = OAuth(app)


    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    #taken from instructions at auth0 
    @app.route('/')
    def index():
        return 'Healthy app'
    
    # Route for getting all shows
    @app.route('/shows')
    @requires_auth('get:shows')
    def get_shows(jwt):
        """Get all shows route"""
        try:
            shows = Show.query.all()

            return jsonify({
                'success': True,
                'shows': [show.format() for show in shows],
            }), 200
        except:
            abort(404)

    # Route for getting a specific show
    @app.route('/shows/<int:id>')
    @requires_auth('get:shows')
    def get_show_by_id(jwt, id):
        """Get a specific show route"""
        try:
            show = Show.query.get(id)   
        # return 404 if there is no show with id
            if show is None:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                    'show': show.format(),
                }), 200
        except:
            abort(404)

    @app.route('/shows', methods=['POST'])
    @requires_auth('post:shows')
    def post_show(jwt):
        """Create a show route"""
        # Process request data
        data = request.get_json()
        show_name = data.get('show_name', None)
        show_date = data.get('show_date', None)

        # return 400 for empty show_name or show date
        if show_name is None or show_date is None:
            abort(400)

        show = Show(show_name=show_name, show_date=show_date)

        try:
            show.insert()
            return jsonify({
                'success': True,
                'show': show.format()
            }), 200
        except:
            abort(404)

    @app.route('/shows/<int:id>', methods=['PATCH'])
    @requires_auth('patch:shows')
    def patch_show(jwt, id):
        """Update a show route"""

        data = request.get_json()
        show_name = data.get('show_name', None)
        show_date = data.get('show_date', None)

        show = Show.query.get(id)

        if show:
            if show is None:
                abort(400)

            if show_name is None or show_date is None:
                abort(400)

            show.show_name = show_name
            show.show_date = show_date

            try:
                show.update()
                return jsonify({
                    'success': True,
                    'show': show.format()
                }), 200
            except:
                abort(422)
        else:
            abort(404)

    @app.route('/shows/<int:id>', methods=['DELETE'])
    @requires_auth('delete:shows')
    def delete_show(jwt, id):
        """Delete a show route"""
        show = Show.query.get(id)
        if show:
            if show is None:
                abort(400)
            try:
                show.delete()
                return jsonify({
                    'success': True,
                    'message':
                    f'show id {show.id}, show named {show.show_name} was deleted',
                })
            except:
                db.session.rollback()
                abort(422)
        else:
            abort(404)



    @app.route('/magicians')
    @requires_auth('get:magicians')
    def get_magicians(jwt):
        """Get all magicians route"""
        try:
            magicians = Magician.query.all()

            return jsonify({
                'success': True,
                'magicians': [magician.format() for magician in magicians],
            }), 200
        except:
            abort(404)

    @app.route('/magicians/<int:id>')
    @requires_auth('get:magicians')
    def get_magician_by_id(jwt, id):
        """Get all magicians route"""
        magician = Magician.query.get(id)
        try:
            if magician is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'magician': magician.format(),
                }), 200
        except:
            abort(404)

    @app.route('/magicians', methods=['POST'])
    @requires_auth('post:magicians')
    def post_magician(jwt):
        """Get all shows route"""
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        magician = Magician(name=name, age=age, gender=gender)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            magician.insert()
            return jsonify({
                'success': True,
                'magician': magician.format()
            }), 200
        except:
            abort(422)

    @app.route('/magicians/<int:id>', methods=['PATCH'])
    @requires_auth('patch:magicians')
    def patch_magician(jwt, id):
        """Update an magician Route"""

        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        magician = Magician.query.get(id)
        if magician:

            if magician is None:
                abort(400)

            if name is None or age is None or gender is None:
                abort(400)

            magician.name = name
            magician.age = age
            magician.gender = gender

            try:
                magician.update()
                return jsonify({
                    'success': True,
                    'magician': magician.format()
                }), 200
            except:
                abort(422)
        else:
            abort(404)

    @app.route('/magicians/<int:id>', methods=['DELETE'])
    @requires_auth('delete:magicians')
    def delete_magician(jwt, id):
        """Delete an magician Route"""
        magician = Magician.query.get(id)
        if magician:
            if magician is None:
                abort(404)
            try:
                magician.delete()
                return jsonify({
                    'success': True,
                    'message':
                    f'magician id {magician.id}, named {magician.name} was deleted',
                })
            except:
                db.session.rollback()
                abort(422)
        else:
            abort(404)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)