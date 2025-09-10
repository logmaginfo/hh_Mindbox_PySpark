import os
from dotenv import load_dotenv#pip install python-dotenv
from sqlalchemy import create_engine, text, Text, Table, Column, Integer, String, MetaData, ForeignKey, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, relationship
from typing import Annotated
from sqlalchemy.testing.schema import mapped_column

load_dotenv()
USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

sync_url = f"postgresql+psycopg://{USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
async_url = f"postgresql+asyncpg://{USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

sync_engine = create_engine(url=sync_url, echo=True)
async_engine = create_async_engine(url=async_url, echo=True)

sync_session = sessionmaker(sync_engine)
async_engine = async_sessionmaker(async_engine)

intpk = Annotated[int, mapped_column(primary_key=True, sort_order=-10)]

class Base(DeclarativeBase):
    id: Mapped[intpk]

# связ-я табл
class Association_table_cat_prod(Base):
    __tablename__ = 'association_table_cat_prod'
    prod_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), default=1)
    cat_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), default=1)
    product: Mapped["Products_Child"] = relationship(back_populates="category_associations")
    category: Mapped["Categories_Parent"] = relationship(back_populates="product_associations")

# катег-ии
class Categories_Parent(Base):
    __tablename__ = 'categories'
    name_cat: Mapped[str] = mapped_column(String(200), nullable=True)
    product: Mapped[list["Products_Child"]] = relationship(
        secondary="association_table_cat_prod", back_populates="category")
    product_associations: Mapped[list["Association_table_cat_prod"]] = relationship(
        back_populates="category")

# прод-ы
class Products_Child(Base):
    __tablename__ = 'products'
    name_pr: Mapped[str] = mapped_column(String(200), nullable=True)
    category: Mapped[list["Categories_Parent"]] = relationship(
        secondary="association_table_cat_prod", back_populates="product"    )
    category_associations: Mapped[list["Association_table_cat_prod"]] = relationship(
        back_populates="product")

