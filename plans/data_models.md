# Data models
- Customers
    - Customer ID (PK)
    - Name
    - First transaction
    - Created Date
    - Modified Date

- Flavours
    - Flavour ID (PK)
    - Name
    - Created Date
    - Modified Date

- Sales
    - Sales ID (PK)
    - Transaction Date
    - Customer ID (FK)
    - Flavour ID (FK)
    - Quantity

- Flavours History
    - History ID (PK)
    - Flavour ID (FK)
    - Created Date
    - Price
