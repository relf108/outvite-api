from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_session():
    engine = create_engine("postgresql://tsutton:tsutton@localhost:5432/outvite")
    Session = sessionmaker(bind=engine)
    return Session()
