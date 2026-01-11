from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.sqlalchemy_models import Base

DATABASE_URL = "sqlite:///./kombucha_business.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()