# FastAPI + SQLModel + PostgreSQL Backend Guide
**Author — Aryan Pandey**

A practical backend guide demonstrating how to build **production-ready APIs** using **FastAPI**, **SQLModel**, and **PostgreSQL** with **Alembic migrations**.

This repository is designed for developers who want to understand how modern Python backends interact with relational databases using clean architecture and ORM concepts.

It begins with basic CRUD operations and gradually introduces intermediate and advanced backend concepts such as:

* ORM object lifecycle
* Database relationships
* Dependency injection
* Pagination
* Query loading strategies
* Database migrations

The goal is to provide a **hands-on reference project** that developers can study, extend, and reuse.

---

# Tech Stack

The backend is built using the following technologies:

* FastAPI — high-performance modern API framework
* SQLModel — ORM built on SQLAlchemy and Pydantic
* PostgreSQL — relational database
* SQLAlchemy — database toolkit used internally by SQLModel
* Alembic — database migration management

---

# Project Structure

The repository follows a modular backend structure.

```
project/
│
├── core/
│   └── database.py        # database engine and session configuration
│
├── models/
│   ├── base.py            # shared mixins (timestamps etc.)
│   ├── users.py           # user database model
│   └── orders.py          # order database model
│
├── schemas/
│   ├── users.py           # request/response schemas
│   └── orders.py
│
├── crud/
│   ├── users.py           # CRUD logic for users
│   └── orders.py
│
├── routes/
│   ├── users.py           # API endpoints
│   └── orders.py
│
├── migrations/            # Alembic database migrations
│   ├── versions/
│   └── env.py
│
├── docs/                  # detailed learning documentation
│
├── main.py                # FastAPI application entrypoint
│
├── alembic.ini
├── requirements.txt
└── README.md
```

This structure separates responsibilities clearly:

**Models →** database schema
**Schemas →** API validation
**CRUD →** database logic
**Routes →** API endpoints
**Migrations →** database schema history

---

# Architecture Overview

Typical request flow in this project:

```
Client Request
      │
      ▼
FastAPI Router
      │
      ▼
Request Schema Validation
      │
      ▼
CRUD Layer
      │
      ▼
SQLModel ORM
      │
      ▼
PostgreSQL Database
```

This layered architecture keeps the code **clean, testable, and scalable**.

---

# Getting Started

## 1. Clone the repository

```
git clone https://github.com/ltd-ARYAN-pvt/fastapi-sqlmodel-postgresql.git
cd fastapi-sqlmodel-postgresql
```

---

## 2. Create virtual environment

```
python -m venv venv
```

Activate it:

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file.

Example:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sqlmodel_demo
```

---

## 5. Create PostgreSQL Database

Alembic manages **schema**, but the database must exist first.

Create the database manually:

```
createdb sqlmodel_demo
```

Or inside PostgreSQL:

```
CREATE DATABASE sqlmodel_demo;
```

---

## 6. Run Database Migrations

Apply migrations to create tables:

```
alembic upgrade head
```

This will create:

* `users` table
* `orders` table
* `alembic_version` table

---

## 7. Start the Application

```
fastapi dev main.py
```

Server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

You can test API endpoints directly from the browser.

---

# Example API Endpoints

Users

```
POST   /users
GET    /users
GET    /users/{id}
PUT    /users/{id}
DELETE /users/{id}
```

Orders

```
POST   /orders
GET    /orders
GET    /orders/{id}
```

Pagination example

```
GET /users?offset=0&limit=10
```

---

# Database Migrations Workflow

This project uses **Alembic** to manage database schema changes.

Typical development workflow:

1️⃣ Modify SQLModel models
2️⃣ Generate migration

```
alembic revision --autogenerate -m "message"
```

3️⃣ Apply migration

```
alembic upgrade head
```

This ensures database schema stays synchronized across environments.

---

# Learning Documentation

Detailed explanations are provided in the `docs` folder.

```
docs/
│
├── 01_sqlmodel_basics.md
├── 02_data_operations.md
├── 03_dependency_injection.md
├── 04_query_loading_strategies.md
├── 05_migrations_and_alembic.md
```

Topics covered include:

* ORM fundamentals
* SQLModel architecture
* CRUD operations
* Relationships
* Pagination
* Dependency injection
* Lazy vs eager loading
* N+1 query problem
* Database migrations with Alembic

These documents make the repository a **mini backend learning guide**.

---

# Example Request

Create a user

```
POST /users
```

Request body

```
{
  "name": "Rahul Sharma",
  "email": "rahul@test.com",
  "age": 22
}
```

Response

```
{
  "id": 1,
  "name": "Rahul Sharma",
  "email": "rahul@test.com",
  "age": 22
}
```

---

# Future Improvements

Possible extensions for this repository:

* Authentication (JWT)
* Role based access control
* Async database operations
* Redis caching
* Background tasks
* Docker deployment
* CI/CD pipelines

---

# Who This Repository Is For

This project is useful for:

* Backend developers learning FastAPI
* Developers exploring SQLModel ORM
* Students learning database-backed APIs
* Anyone wanting a clean backend architecture example

---

# Contributing

Contributions are welcome.

If you find issues or want to improve documentation, feel free to open a pull request.

---

# License

This project is open-source and available under the MIT License.
