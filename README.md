# 🚀 SmartAttendance — Face Recognition Attendance System

A modern, AI-powered attendance management system that automates student attendance using real-time face recognition. Built with a scalable full-stack architecture using Flask (backend) and React (frontend).


## 📌 Overview

SmartAttendance eliminates manual attendance tracking by leveraging computer vision and machine learning. It provides secure, fast, and accurate attendance recording with advanced analytics and role-based access control.


## 🛠 Tech Stack

### Frontend

* React 18 + TypeScript
* Vite
* Tailwind CSS

### Backend

* Python (Flask)
* Flask-JWT-Extended

### Database

* MySQL 8.0

### AI / Machine Learning

* FaceNet
* InsightFace
* OpenCV
* Scikit-learn


## ✨ Key Features

* 🎯 Real-time face recognition for attendance
* 🔐 Role-based access control (Admin, Instructor, Student)
* 🕒 Session management (Lab/Theory, Morning/Afternoon)
* 📊 Analytics dashboard with charts and reports
* 📁 Export data to CSV/Excel
* 📧 Email-based password reset
* 🛡 Protection against SQL Injection & XSS


## 📂 Project Structure

```
smartattendance/
├── backend/
│   ├── blueprints/
│   ├── db/
│   ├── middleware/
│   ├── recognizer/
│   ├── utils/
│   ├── app.py
│   ├── config.py
│   └── seed_db.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── lib/
│   └── package.json
│
└── setup_mysql_database.sql
```


## ⚙️ Setup & Installation

### 🔧 Prerequisites

* Python 3.10+
* Node.js 18+
* MySQL 8.0


### 1️⃣ Clone Repository

```bash
git clone https://github.com/bacha67/Smart-Attendance-updated.git
cd Smart-Attendance-updated
```


### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file inside `backend/`:

```
SECRET_KEY=your-secret-key
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=smart_attendance
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password

JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=168
```


### 3️⃣ Database Setup

```bash
mysql -u root -p < setup_mysql_database.sql
cd backend
python seed_db.py
```


### 4️⃣ Frontend Setup

```bash
cd frontend
npm install
```


## ▶️ Running the Application

### Start Backend

```bash
cd backend
python app.py
```

### Start Frontend

```bash
cd frontend
npm run dev
```

### Access URLs

* Frontend: http://localhost:5173
* Backend: http://localhost:5000

---

## 🔑 Demo Credentials

| Role       | Username     | Password |
| ---------- | ------------ | -------- |
| Admin      | admin        | admin123 |
| Instructor | dr.bekele    | inst123  |
| Instructor | dr.almaz     | inst123  |
| Instructor | prof.hailu   | inst123  |
| Instructor | dr.tigist    | inst123  |
| Instructor | dr.yonas     | inst123  |
| Student    | stu.nabila   | stud123  |
| Student    | stu.bekam    | stud123  |
| Student    | stu.yohannis | stud123  |

> Students follow: `stu.<firstname>` (password: `stud123`)


## 🔌 API Endpoints

| Method | Endpoint                      | Description        |
| ------ | ----------------------------- | ------------------ |
| POST   | /api/auth/login               | Login              |
| GET    | /api/auth/me                  | Current user       |
| POST   | /api/attendance/start-session | Start session      |
| POST   | /api/attendance/recognize     | Face recognition   |
| POST   | /api/attendance/end-session   | End session        |
| GET    | /api/instructor/records       | Attendance records |
| GET    | /api/admin/analytics/*        | Analytics          |
| GET    | /health                       | Health check       |

---

## 📜 License

MIT License
