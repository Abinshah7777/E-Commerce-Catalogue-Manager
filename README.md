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

🧑‍💻 Setup Instructions
1️⃣ Clone the repository
bash
Copy
Edit
git clone https://github.com/Abinshah7777/E-Commerce-Catalogue-Manager.git
cd E-Commerce-Catalogue-Manager
2️⃣ Create virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
3️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set up MySQL Database
💡 Make sure MySQL is installed and running on your system.

Create a new database (e.g., catalogue_db)

Update DB connection settings inside your app.py or config file

Run any SQL script to initialize tables, if needed (or your app auto-creates them)

Example MySQL command:
sql
Copy
Edit
CREATE DATABASE catalogue_db;
Configure your MySQL credentials inside your code:
python
Copy
Edit
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'yourpassword'
mysql_db = 'catalogue_db'
5️⃣ Run the Flask app
bash
Copy
Edit
python app.py
The app should now be live at:
📡 http://127.0.0.1:5000

🔐 Login Credentials
Use the following credentials to log in:

Username: admin

Password: admin123

These can be updated inside the authentication service or in your database.

🧪 Usage
Open your browser and go to: http://127.0.0.1:5000

Log in using the provided credentials

You can now:

➕ Add a new catalogue

🔍 Search by catalogue ID or Name

✏️ Update catalogues using inline buttons

🗑️ Delete catalogues using inline buttons

📜 View all catalogues in one view

All interactions are dynamic and happen via JavaScript Fetch API (no page reloads).

📝 Notes
All data exchange happens via JSON APIs

No page reloads: frontend updates dynamically

Logs are stored in logs/app.log

Input validation is handled through util/validators.py

Custom exceptions ensure clear error handling and cleaner code

👨‍💻 Author
Abinshah PM
GitHub: @Abinshah7777
