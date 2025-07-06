
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from service.catalogue_service import CatalogueService
from dto.catalogue_dto import Catalogue
from service.authentication_service import AuthenticationService
from exceptions.exceptions import CatalogueNotFoundError, InvalidCatalogueInputError, InvalidCredentialsError, CatalogueAlreadyExistsError
import os


# ✅ Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# ------------------- Logging Configuration -------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
# -------------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'your_secret_key'

service = CatalogueService()
auth_service = AuthenticationService()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/api/catalogues', methods=['GET'])
def get_all_catalogues():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        logging.info(f'User "{session["username"]}" fetched all catalogues.')
        catalogues = service.get_all_catalogues()
        return success_response("Catalogues fetched successfully", [c.to_dict() for c in catalogues])
    except Exception as e:
        logging.error(f'Error fetching catalogues for user "{session["username"]}": {e}', exc_info=True)
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues/<int:id>', methods=['GET'])
def get_catalogue(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        catalogue = service.get_catalogue_by_id(id)
        logging.info(f'User "{session["username"]}" fetched catalogue with ID {id}.')
        return success_response("Catalogue fetched successfully", catalogue.to_dict())
    except CatalogueNotFoundError:
        logging.warning(f'User "{session["username"]}" tried to fetch non-existent catalogue ID {id}.')
        return error_response("Catalogue with the specified ID does not exist.", 404)
    except Exception as e:
        logging.error(f'Error fetching catalogue ID {id} for user "{session["username"]}": {e}', exc_info=True)
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues', methods=['POST'])
def create_catalogue():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        data = request.json
        if not all(key in data for key in ['catalogue_id', 'catalogue_name', 'catalogue_version', 'is_cat_active', 'catalogue_start', 'catalogue_end']):
            raise InvalidCatalogueInputError("Invalid input: one or more required fields are missing or empty.")

        #  Date validation
        start_date = datetime.strptime(data['catalogue_start'], '%Y-%m-%d')
        end_date = datetime.strptime(data['catalogue_end'], '%Y-%m-%d')
        today = datetime.today().date()

        if start_date.date() <= today or end_date.date() <= today:
            logging.warning(f'User "{session["username"]}" attempted to create a catalogue with past or today\'s date.')
            return jsonify({
                "success": False,
                "error": "Catalogue start and end dates must be in the future."
            }), 400

        if end_date <= start_date:
            logging.warning(f'User "{session["username"]}" entered end date before start date.')
            return jsonify({
                "success": False,
                "error": "Catalogue end date must be after the start date."
            }), 400

        catalogue = Catalogue(
            catalogue_id=int(data['catalogue_id']),
            catalogue_name=data['catalogue_name'],
            catalogue_version=data['catalogue_version'],
            is_cat_active=bool(int(data['is_cat_active'])),
            catalogue_start=data['catalogue_start'],
            catalogue_end=data['catalogue_end']
        )

        service.create_catalogue(catalogue)
        logging.info(f'User "{session["username"]}" created catalogue with ID {catalogue.catalogue_id}.')

        return jsonify({
            "success": True,
            "message": f"Catalogue created successfully with ID {catalogue.catalogue_id}",
            "data": {
                "catalogue_id": catalogue.catalogue_id
            }
        }), 201

    except CatalogueAlreadyExistsError as e:
        logging.warning(f'User "{session["username"]}" attempted to create a duplicate catalogue ID {data.get("catalogue_id")}.')
        return jsonify({
            "success": False,
            "error": str(e)
        }), 409

    except (InvalidCatalogueInputError, ValueError) as e:
        logging.warning(f'Invalid input from user "{session["username"]}": {e}')
        return jsonify({
            "success": False,
            "error": "Invalid input: field types are incorrect or required fields are missing."
        }), 400

    except Exception as e:
        logging.error(f'Unexpected error during catalogue creation by user "{session["username"]}": {e}', exc_info=True)
        return jsonify({
            "success": False,
            "error": "Unexpected error occurred. Please try again later."
        }), 500

@app.route('/api/catalogues/<int:id>', methods=['PUT'])
def update_catalogue(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        data = request.json
        if not all(key in data for key in ['catalogue_name', 'catalogue_version', 'is_cat_active', 'catalogue_start', 'catalogue_end']):
            raise InvalidCatalogueInputError("Invalid input: one or more required fields are missing or empty.")

        #  Date validation
        start_date = datetime.strptime(data['catalogue_start'], '%Y-%m-%d')
        end_date = datetime.strptime(data['catalogue_end'], '%Y-%m-%d')
        today = datetime.today().date()

        if start_date.date() <= today or end_date.date() <= today:
            logging.warning(f'User "{session["username"]}" attempted to update catalogue ID {id} with past or today\'s date.')
            return error_response("Catalogue start and end dates must be in the future.", 400)

        if end_date <= start_date:
            logging.warning(f'User "{session["username"]}" attempted to set end date before start date for catalogue ID {id}.')
            return error_response("Catalogue end date must be after the start date.", 400)

        updated = Catalogue(
            catalogue_id=id,
            catalogue_name=data['catalogue_name'],
            catalogue_version=data['catalogue_version'],
            is_cat_active=bool(int(data['is_cat_active'])),
            catalogue_start=data['catalogue_start'],
            catalogue_end=data['catalogue_end']
        )
        service.update_catalogue_by_id(id, updated)
        logging.info(f'User "{session["username"]}" updated catalogue ID {id}.')
        return success_response(f"Catalogue {id} updated successfully")
    except CatalogueNotFoundError:
        logging.warning(f'User "{session["username"]}" tried to update non-existent catalogue ID {id}.')
        return error_response("Catalogue with the specified ID does not exist.", 404)
    except (InvalidCatalogueInputError, ValueError) as e:
        logging.warning(f'Invalid update input from user "{session["username"]}" for ID {id}: {e}')
        return error_response("Invalid input: field types are incorrect or required fields are missing.", 400)
    except Exception as e:
        logging.error(f'Error updating catalogue ID {id} by user "{session["username"]}": {e}', exc_info=True)
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues/<int:id>', methods=['DELETE'])
def delete_catalogue(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        service.delete_catalogue_by_id(id)
        logging.info(f'User "{session["username"]}" deleted catalogue ID {id}.')
        return success_response(f"Catalogue {id} deleted successfully")
    except CatalogueNotFoundError:
        logging.warning(f'User "{session["username"]}" tried to delete non-existent catalogue ID {id}.')
        return error_response("Catalogue with the specified ID does not exist.", 404)
    except Exception as e:
        logging.error(f'Error deleting catalogue ID {id} by user "{session["username"]}": {e}', exc_info=True)
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            if auth_service.authenticate(username, password):
                session['username'] = username
                logging.info(f'User "{username}" logged in successfully.')
                return redirect(url_for('index'))
            else:
                logging.warning(f'Failed login attempt for username: "{username}".')
                return render_template('login.html', error="Invalid username or password.")
        except Exception as e:
            logging.error(f'Login error for user "{username}": {e}', exc_info=True)
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.get('username')
    session.pop('username', None)
    logging.info(f'User "{username}" logged out.')
    return redirect(url_for('login'))

# Standardized Response Format
def success_response(message, data=None):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), 200

def error_response(error_message, status_code=400):
    return jsonify({
        "success": False,
        "error": error_message
    }), status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
