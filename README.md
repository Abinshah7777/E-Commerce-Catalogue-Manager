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

📁 Project Structure
php
Copy
Edit
Catalogue_Manager/
├── app.py                    # Main Flask app
├── dto/
│   └── catalogue_dto.py      # DTO for Catalogue
├── exceptions/
│   ├── __init__.py
│   └── exceptions.py         # Custom exception classes
├── logs/
│   └── app.log               # Application logs
├── service/
│   ├── __init__.py
│   ├── authentication_service.py
│   └── catalogue_service.py  # Business logic layer
├── static/
│   ├── css/
│   │   └── style.css         # Stylesheet for the frontend
│   └── js/
│       └── main.js           # JavaScript (Fetch API logic)
├── templates/
│   ├── index.html            # Main frontend page
│   └── login.html            # Login page
├── util/
│   └── validators.py         # Input validation helpers
├── tests/                    # (Optional) Unit tests
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore file
└── README.md                 # Project documentation

# 🧑‍💻 Setup Instructions
### 1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/Abinshah7777/E-Commerce-Catalogue-Manager.git
cd E-Commerce-Catalogue-Manager
### 2️⃣ Create a Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
Activate it:

''' bash
Copy
Edit
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
### 3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
### 4️⃣ Set Up MySQL Database
Make sure MySQL is installed and running on your system.

Create a new database (e.g., catalogue_db)

Update the DB connection settings in app.py or your config module

Run any initial SQL if needed (your app may auto-create tables)

Example SQL:

sql
Copy
Edit
CREATE DATABASE catalogue_db;
Example DB Config in app.py:

python
Copy
Edit
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'yourpassword'
mysql_db = 'catalogue_db'
### 5️⃣ Run the Flask App
bash
Copy
Edit
python app.py
Then open your browser and go to:
http://127.0.0.1:5000

# 🔐 Login Credentials
Use the following credentials to log in:

Username: admin

Password: admin123

These can be changed in the database or authentication service code.

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
