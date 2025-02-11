from app.db.base import Base
from app.db.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)


# Example of how to seed data (optional):
# def seed_data():
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     # Add your seed data logic here
#     session.close()

if __name__ == "__main__":
    init_db()
    # seed_data()
