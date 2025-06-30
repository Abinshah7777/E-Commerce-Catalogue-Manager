from flask import Flask, request, jsonify, render_template  # <-- added render_template
from service.catalogue_service import CatalogueService
from dto.catalogue_dto import Catalogue
from exceptions.exceptions import CatalogueNotFoundError, InvalidCatalogueInputError

app = Flask(__name__)
service = CatalogueService()

# ✅ Serve index.html at root path
@app.route('/')
def index():
    return render_template('index.html')

# Add these new routes to your app.py file

@app.route('/create')
def create_form():
    """Serves the form for creating a new catalogue."""
    return render_template('form.html', action='Create', catalogue=None)

# Find this function in your app.py

@app.route('/update/<int:id>')
def update_form(id):
    """Serves the form pre-filled with data for updating an existing catalogue."""
    try:
        catalogue_object = service.get_catalogue_by_id(id)
        catalogue_dict = catalogue_object.to_dict()
        
        return render_template('form.html', action='Update', catalogue=catalogue_dict)
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404
@app.route('/api/catalogues', methods=['GET'])
def get_all_catalogues():
    catalogues = service.get_all_catalogues()
    return jsonify([c.to_dict() for c in catalogues]), 200

@app.route('/api/catalogues/<int:id>', methods=['GET'])
def get_catalogue(id):
    try:
        catalogue = service.get_catalogue_by_id(id)
        return jsonify(catalogue.to_dict()), 200
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    

# Add this new route to your app.py file

@app.route('/view/<int:id>')
def view_catalogue(id):
    """Serves a read-only page showing the details of a single catalogue."""
    try:
        # Get the catalogue object from the service
        catalogue_object = service.get_catalogue_by_id(id)

        # Convert it to a dictionary to pass to the template
        catalogue_dict = catalogue_object.to_dict()

        return render_template('view.html', catalogue=catalogue_dict)
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/catalogues', methods=['POST'])
def create_catalogue():
    try:
        data = request.json
        catalogue = Catalogue(
            catalogue_id=int(data['catalogue_id']),
            catalogue_name=data['catalogue_name'],
            catalogue_version=data['catalogue_version'],
            is_cat_active=bool(int(data['is_cat_active'])),
            catalogue_start=data['catalogue_start'],
            catalogue_end=data['catalogue_end']
        )
        service.create_catalogue(catalogue)
        return jsonify({'message': 'Catalogue created successfully'}), 201
    except (InvalidCatalogueInputError, ValueError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/catalogues/<int:id>', methods=['PUT'])
def update_catalogue(id):
    try:
        data = request.json
        updated = Catalogue(
            catalogue_id=id,
            catalogue_name=data['catalogue_name'],
            catalogue_version=data['catalogue_version'],
            is_cat_active=bool(int(data['is_cat_active'])),
            catalogue_start=data['catalogue_start'],
            catalogue_end=data['catalogue_end']
        )
        service.update_catalogue_by_id(id, updated)
        return jsonify({'message': f'Catalogue {id} updated successfully'}), 200
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except (InvalidCatalogueInputError, ValueError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/catalogues/<int:id>', methods=['DELETE'])
def delete_catalogue(id):
    try:
        service.delete_catalogue_by_id(id)
        return jsonify({'message': f'Catalogue {id} deleted successfully'}), 200
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
