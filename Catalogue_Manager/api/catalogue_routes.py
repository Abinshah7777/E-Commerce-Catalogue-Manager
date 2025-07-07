from flask import session, redirect, url_for, request
from flask_restx import Resource, fields, Namespace
from service.catalogue_service import CatalogueService
from dto.catalogue_dto import Catalogue
from exceptions.exceptions import CatalogueNotFoundError, InvalidCatalogueInputError, CatalogueAlreadyExistsError
from datetime import datetime
import logging
from service.authentication_service import AuthenticationService
from exceptions.exceptions import InvalidCredentialsError

# Create namespace
catalogue_ns = Namespace('catalogues', description='Catalogue management operations')
auth_ns = Namespace('auth', description='Authentication operations')

# Define Swagger models
catalogue_model = catalogue_ns.model('Catalogue', {
    'catalogue_id': fields.Integer(required=True, description='Catalogue ID'),
    'catalogue_name': fields.String(required=True, description='Catalogue name'),
    'catalogue_version': fields.String(required=True, description='Catalogue version'),
    'is_cat_active': fields.Boolean(required=True, description='Is catalogue active'),
    'catalogue_start': fields.String(required=True, description='Catalogue start date (YYYY-MM-DD)'),
    'catalogue_end': fields.String(required=True, description='Catalogue end date (YYYY-MM-DD)'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

catalogue_input = catalogue_ns.model('CatalogueInput', {
    'catalogue_id': fields.Integer(required=True, description='Catalogue ID'),
    'catalogue_name': fields.String(required=True, description='Catalogue name'),
    'catalogue_version': fields.String(required=True, description='Catalogue version'),
    'is_cat_active': fields.Integer(required=True, description='Is catalogue active (0 or 1)'),
    'catalogue_start': fields.String(required=True, description='Catalogue start date (YYYY-MM-DD)'),
    'catalogue_end': fields.String(required=True, description='Catalogue end date (YYYY-MM-DD)')
})

catalogue_update = catalogue_ns.model('CatalogueUpdate', {
    'catalogue_name': fields.String(required=True, description='Catalogue name'),
    'catalogue_version': fields.String(required=True, description='Catalogue version'),
    'is_cat_active': fields.Integer(required=True, description='Is catalogue active (0 or 1)'),
    'catalogue_start': fields.String(required=True, description='Catalogue start date (YYYY-MM-DD)'),
    'catalogue_end': fields.String(required=True, description='Catalogue end date (YYYY-MM-DD)')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# Initialize service
service = CatalogueService()
auth_service = AuthenticationService()

# Helper function to check authentication
def check_auth():
    if 'username' not in session:
        catalogue_ns.abort(401, 'Authentication required')

@catalogue_ns.route('/')
class CatalogueList(Resource):
    @catalogue_ns.doc('list_catalogues')
    @catalogue_ns.marshal_with(catalogue_model, as_list=True)
    def get(self):
        """Retrieve all catalogues"""
        check_auth()
        try:
            logging.info(f'User "{session["username"]}" fetched all catalogues via Swagger.')
            catalogues = service.get_all_catalogues()
            return [catalogue.to_dict() for catalogue in catalogues]
        except Exception as e:
            logging.error(f'Error fetching catalogues for user "{session["username"]}" via Swagger: {e}', exc_info=True)
            catalogue_ns.abort(500, "Unexpected error occurred. Please try again later.")
    
    @catalogue_ns.doc('create_catalogue')
    @catalogue_ns.expect(catalogue_input)
    @catalogue_ns.marshal_with(catalogue_model, code=201)
    def post(self):
        """Create a new catalogue"""
        check_auth()
        try:
            data = catalogue_ns.payload
            if not all(key in data for key in ['catalogue_id', 'catalogue_name', 'catalogue_version', 'is_cat_active', 'catalogue_start', 'catalogue_end']):
                raise InvalidCatalogueInputError("Invalid input: one or more required fields are missing or empty.")

            # Date validation
            start_date = datetime.strptime(data['catalogue_start'], '%Y-%m-%d')
            end_date = datetime.strptime(data['catalogue_end'], '%Y-%m-%d')
            today = datetime.today().date()

            if start_date.date() <= today or end_date.date() <= today:
                logging.warning(f'User "{session["username"]}" attempted to create a catalogue with past or today\'s date via Swagger.')
                catalogue_ns.abort(400, "Catalogue start and end dates must be in the future.")

            if end_date <= start_date:
                logging.warning(f'User "{session["username"]}" entered end date before start date via Swagger.')
                catalogue_ns.abort(400, "Catalogue end date must be after the start date.")

            catalogue = Catalogue(
                catalogue_id=int(data['catalogue_id']),
                catalogue_name=data['catalogue_name'],
                catalogue_version=data['catalogue_version'],
                is_cat_active=bool(int(data['is_cat_active'])),
                catalogue_start=data['catalogue_start'],
                catalogue_end=data['catalogue_end']
            )

            service.create_catalogue(catalogue)
            logging.info(f'User "{session["username"]}" created catalogue with ID {catalogue.catalogue_id} via Swagger.')
            return catalogue.to_dict(), 201

        except CatalogueAlreadyExistsError as e:
            logging.warning(f'User "{session["username"]}" attempted to create a duplicate catalogue ID {data.get("catalogue_id")} via Swagger.')
            catalogue_ns.abort(409, str(e))

        except (InvalidCatalogueInputError, ValueError) as e:
            logging.warning(f'Invalid input from user "{session["username"]}" via Swagger: {e}')
            catalogue_ns.abort(400, "Invalid input: field types are incorrect or required fields are missing.")

        except Exception as e:
            logging.error(f'Unexpected error during catalogue creation by user "{session["username"]}" via Swagger: {e}', exc_info=True)
            catalogue_ns.abort(500, "Unexpected error occurred. Please try again later.")

@catalogue_ns.route('/<int:catalogue_id>')
@catalogue_ns.param('catalogue_id', 'The catalogue identifier')
class CatalogueItem(Resource):
    @catalogue_ns.doc('get_catalogue')
    @catalogue_ns.marshal_with(catalogue_model)
    def get(self, catalogue_id):
        """Retrieve a specific catalogue"""
        check_auth()
        try:
            catalogue = service.get_catalogue_by_id(catalogue_id)
            logging.info(f'User "{session["username"]}" fetched catalogue with ID {catalogue_id} via Swagger.')
            return catalogue.to_dict()
        except CatalogueNotFoundError:
            logging.warning(f'User "{session["username"]}" tried to fetch non-existent catalogue ID {catalogue_id} via Swagger.')
            catalogue_ns.abort(404, "Catalogue with the specified ID does not exist.")
        except Exception as e:
            logging.error(f'Error fetching catalogue ID {catalogue_id} for user "{session["username"]}" via Swagger: {e}', exc_info=True)
            catalogue_ns.abort(500, "Unexpected error occurred. Please try again later.")
    
    @catalogue_ns.doc('update_catalogue')
    @catalogue_ns.expect(catalogue_update)
    @catalogue_ns.marshal_with(catalogue_model)
    def put(self, catalogue_id):
        """Update a catalogue"""
        check_auth()
        try:
            data = catalogue_ns.payload
            if not all(key in data for key in ['catalogue_name', 'catalogue_version', 'is_cat_active', 'catalogue_start', 'catalogue_end']):
                raise InvalidCatalogueInputError("Invalid input: one or more required fields are missing or empty.")

            # Date validation
            start_date = datetime.strptime(data['catalogue_start'], '%Y-%m-%d')
            end_date = datetime.strptime(data['catalogue_end'], '%Y-%m-%d')
            today = datetime.today().date()

            if start_date.date() <= today or end_date.date() <= today:
                logging.warning(f'User "{session["username"]}" attempted to update catalogue ID {catalogue_id} with past or today\'s date via Swagger.')
                catalogue_ns.abort(400, "Catalogue start and end dates must be in the future.")

            if end_date <= start_date:
                logging.warning(f'User "{session["username"]}" attempted to set end date before start date for catalogue ID {catalogue_id} via Swagger.')
                catalogue_ns.abort(400, "Catalogue end date must be after the start date.")

            updated = Catalogue(
                catalogue_id=catalogue_id,
                catalogue_name=data['catalogue_name'],
                catalogue_version=data['catalogue_version'],
                is_cat_active=bool(int(data['is_cat_active'])),
                catalogue_start=data['catalogue_start'],
                catalogue_end=data['catalogue_end']
            )
            service.update_catalogue_by_id(catalogue_id, updated)
            logging.info(f'User "{session["username"]}" updated catalogue ID {catalogue_id} via Swagger.')
            return updated.to_dict()
        except CatalogueNotFoundError:
            logging.warning(f'User "{session["username"]}" tried to update non-existent catalogue ID {catalogue_id} via Swagger.')
            catalogue_ns.abort(404, "Catalogue with the specified ID does not exist.")
        except (InvalidCatalogueInputError, ValueError) as e:
            logging.warning(f'Invalid update input from user "{session["username"]}" for ID {catalogue_id} via Swagger: {e}')
            catalogue_ns.abort(400, "Invalid input: field types are incorrect or required fields are missing.")
        except Exception as e:
            logging.error(f'Error updating catalogue ID {catalogue_id} by user "{session["username"]}" via Swagger: {e}', exc_info=True)
            catalogue_ns.abort(500, "Unexpected error occurred. Please try again later.")
    
    @catalogue_ns.doc('delete_catalogue')
    def delete(self, catalogue_id):
        """Delete a catalogue"""
        check_auth()
        try:
            service.delete_catalogue_by_id(catalogue_id)
            logging.info(f'User "{session["username"]}" deleted catalogue ID {catalogue_id} via Swagger.')
            return '', 204
        except CatalogueNotFoundError:
            logging.warning(f'User "{session["username"]}" tried to delete non-existent catalogue ID {catalogue_id} via Swagger.')
            catalogue_ns.abort(404, "Catalogue with the specified ID does not exist.")
        except Exception as e:
            logging.error(f'Error deleting catalogue ID {catalogue_id} by user "{session["username"]}" via Swagger: {e}', exc_info=True)
            catalogue_ns.abort(500, "Unexpected error occurred. Please try again later.")

# ✅ Authentication endpoints below the catalogue classes
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate and start a session"""
        data = request.json
        username = data.get('username')
        password = data.get('password')
        try:
            if auth_service.authenticate(username, password):
                session['username'] = username
                logging.info(f'User "{username}" logged in via Swagger.')
                return {'message': 'Login successful'}, 200
            else:
                logging.warning(f'Failed login via Swagger for user "{username}".')
                return {'error': 'Invalid credentials'}, 401
        except InvalidCredentialsError:
            return {'error': 'Invalid credentials'}, 401
        except Exception as e:
            logging.error(f'Error during login: {e}', exc_info=True)
            return {'error': 'Unexpected error occurred.'}, 500

@auth_ns.route('/logout')
class Logout(Resource):
    def post(self):
        """Logout and clear session"""
        username = session.get('username')
        session.pop('username', None)
        logging.info(f'User "{username}" logged out via Swagger.')
        return {'message': 'Logout successful'}, 200
