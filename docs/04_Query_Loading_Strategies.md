# Query Loading Strategies: Lazy Loading, Eager Loading, and the N+1 Problem

When working with relational databases using an ORM, data often spans multiple related tables.
How the ORM loads related data can significantly affect application performance.

This document explains:

* Lazy loading
* Eager loading
* The N+1 query problem
* How to optimize database queries

---

# 1. Why Loading Strategies Matter

Consider two related tables:

* `users`
* `orders`

A user can have multiple orders.

If an API needs to return users along with their orders, the ORM must decide **when to load the related data**.

Two main strategies exist:

| Strategy      | Behavior                                           |
| ------------- | -------------------------------------------------- |
| Lazy Loading  | Loads related data only when accessed              |
| Eager Loading | Loads related data immediately with the main query |

---

# 2. Lazy Loading (Default Behavior)

Lazy loading means related data is **not fetched immediately**.

Example:

```python
users = session.exec(select(User)).all()
```

At this point:

```text
Only users are loaded.
Orders are not yet loaded.
```

When the code accesses the relationship:

```python
user.orders
```

SQLAlchemy then sends another query to fetch the orders.

Example SQL queries generated:

```sql
SELECT * FROM users;

SELECT * FROM orders WHERE user_id = 1;
```

The second query runs **only when the relationship is accessed**.

---

# 3. The N+1 Query Problem

Lazy loading can cause a serious performance issue called the **N+1 query problem**.

Example code:

```python
users = session.exec(select(User)).all()

for user in users:
    print(user.orders)
```

Suppose there are **5 users**.

Queries executed:

```text
1 query → fetch users
5 queries → fetch orders for each user
```

Total queries:

```text
1 + N queries
```

Example:

```text
SELECT * FROM users;

SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
SELECT * FROM orders WHERE user_id = 3;
SELECT * FROM orders WHERE user_id = 4;
SELECT * FROM orders WHERE user_id = 5;
```

This becomes extremely inefficient when datasets grow.

Example with 100 users:

```text
101 database queries
```

This is known as the **N+1 problem**.

---

# 4. Eager Loading

Eager loading solves this problem by fetching related data **in the same query**.

Example using SQLAlchemy's `selectinload`.

```python
from sqlalchemy.orm import selectinload

statement = select(User).options(selectinload(User.orders))

users = session.exec(statement).all()
```

Now the ORM loads users and their orders efficiently.

Queries generated:

```sql
SELECT * FROM users;

SELECT * FROM orders WHERE user_id IN (1,2,3,4,5);
```

Instead of running one query per user, the ORM fetches related data **in batches**.

---

# 5. Joined Eager Loading

Another eager loading technique is **join loading**.

Example:

```python
from sqlalchemy.orm import joinedload

statement = select(User).options(joinedload(User.orders))

users = session.exec(statement).all()
```

Generated SQL:

```sql
SELECT users.*, orders.*
FROM users
LEFT JOIN orders
ON users.id = orders.user_id;
```

This loads users and orders in **a single query**.

---

# 6. Choosing Between Loading Strategies

| Strategy          | Use Case                               |
| ----------------- | -------------------------------------- |
| Lazy Loading      | When related data is rarely needed     |
| Select-in Loading | Best for most APIs                     |
| Joined Loading    | Useful when returning nested responses |

For API responses that include related objects, eager loading is usually preferred.

---

# 7. Example API Scenario

Suppose an API returns:

```json
{
  "user": "Rahul",
  "orders": [
    {"product": "Laptop"},
    {"product": "Phone"}
  ]
}
```

Without eager loading:

* multiple queries executed
* slower response

With eager loading:

* fewer queries
* faster API performance

---

# 8. Performance Considerations

Poor loading strategies can cause:

* slow APIs
* high database load
* excessive network overhead

Optimized loading strategies:

* reduce database queries
* improve response time
* scale better with large datasets

---

# Summary

In this document we explored:

* Lazy loading
* Eager loading
* The N+1 query problem
* Query optimization techniques

Understanding loading strategies is important when building scalable backend APIs with ORMs.

Efficient database querying ensures applications remain fast even as data grows.
