from models import Base
from sqlalchemy import create_engine

# SYNC_DATABASE_URL = "sqlite:///data.db"
DATABASE_URL = "postgresql://postgres:1231231@localhost:5432/workmate"

sync_engine = create_engine(DATABASE_URL, echo=True)


if __name__ == "__main__":
    Base.metadata.create_all(sync_engine)
