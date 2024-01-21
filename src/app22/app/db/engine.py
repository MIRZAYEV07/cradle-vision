from sqlmodel import create_engine

from src.app22 import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
