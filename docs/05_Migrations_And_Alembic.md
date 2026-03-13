# Database Migrations and Alembic

As backend applications grow, database schemas evolve.
Tables change, columns are added, indexes are modified, and relationships are updated.

Managing these changes safely requires **database migrations**.

This document explains:

* What database migrations are
* Why `create_all()` is not suitable for production
* How migrations work
* How Alembic manages schema changes
* Typical migration workflow

---

# 1. What Are Database Migrations?

A **database migration** is a controlled way to update the structure of a database.

Examples of schema changes:

* Adding a new column
* Removing a column
* Renaming a column
* Creating new tables
* Adding indexes or constraints

Instead of manually altering the database each time, migrations allow developers to **track schema changes in code**.

---

# 2. The Problem With `create_all()`

During early development with SQLModel, developers often use:

```python
SQLModel.metadata.create_all(engine)
```

This command:

* creates tables that do not exist
* does **not update existing tables**

Example problem:

Initial model:

```python
class User(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    name: str
```

Later you update the model:

```python
class User(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
```

If you run `create_all()` again:

```text
The new column "age" will NOT be added.
```

This is why production systems use **migration tools**.

---

# 3. What is Alembic?

**Alembic** is the official migration tool used with SQLAlchemy-based ORMs.

It helps manage database schema changes by:

* generating migration scripts
* tracking schema versions
* applying upgrades and downgrades

It integrates seamlessly with SQLModel because SQLModel is built on top of SQLAlchemy.

---

# 4. Why Migrations Are Important

Migrations solve several problems:

| Problem                                | Solution                      |
| -------------------------------------- | ----------------------------- |
| Schema changes break production        | Controlled updates            |
| Team members modify database structure | Version-controlled migrations |
| Databases differ across environments   | Consistent schema updates     |

In production systems:

```text
Code version → Migration version → Database schema
```

All environments remain synchronized.

---

# 5. Installing Alembic

Install Alembic with pip:

```bash
pip install alembic
```

This installs the migration CLI tool.

---

# 6. Initializing Alembic

Initialize Alembic in the project directory:

```bash
alembic init migrations
```

This creates a new folder structure:

```text
migrations/
│
├── versions/
├── env.py
├── script.py.mako
└── alembic.ini
```

Explanation:

| File            | Purpose                           |
| --------------- | --------------------------------- |
| versions/       | Stores migration files            |
| env.py          | Alembic environment configuration |
| alembic.ini     | Database connection settings      |
| script template | Migration file template           |

---

# 7. Configuring Database Connection

Update the database URL inside **alembic.ini**.

Example:

```ini
sqlalchemy.url = postgresql://postgres:password@localhost:5432/sqlmodel_demo
```

Alternatively, you can load environment variables from your application settings.

---

# 8. Generating a Migration

After modifying models, generate a migration:

```bash
alembic revision --autogenerate -m "create users table"
```

Alembic compares:

```text
current database schema
vs
current SQLModel metadata
```

Then generates a migration script.

Example file:

```text
migrations/versions/123_create_users_table.py
```

---

# 9. Migration Script Structure

Example migration file:

```python
def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String())
    )

def downgrade():
    op.drop_table("users")
```

Explanation:

| Function    | Purpose               |
| ----------- | --------------------- |
| upgrade()   | Apply schema changes  |
| downgrade() | Revert schema changes |

---

# 10. Applying Migrations

To apply migrations:

```bash
alembic upgrade head
```

This upgrades the database to the latest schema version.

Alembic keeps track of applied migrations using a special table:

```text
alembic_version
```

---

# 11. Rolling Back Migrations

If something goes wrong, migrations can be rolled back.

Example:

```bash
alembic downgrade -1
```

This reverts the most recent migration.

Example:

```bash
alembic downgrade base
```

Reverts all migrations.

---

# 12. Typical Migration Workflow

A typical development workflow looks like this:

```text
1. Modify SQLModel models
2. Generate migration
3. Review migration script
4. Apply migration to database
```

Commands:

```bash
alembic revision --autogenerate -m "add age column"
alembic upgrade head
```

---

# 13. Migrations in Production Systems

In real-world applications:

* migrations are stored in version control
* deployments automatically run migrations
* schema changes are reviewed before deployment

Benefits:

* consistent database schema
* easier collaboration
* safe schema evolution

---

# Summary

In this document we covered:

* what database migrations are
* limitations of `create_all()`
* how Alembic manages schema changes
* generating and applying migrations
* safe database evolution practices

Migrations are essential for maintaining database integrity in production backend systems.
