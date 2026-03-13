# Dependency Injection and Session Management

Modern backend frameworks rely heavily on **dependency injection** to manage resources such as database connections, authentication, and configuration.

In applications built with FastAPI and SQLModel, dependency injection is commonly used to manage **database sessions**.

This document explains:

* What dependency injection is
* How FastAPI implements it
* Why `Depends()` is used
* Why `yield` is used for database sessions
* The lifecycle of a database request

---

# 1. What is Dependency Injection?

Dependency Injection (DI) is a design pattern where a function receives the resources it needs **from the framework**, instead of creating them itself.

Without dependency injection:

```python
def get_users():
    session = Session(engine)
```

The function is responsible for creating the session.

With dependency injection:

```python
def get_users(session: Session):
```

The session is **provided by the framework**.

Benefits:

* Better code organization
* Reusable components
* Easier testing
* Centralized resource management

---

# 2. Dependency Injection in FastAPI

FastAPI provides dependency injection using `Depends()`.

Example:

```python
from fastapi import Depends

@router.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()
```

Explanation:

| Component     | Meaning                               |
| ------------- | ------------------------------------- |
| `Depends()`   | tells FastAPI to resolve a dependency |
| `get_session` | function that creates the session     |
| `session`     | injected database session             |

FastAPI automatically calls the dependency function before executing the route.

---

# 3. Creating a Database Session Dependency

Example implementation:

```python
def get_session():

    with Session(engine) as session:
        yield session
```

This function acts as a **dependency provider**.

Steps:

1. A session is created
2. It is provided to the API route
3. After the request finishes, the session is closed

---

# 4. Why `yield` is Used Instead of `return`

Using `yield` allows FastAPI to manage **setup and cleanup logic**.

Example flow:

```
Request arrives
     ↓
FastAPI calls dependency
     ↓
Session is created
     ↓
Session yielded to route
     ↓
Route executes
     ↓
Response returned
     ↓
Session automatically closed
```

If `return` was used, FastAPI would not have control over cleanup.

---

# 5. Context Manager (`with` Statement)

The database session is created using a context manager.

Example:

```python
with Session(engine) as session:
```

A context manager ensures:

* resources are properly opened
* resources are automatically closed

Equivalent logic:

```
open session
try:
    run code
finally:
    close session
```

This prevents **connection leaks**.

---

# 6. Complete Example

Database dependency:

```python
def get_session():
    with Session(engine) as session:
        yield session
```

Route using dependency:

```python
@router.get("/users")
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
```

FastAPI automatically handles session creation and cleanup.

---

# 7. Request Lifecycle with Database

Complete request flow:

```
Client Request
     ↓
FastAPI Router
     ↓
Dependency Resolution
     ↓
Database Session Created
     ↓
Route Logic Executes
     ↓
Response Returned
     ↓
Session Closed
```

This ensures each request has its own database session.

---

# 8. Why This Pattern is Important

Using dependency injection for database sessions provides several advantages:

* prevents session conflicts
* ensures connections are closed
* improves application scalability
* simplifies testing

It also follows best practices used in production backend systems.

---

# Summary

In this document we covered:

* Dependency injection principles
* FastAPI's `Depends()` mechanism
* Database session management
* Why `yield` is used in dependencies
* Request lifecycle with database sessions

Understanding dependency injection is essential when building scalable backend services.

The next document will explore **database loading strategies**, including lazy loading, eager loading, and the N+1 query problem.
