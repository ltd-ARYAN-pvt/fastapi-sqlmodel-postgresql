# SQLModel Basics, ORM Concepts, and Database Connection

## Introduction

This document introduces the core concepts required to work with **SQLModel**, including:

* What an ORM is
* How SQLModel works internally
* How database connections are established
* The lifecycle of database sessions

This forms the foundation for building backend systems using **FastAPI**, **SQLModel**, and **PostgreSQL**.

---

# 1. What is an ORM?

ORM stands for **Object Relational Mapper**.

It is a technique that allows developers to interact with relational databases using **programming language objects instead of writing raw SQL queries**.

## Without ORM

Example SQL query:

```sql
SELECT * FROM users WHERE id = 1;
```

You must manually write SQL and process database results.

## With ORM

Example using SQLModel:

```python
user = session.get(User, 1)
```

Here the ORM:

1. Converts the Python request into SQL
2. Sends the SQL to the database
3. Converts the result back into a Python object

---

# 2. Why ORMs Exist

ORMs help developers by providing:

### Abstraction

Developers interact with **Python objects** instead of writing SQL every time.

### Productivity

Less boilerplate code.

### Maintainability

Database logic stays organized within models.

### Database portability

Changing databases (e.g., SQLite → PostgreSQL) often requires minimal code changes.

---

# 3. What is SQLModel?

SQLModel is a Python library that combines the best features of:

* SQLAlchemy (database ORM)
* Pydantic (data validation)

It allows developers to define **database models and API schemas in a single unified structure**.

Example:

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
```

This single model can:

* Define database tables
* Validate API input
* Serialize API responses

---

# 4. How SQLModel Works Internally

SQLModel is built on top of **SQLAlchemy**.

Architecture:

```
Python Code
    ↓
SQLModel
    ↓
SQLAlchemy ORM
    ↓
Database Driver (psycopg2)
    ↓
PostgreSQL
```

Flow of execution:

1. Python objects are created
2. SQLModel converts them into SQLAlchemy models
3. SQLAlchemy generates SQL queries
4. Queries are sent to the database
5. Results are returned as Python objects

---

# 5. Connecting to the Database

To interact with the database, SQLModel uses a **database engine**.

Example:

```python
from sqlmodel import create_engine

DATABASE_URL = "postgresql://postgres:password@localhost:5432/sqlmodel_demo"

engine = create_engine(DATABASE_URL)
```

## What is an Engine?

The engine:

* Manages database connections
* Maintains a connection pool
* Sends SQL queries to the database

Think of the engine as a **communication bridge between Python and the database**.

---

# 6. Creating Database Sessions

A **Session** represents an interaction with the database.

Example:

```python
from sqlmodel import Session

with Session(engine) as session:
    users = session.exec(select(User)).all()
```

The session is responsible for:

* Querying the database
* Tracking changes to objects
* Committing transactions
* Rolling back errors

---

# 7. SQLModel Object Lifecycle

When working with ORM objects, they move through several states.

### Transient

Object exists only in Python.

```
user = User(name="Rahul", email="rahul@test.com")
```

Not yet stored in the database.

---

### Pending

Object has been added to the session.

```
session.add(user)
```

But not yet committed.

---

### Persistent

After committing:

```
session.commit()
```

The object now exists in the database.

---

### Detached

When the session is closed, the object becomes detached from the session.

---

# 8. Example Flow

Example user creation flow:

```python
user = User(name="Rahul", email="rahul@test.com")

session.add(user)

session.commit()

session.refresh(user)
```

Process:

1. User object created in Python
2. Object added to session
3. SQL INSERT query generated
4. Data stored in PostgreSQL
5. ORM returns the stored object

---

# Summary

In this document we covered:

* What an ORM is
* Why ORMs are used
* How SQLModel works internally
* How database engines and sessions work
* The lifecycle of ORM objects

These concepts are essential for understanding how SQLModel manages communication between Python applications and relational databases.

The next sections will cover:

* CRUD operations
* Database relationships
* Pagination
* Dependency injection
