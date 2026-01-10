import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield Session()

    session.close()
    Base.metadata.drop_all(engine)


def test_customer():
    pass


def test_flavours():
    pass


def test_flavour_history():
    pass


def test_sales():
    pass
