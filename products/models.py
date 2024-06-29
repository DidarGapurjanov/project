from sqlalchemy import Table, Column, Integer, Float, String, MetaData

metadata = MetaData()

product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("description", String),
    Column("price", Float),
)


