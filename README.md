# Flask Bulletin Board API

A simple Flask Bulletin API project with **JWT authentication**, **role-based access**, and **SQLAlchemy ORM**.

---

## Features

- JWT authentication (Access + Refresh token + remember_me)
- Role-based authorization (Admin / User / Guest User)
- Users can only modify their own posts (CRUD operation)
- Admin can modify users & posts (CRUD operation)
- SQLAlchemy ORM for database modeling
- MySQL support
- Data validation using Pydantic
- Image store in Cloudinary Server

---

## Tech Stack

- Python 3.10+
- Flask
- Flask-JWT-Extended
- Flask-Migrate
- Flask-SQLAlchemy
- Pydantic
- MySQL / MariaDB
- Flask-Cors
- Flask-Mail
- Cloudinary
- Poetry (for dependency management)

---

## Setup

1. Clone repository

```bash
git clone https://github.com/LinnAungHtet-MTM/Python_Flask_Bulletin.git
cd Python_Flask_Bulletin
```

2. Install dependencies

*(dependencies only install)*
```bash
poetry install --no-root
```

3. Copy .env.example to .env

```bash
copy .env.example .env
```

4. Run Database Migration
```bash
poetry run flask db upgrade
```

4. Run Database Seeder
```bash
poetry run flask seed
```

5. Default Login Credentials
After running the seeder command, you can login using the following credentials:
    **Email:**    =>  admin@gmail.com
-   **Password:** =>  Admin123

6. Run Application
```bash
poetry run flask run
```