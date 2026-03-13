# CRUD Operations, Relationships, and Pagination

This document explains how data is manipulated in a backend built using **FastAPI**, **SQLModel**, and **PostgreSQL**.

We will cover:

* CRUD operations
* Database relationships
* Pagination strategies

These concepts form the backbone of almost every backend system.

---

# 1. CRUD Operations

CRUD stands for:

| Operation | Meaning                   |
| --------- | ------------------------- |
| Create    | Insert data into database |
| Read      | Retrieve data             |
| Update    | Modify existing data      |
| Delete    | Remove data               |

Most backend APIs revolve around these four operations.

---

# 2. Creating Data

Creating records involves three main steps:

1. Create a model object
2. Add it to the session
3. Commit the transaction

Example:

```python
user = User(name="Rahul", email="rahul@test.com", age=22)

session.add(user)
session.commit()
session.refresh(user)
```

Explanation:

| Step              | Purpose                         |
| ----------------- | ------------------------------- |
| session.add()     | Adds object to session          |
| session.commit()  | Writes changes to database      |
| session.refresh() | Fetches updated database values |

This generates a SQL query similar to:

```sql
INSERT INTO users (name, email, age) VALUES ('Rahul', 'rahul@test.com', 22);
```

---

# 3. Reading Data

Data retrieval is done using queries.

Example:

```python
users = session.exec(select(User)).all()
```

Get a specific record:

```python
user = session.get(User, user_id)
```

Equivalent SQL:

```sql
SELECT * FROM users;
SELECT * FROM users WHERE id = 1;
```

---

# 4. Updating Data

Updating involves modifying an existing object.

Example:

```python
user = session.get(User, user_id)

user.name = "Rahul Sharma"
user.age = 23

session.add(user)
session.commit()
session.refresh(user)
```

Generated SQL:

```sql
UPDATE users SET name='Rahul Sharma', age=23 WHERE id=1;
```

---

# 5. Deleting Data

Deleting records removes them from the database.

Example:

```python
user = session.get(User, user_id)

session.delete(user)
session.commit()
```

Equivalent SQL:

```sql
DELETE FROM users WHERE id = 1;
```

---

# 6. Database Relationships

Relational databases allow tables to be connected.

Common types of relationships:

| Relationship | Example            |
| ------------ | ------------------ |
| One-to-One   | User → Profile     |
| One-to-Many  | User → Orders      |
| Many-to-Many | Students → Courses |

---

# 7. One-to-Many Relationship

Example: A user can have many orders.

User model:

```python
class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    orders: List["Order"] = Relationship(back_populates="user")
```

Order model:

```python
class Order(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    product: str
    user_id: int = Field(foreign_key="users.id")

    user: Optional["User"] = Relationship(back_populates="orders")
```

Explanation:

| Component      | Purpose                      |
| -------------- | ---------------------------- |
| foreign_key    | Links tables                 |
| Relationship() | ORM relationship             |
| back_populates | Enables bidirectional access |

Usage:

```python
user.orders
order.user
```

---

# 8. Many-to-Many Relationship

Example:

Students ↔ Courses

This requires a **link table**.

Example:

```python
class Enrollment(SQLModel, table=True):

    student_id: int = Field(foreign_key="student.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)
```

This table connects both models.

---

# 9. Pagination

Pagination is used when datasets are large.

Instead of returning thousands of rows, we return a subset.

Example request:

```
GET /users?offset=0&limit=10
```

Meaning:

* skip first 0 records
* return next 10

---

# 10. Pagination Implementation

Example:

```python
def get_users(session: Session, offset: int = 0, limit: int = 10):

    statement = select(User).offset(offset).limit(limit)

    return session.exec(statement).all()
```

Equivalent SQL:

```sql
SELECT * FROM users LIMIT 10 OFFSET 0;
```

---

# 11. Why Pagination is Important

Without pagination:

* APIs may return thousands of rows
* Responses become slow
* Database load increases

With pagination:

* faster responses
* lower memory usage
* better API performance

---

# 12. Production Pagination Response

A better API response structure:

```json
{
  "total": 100,
  "offset": 0,
  "limit": 10,
  "data": [
    { "id": 1, "name": "Rahul" },
    { "id": 2, "name": "Aman" }
  ]
}
```

This allows clients to know:

* total records
* next page
* current page size

---

# Summary

In this document we covered:

* CRUD operations
* How SQLModel performs database interactions
* Table relationships
* Pagination strategies for large datasets

These concepts are essential when designing scalable backend APIs.

Next, we will explore **dependency injection and session management**, which powers database access in FastAPI applications.
