from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "Customers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    first_transaction: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    modified_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

class Flavours(Base):
    __tablename__ = "Flavours"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    modified_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

class FlavourHistory(Base):
    __tablename__ = "FlavourHistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    flavour_id: Mapped[int] = mapped_column(ForeignKey("Flavours.id"), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    relationship()

class Sales(Base):
    __tablename__ = "Sales"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    flavour_id: Mapped[int] = mapped_column(ForeignKey("Flavours.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customers.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)