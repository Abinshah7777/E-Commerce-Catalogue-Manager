from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from service.catalogue_service import CatalogueService
from dto.catalogue_dto import Catalogue
from service.authentication_service import AuthenticationService
from exceptions.exceptions import CatalogueNotFoundError, InvalidCatalogueInputError, InvalidCredentialsError

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
        catalogues = service.get_all_catalogues()
        return success_response("Catalogues fetched successfully", [c.to_dict() for c in catalogues])
    except Exception:
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues/<int:id>', methods=['GET'])
def get_catalogue(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        catalogue = service.get_catalogue_by_id(id)
        return success_response("Catalogue fetched successfully", catalogue.to_dict())
    except CatalogueNotFoundError:
        return error_response("Catalogue with the specified ID does not exist.", 404)
    except Exception:
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues', methods=['POST'])
def create_catalogue():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        data = request.json
        if not all(key in data for key in ['catalogue_id', 'catalogue_name', 'catalogue_version', 'is_cat_active', 'catalogue_start', 'catalogue_end']):
            raise InvalidCatalogueInputError("Invalid input: one or more required fields are missing or empty.")
        catalogue = Catalogue(
            catalogue_id=int(data['catalogue_id']),
            catalogue_name=data['catalogue_name'],
            catalogue_version=data['catalogue_version'],
            is_cat_active=bool(int(data['is_cat_active'])),
            catalogue_start=data['catalogue_start'],
            catalogue_end=data['catalogue_end']
        )
        service.create_catalogue(catalogue)
        return success_response("Catalogue created successfully"), 201
    except (InvalidCatalogueInputError, ValueError):
        return error_response("Invalid input: field types are incorrect or required fields are missing.", 400)
    except Exception:
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues/<int:id>', methods=['PUT'])
def update_catalogue(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        data = request.json
        if not all(key in data for key in ['catalogue_name', 'catalogue_version', 'is_cat_active', 'catalogue_start', 'catalogue_end']):
            raise InvalidCatalogueInputError("Invalid input: one or more required fields are missing or empty.")
        updated = Catalogue(
            catalogue_id=id,
            catalogue_name=data['catalogue_name'],
            catalogue_version=data['catalogue_version'],
            is_cat_active=bool(int(data['is_cat_active'])),
            catalogue_start=data['catalogue_start'],
            catalogue_end=data['catalogue_end']
        )
        service.update_catalogue_by_id(id, updated)
        return success_response(f"Catalogue {id} updated successfully")
    except CatalogueNotFoundError:
        return error_response("Catalogue with the specified ID does not exist.", 404)
    except (InvalidCatalogueInputError, ValueError):
        return error_response("Invalid input: field types are incorrect or required fields are missing.", 400)
    except Exception:
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/api/catalogues/<int:id>', methods=['DELETE'])
def delete_catalogue(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        service.delete_catalogue_by_id(id)
        return success_response(f"Catalogue {id} deleted successfully")
    except CatalogueNotFoundError:
        return error_response("Catalogue with the specified ID does not exist.", 404)
    except Exception:
        return error_response("Unexpected error occurred. Please try again later.", 500)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            if auth_service.authenticate(username, password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                raise InvalidCredentialsError("Invalid username or password.")
        except InvalidCredentialsError as e:
            return render_template('login.html', error=str(e))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
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
