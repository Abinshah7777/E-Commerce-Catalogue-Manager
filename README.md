# E-Commerce Catalogue Manager

This is a simple web application for managing e-commerce catalogues. It allows users to perform standard CRUD (Create, Read, Update, Delete) operations through a user-friendly web interface using Flask and JavaScript (Fetch API).

## Features

- **Create Catalogue:** Add new catalogue entries with details like name, start date, end date, and active status.
- **View All Catalogues:** Display a list of all existing catalogues in a tabular format.
- **View Catalogue by ID:** Retrieve and display details for a specific catalogue using its unique ID.
- **Update Catalogue by ID:** Modify the details of an existing catalogue.
- **Delete Catalogue by ID:** Remove a catalogue entry from the system.

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API for asynchronous communication)
- **Architecture:** Modular OOP design with service layers, DTOs, and custom exceptions
- **Data Handling:** In-memory storage (no database)
- **Version Control:** Git & GitHub

## Project Structure

E-Commerce-Catalogue-Manager/
├── app.py # Main Flask application
├── templates/
│ └── index.html # Frontend HTML interface
├── static/
│ └── js/
│ └── main.js # JavaScript for Fetch API interaction
├── dto/
│ └── catalogue_dto.py # Catalogue class definition (DTO)
├── service/
│ └── catalogue_service.py # Business logic for catalogue management
├── exceptions/
│ └── exceptions.py # Custom error classes
├── util/
│ └── validators.py # Input validation functions
├── requirements.txt # Python package requirements
└── README.md # Project documentation


## Setup Instructions

To run this project locally on your system:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Abinshah7777/E-Commerce-Catalogue-Manager.git
    cd E-Commerce-Catalogue-Manager
    ```

2. **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask Application:**
    ```bash
    python app.py
    ```
    The application will typically run on:  
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage

1. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
2. Use the buttons provided to:
    - Create a new catalogue
    - View a specific catalogue using its ID
    - Update or delete a catalogue by ID
    - View all catalogues at once
3. The interface will display all results directly on the page, and success or error messages will appear at the top.

## Notes

- This version does **not** include category support or database integration.
- All data is stored in memory during runtime — restarting the app will reset all data.
- Input validation is handled using utility functions and custom exceptions for cleaner error handling.

## Author

**Abinshah PM**  
GitHub: [Abinshah7777](https://github.com/Abinshah7777)