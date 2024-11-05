from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention, schema="bookstore")
Base = declarative_base(metadata=metadata)


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Название жанра")
    books = relationship("Book", back_populates="genre")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Название автора")
    books = relationship("Book", back_populates="author")


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Имя города")
    days_to_deliver = Column(Integer, nullable=False, comment="Дней на доставку")
    clients = relationship("Client", back_populates="city")


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Имя клиента")
    city_id = Column(Integer, ForeignKey("city.id"), comment="Город клиента")
    city = relationship("City", back_populates="clients")
    email = Column(String, comment="Почта клиента")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String, nullable=False, comment="Название книги")
    author_id = Column(Integer, ForeignKey("author.id"), comment="Автор книги")
    author = relationship("Author", back_populates="books")
    genre_id = Column(Integer, ForeignKey("genre.id"), comment="Жанр книги")
    genre = relationship("Genre", back_populates="books")
    price = Column(Integer, nullable=False, comment="Цена книги")
    amount = Column(Integer, nullable=False, comment="Кол-во стока")
    book_purchases = relationship("BookPurchase", back_populates="book")


class Purchase(Base):
    __tablename__ = "purchase"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    description = Column(String, nullable=False, comment="Пожелания клиента")
    client_id = Column(Integer, ForeignKey("client.id"), comment="Клиент")
    client = relationship("Client", back_populates="purchases")
    book_purchases = relationship("BookPurchase", back_populates="purchase")
    purchase_steps = relationship("PurchaseStep", back_populates="purchase")


class BookPurchase(Base):
    __tablename__ = "book_purchase"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchase.id"), comment="Пожелания")
    purchase = relationship("Purchase", back_populates="book_purchases")
    book_id = Column(Integer, ForeignKey("book.id"), comment="Книга")
    book = relationship("Book", back_populates="book_purchases")
    amount = Column(Integer, nullable=False, comment="Кол-во")


class Step(Base):
    __tablename__ = "step"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Название этапа")
    purchase_steps = relationship("PurchaseStep", back_populates="step")


class PurchaseStep(Base):
    __tablename__ = "purchase_step"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchase.id"), comment="Покупка")
    purchase = relationship("Purchase", back_populates="purchase_steps")
    step_id = Column(Integer, ForeignKey("step.id"), comment="Этап")
    step = relationship("Step", back_populates="purchase_steps")
    begin_date = Column(Date, nullable=False, comment="Начало этапа")
    end_date = Column(Date, nullable=False, comment="Конец этапа")
