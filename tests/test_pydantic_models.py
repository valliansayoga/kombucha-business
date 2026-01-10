import pytest
from pydantic import ValidationError
from backend.pydantic_models import FlavourCreate, SalesCreate
from datetime import datetime
from pytz import timezone

TZ = timezone("Asia/Jakarta")
TEST_DATA = [
    (1, 1, datetime(2026, 1, 10, 11, 0, tzinfo=TZ)),
    (1, 2, datetime(2026, 1, 10, 12, 0, tzinfo=TZ)),
    (1, 3, datetime(2026, 1, 10, 20, 0, tzinfo=TZ)),
    (2, 1, datetime(2026, 1, 10, 16, 6, tzinfo=TZ)),
    (3, 1, datetime(2026, 1, 10, 15, 23, tzinfo=TZ)),
]


def test_flavour_validation_success():
    data = {"name": "Original", "price": 20000}
    flavour = FlavourCreate(**data)
    assert flavour.name == "Original"
    assert flavour.price == 20000


def test_flavour_validation_invalid_price():
    data = {"name": "Original", "price": -5000}
    with pytest.raises(ValidationError):
        FlavourCreate(**data)


def test_flavour_validation_invalid_short_name():
    data = {"name": "Xy", "price": 5000}
    with pytest.raises(ValidationError):
        FlavourCreate(**data)


def test_flavour_validation_invalid_long_name():
    data = {"name": "Xyz" * 20, "price": 5000}
    with pytest.raises(ValidationError):
        FlavourCreate(**data)


def test_sales_single_input():
    date = datetime(2026, 1, 10, 10, 0, tzinfo=TZ)
    data = {
        "customer_id": 1,
        "flavour_id": 1,
        "transaction_date": date,
    }
    sale = SalesCreate(**data)
    assert sale.customer_id == 1
    assert sale.flavour_id == 1
    assert sale.transaction_date == date


def test_sales_invalid_date_input():
    with pytest.raises(ValueError):
        date = datetime(-69, 1, 10, 10, 0, tzinfo=TZ)
        data = {
            "customer_id": 1,
            "flavour_id": 1,
            "transaction_date": date,
        }
        sale = SalesCreate(**data)


@pytest.mark.parametrize("customer_id,flavour_id,transaction_date", TEST_DATA)
def test_sales_bulk_input(
    customer_id: int,
    flavour_id: int,
    transaction_date: datetime,
):
    data = {
        "customer_id": customer_id,
        "flavour_id": flavour_id,
        "transaction_date": transaction_date,
    }
    sale = SalesCreate(**data)
    assert sale.customer_id == customer_id
    assert sale.flavour_id == flavour_id
    assert sale.transaction_date == transaction_date
