from config import settings
from models import Base
from sqlalchemy import create_engine


sync_engine = create_engine(settings.get_db_url(is_async=False), echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(sync_engine)
