import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.sqlalchemy_models import Base, Customer, Flavours, FlavourHistory, Sales


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


def _table_has(term: str) -> bool:
    names = Base.metadata.tables.keys()
    term = term.lower()
    return any(term in name.lower() for name in names)


def test_customer(session):
    assert _table_has("customer"), "Expected a table related to customers in metadata"


def test_flavours(session):
    assert _table_has("flavour") or _table_has("flavors") or _table_has("flavor"), "Expected a table related to flavours in metadata"


def test_flavour_history(session):
    # allow "history" or "hist" in combination with flavour/flavor
    names = [n.lower() for n in Base.metadata.tables.keys()]
    matches = [n for n in names if ("flavour" in n or "flavor" in n) and ("history" in n or "hist" in n)]
    assert matches, "Expected a flavour history table in metadata"


def test_sales(session):
    assert _table_has("sale") or _table_has("sales"), "Expected a table related to sales in metadata"


def test_session_executes_simple_query(session):
    # ensure session is usable for executing simple SQL
    result = session.execute(text("SELECT 1")).scalar()
    assert int(result) == 1

def test_price_match(session):
    """Test that Sales can correctly match to the appropriate FlavourHistory price."""
    from datetime import date
    from sqlalchemy import func, select
    
    # Create test data
    flavour = Flavours(id=1, name="Ginger")
    customer = Customer(id=1, name="Test Customer")
    session.add_all([flavour, customer])
    session.flush()
    
    flavour = Flavours(id=2, name="Strawberry")
    session.add_all([flavour])
    session.flush()
    
    # Add FlavourHistory records with different prices and dates
    history_records = [
        FlavourHistory(flavour_id=1, price=10000, created_date=date(2025, 12, 1)),
        FlavourHistory(flavour_id=1, price=12000, created_date=date(2026, 1, 1)),  # Should match this one
        FlavourHistory(flavour_id=1, price=13000, created_date=date(2026, 1, 13)),

        FlavourHistory(flavour_id=2, price=14000, created_date=date(2025, 12, 1)),
        FlavourHistory(flavour_id=2, price=15000, created_date=date(2026, 1, 1)),  # Should match this one
        FlavourHistory(flavour_id=2, price=16000, created_date=date(2026, 1, 13)),
    ]
    session.add_all(history_records)
    session.flush()
    
    # Add Sales record
    sale = Sales(
        transaction_date=date(2026, 1, 11),
        flavour_id=1,
        customer_id=1,
        quantity=1
    )
    session.add(sale)
    session.commit()

    sale = Sales(
        transaction_date=date(2026, 1, 11),
        flavour_id=2,
        customer_id=1,
        quantity=1
    )
    session.add(sale)
    session.commit()
    
    # Query using SQLAlchemy ORM to find the matching price
    base_cte = (
        select(
            Sales.transaction_date,
            Sales.flavour_id,
            FlavourHistory.price,
            func.row_number()
            .over(
                partition_by=Sales.flavour_id,
                order_by=FlavourHistory.created_date.desc(),
            )
            .label("rn"),
        )
        .join(
            FlavourHistory,
            (Sales.transaction_date > FlavourHistory.created_date)
            & (Sales.flavour_id == FlavourHistory.flavour_id),
        )
        .cte("base")
    )

    price_cte = (
        select(
            base_cte.c.flavour_id,
            base_cte.c.price,
        )
        .where(base_cte.c.rn == 1)
        .cte("price")
    )

    stmt = (
        select(
            Sales,
            price_cte.c.price,
        )
        .join(
            price_cte,
            Sales.flavour_id == price_cte.c.flavour_id,
        )
    )

    matching_histories = session.execute(stmt).all()

    
    assert len(matching_histories) == 2, f"Expected 2 matching FlavourHistory records, got {len(matching_histories)}"

    for matching_history in matching_histories:
        assert matching_history is not None, "Expected to find a matching FlavourHistory record"
        if matching_history[0].flavour_id == 1:
            assert matching_history[1] == 12000, f"Expected price 12000, got {matching_history[1]}"
        elif matching_history[0].flavour_id == 2:
            assert matching_history[1] == 15000, f"Expected price 15000, got {matching_history[1]}"