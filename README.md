# Xtern – Internship Management System

Xtern is a web-based internship management system designed to streamline the process of managing internships, applicants, companies, and applications. The system provides separate dashboards for applicants, companies, and administrators, ensuring smooth interaction and data management.

## 🚀 Features

- **Applicant Module**
  - Registration, login, and profile management
  - Add educational qualifications
  - Search and apply for internships
  - Track application status

- **Company Module**
  - Registration (admin approval required)
  - Post internships
  - View and manage applications
  - Approve or reject applicants
  - Analytics dashboard with charts

- **Admin Module**
  - Approve or reject company registrations
  - Manage users and data

- **General**
  - Resume uploads (PDF)
  - Skill matching between applicants and internships
  - Secure authentication and authorization

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **Charting**: Chart.js

## ⚙️ Setup Instructions

1️⃣ **Clone the repository**
```bash
git clone https://github.com/your-username/xtern.git
cd xtern
```

2️⃣ Create a virtual environment
```bash
python -m venv venv
# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Set up the database
Import the provided SQL dump into your MySQL server.
Update the database connection settings in your Flask app (e.g., config.py).

5️⃣ Run the application
```bash
flask run
```


📂 Project Structure
xtern/
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── app.py                # Main Flask application
├── models.py             # Database models (if separated)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


✨ Future Work
Filter and sort internships by location, stipend, etc.
Add pagination to lists
Improve mobile responsiveness


🙌 Acknowledgments
This project was developed as part of my academic coursework to practice full-stack development using Flask and MySQL.
