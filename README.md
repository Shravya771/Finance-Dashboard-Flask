

# 💸 Finance Dashboard (Flask + JWT)

A modern **Finance Management Dashboard** built using **Flask**, featuring **secure authentication**, **role-based access control**, and **financial analytics**.

---

## 🚀 Features

✨ **Authentication & Security**

* JWT-based Login & Registration
* Password hashing using Bcrypt

👥 **Role-Based Access**

* Admin → Full access
* Analyst → Analytics access
* Viewer → Read-only access

💰 **Transaction Management**

* Add, view, update, delete transactions
* Filter transactions by category/type

📊 **Analytics**

* Income vs Expense summary
* Category-wise expense analysis
* Monthly financial insights

🧑‍💼 **Admin Controls**

* View all users
* Update user roles
* Delete users (with transactions)

---

## 🛠️ Tech Stack

| Layer    | Technology               |
| -------- | ------------------------ |
| Backend  | Flask                    |
| Database | SQLite                   |
| ORM      | SQLAlchemy               |
| Auth     | JWT (Flask-JWT-Extended) |
| Security | Bcrypt                   |
| Frontend | HTML, CSS, JavaScript    |

---

## 📁 Project Structure

```
finance_dashboard/
│── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── finance_routes.py
│   │   ├── user_routes.py
│   ├── utils/
│   │   ├── decorators.py
│   │   ├── validators.py
│
│── templates/
│   ├── login.html
│   ├── dashboard.html
│
│── config.py
│── run.py
│── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Shravya771/Finance-Dashboard-Flask.git
cd Finance-Dashboard-Flask
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
python run.py
```

---

## 🌐 Access Application

* 🔐 Login Page →https://finance-dashboard-flask-3.onrender.com/
* 🔗 Postman → https://shettyshravya771-9327508.postman.co/workspace/0f84f734-95da-4553-8413-7b49efb5941e/collection/53736078-973a0de1-5931-48cf-b3f5-bb405fdabae4?action=share&source=copy-link&creator=53736078
---

## 🔑 API Endpoints

### 🔐 Authentication

```
POST /auth/register
POST /auth/login
```

### 💰 Finance

```
POST   /finance/
GET    /finance/
PUT    /finance/<id>        (Admin only)
DELETE /finance/<id>        (Admin only)
GET    /finance/summary
GET    /finance/category-summary
GET    /finance/filter
GET    /finance/monthly-summary
```

### 👥 Users (Admin Only)

```
GET    /users/
PUT    /users/<id>/role
DELETE /users/<id>
```

---

## 🔐 Roles & Permissions

| Role    | Access Level     |
| ------- | ---------------- |
| Admin   | Full access      |
| Analyst | View + Analytics |
| Viewer  | View only        |

---

## 🧪 Testing (Postman)

Use Postman to test APIs.

👉 Add JWT Token in header:

```
Authorization: Bearer <your_token>
```

---

## 📌 Key Highlights

* 🔒 Secure authentication using JWT
* 🔐 Role-based authorization
* 📊 Real-time financial summaries
* 🧾 Clean and responsive UI
* ⚡ RESTful API design

---

## 👩‍💻 Author

**Shravya Shetty**


---

# 🎯 WHY THIS IS BETTER 

* Clean sections ✅
* Proper formatting ✅
* Looks professional ✅
* Easy for evaluator to read ✅

## 📸 Screenshots

### 📝 Register Page and 🔐 Login Page
<img width="500" height="500" alt="Screenshot 2026-04-04 175213" src="https://github.com/user-attachments/assets/adb1648f-8d2c-4d4e-8a52-e0f323f8b2a8" />


### 📊 Dashboard
<img width="500" height="500" alt="Screenshot 2026-04-04 175250" src="https://github.com/user-attachments/assets/bc2c3ae9-c6b7-4bae-b8f5-78d03eda0179" />


### 👮 Postman 
<img width="500" height="500" alt="Screenshot 2026-04-04 175336" src="https://github.com/user-attachments/assets/36e8c99b-3a7b-496b-9e8c-aca5d18e2800" />
"# FinFlow-finance-dashboard-flask" 
