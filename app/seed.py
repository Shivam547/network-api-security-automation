from app.database import SessionLocal, engine, Base
from app.models import User


Base.metadata.create_all(bind=engine)


def seed_users():

    db = SessionLocal()

    users = [
        User(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role="admin",
            active=True
        ),
        User(
            username="manager",
            email="manager@example.com",
            password="manager123",
            role="manager",
            active=True
        ),
        User(
            username="user1",
            email="user1@example.com",
            password="user123",
            role="user",
            active=True
        ),
        User(
            username="readonly",
            email="readonly@example.com",
            password="readonly123",
            role="readonly",
            active=True
        )
    ]

    for user in users:

        existing_user = (
            db.query(User)
            .filter(User.username == user.username)
            .first()
        )

        if not existing_user:
            db.add(user)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_users()
    print("Users seeded successfully.")