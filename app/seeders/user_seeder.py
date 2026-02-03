from app.extension import db
from app.models.user import User
from werkzeug.security import generate_password_hash


def user_seeder():
    try:
        user = User(
            name="admin",
            email="admin@gmail.com",
            password=generate_password_hash("Admin123"),
            role=False,
        )

        db.session.add(user)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        raise e
