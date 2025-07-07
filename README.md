# 🛍️ E-Commerce Catalogue Manager

A full-stack web application to manage e-commerce catalogues with secure login, MySQL database integration, and dynamic front-end interaction using JavaScript's Fetch API.

---

## 🚀 Features

- 🔐 User Authentication (Login + Logout)
- 🆕 Create a new catalogue
- 📄 View all catalogues
- 🔍 Search by ID or Name (live filtering)
- 🧾 View by ID using the search bar
- ✏️ Update catalogue (inline)
- ❌ Delete catalogue (inline)
- ⚙️ Clean modular structure (DTOs, Services, Validators, Exceptions)

---

## 🛠️ Technologies Used

| Layer        | Tech Stack                         |
|--------------|------------------------------------|
| Backend      | Flask (Python)                     |
| Frontend     | HTML5, CSS3, JavaScript (Fetch API)|
| Database     | MySQL                              |
| Architecture | Modular OOP + Service Layer        |
| Other        | Session-based auth, Custom logging |

# 📁 Project Structure
```
Catalogue_Manager/
├── app.py                    # Main Flask app entry point
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation

├── api/        
    ├── __init__.py
│   └── catalogue_routtes.py      # JSON API routes

├── config/
│   └── config.ini            # MySQL and app configurations

├── dto/
│   ├── __init__.py
│   └── catalogue_dto.py      # DTO for Catalogue objects

├── exceptions/
│   ├── __init__.py
│   └── exceptions.py         # Custom exception classes

├── service/
│   ├── __init__.py
│   ├── authentication_service.py
│   └── catalogue_service.py  # Business logic layer

├── static/
│   ├── css/
│   │   └── style.css         # Frontend styles
│   └── js/
│       └── main.js           # JavaScript (Fetch API logic)

├── templates/
│   ├── index.html            # Main UI
│   └── login.html            # Login page

├── util/
│   ├── __init__.py
│   ├── db_get_connection.py  # MySQL connection helper
│   └── validators.py         # Input validation

├── logs/
│   └── app.log               # Application logs

├── tests/
    ├── __init__.py
    └── test_catalogue.py     # Unit tests
```



# 🧑‍💻 Setup Instructions
### 1️⃣ Clone the Repository
git clone https://github.com/Abinshah7777/E-Commerce-Catalogue-Manager.git


### 2️⃣ Create a Virtual Environment (Optional but Recommended)

python -m venv venv

### Activate it:
### On Windows

venv\Scripts\activate

### On macOS/Linux

source venv/bin/activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt
### 4️⃣ Set Up MySQL Database

Make sure MySQL is installed and running on your system.

Create a new database 

Update the DB connection settings in app.py or your config module

Run any initial SQL if needed (your app may auto-create tables)

Example SQL:

CREATE DATABASE catalogue_db;

### 5️⃣ Run the Flask App

python app.py
Then open your browser and go to:

http://127.0.0.1:5000

# 🔐 Login Credentials

Use the following credentials to log in:

Username: admin

Password: admin123

# 📘 API Documentation
This project includes interactive API documentation using Swagger UI via Flask-RestX.

### 🔗 Access the API docs here:
```

http://192.168.1.4:5000/api/docs

```
### or if you're running locally:
```
http://localhost:5000/api/docs

```

This Swagger UI interface allows you to explore and test all /api/catalogues endpoints.



# 🧪 Usage

Once logged in:

➕ Add a new catalogue

🔍 Search by ID or Name using the search bar

✏️ Update a catalogue using the inline update button

🗑️ Delete a catalogue using the inline delete button

📜 View all catalogues directly on the homepage

All actions are done without reloading the page using JavaScript Fetch API.

# 📝 Notes

All data is managed through JSON APIs

The frontend dynamically updates using JavaScript

Application logs are saved to logs/app.log

Input validation is handled in util/validators.py

Graceful error handling is managed using custom exceptions

# 👨‍💻 Author

Abinshah PM

GitHub: @Abinshah7777
