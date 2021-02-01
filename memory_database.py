from pprint import pprint

from sqlalchemy import create_engine, Float, Text, Date, desc, text
from sqlalchemy import Column, Integer, String, CheckConstraint, UniqueConstraint,\
    ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

# inicjalizacja połaczenia z bazą danych
engine = create_engine('sqlite:///:memory:', echo=False)
# engine = create_engine('sqlite:///C:\\Users\\User\\\Data_Science\\Flask_SQLAlch\\agidb.db', echo=False)

Session = sessionmaker(bind=engine)  # metoda która tworzy klasę
session = Session()  # obiekt klasy session

# deklatrowanie mappingu czyli tworzenie klasy bazowej
# # obsluga zarządzania tabelami
Base = declarative_base()


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, Sequence('city_id_seq'), primary_key=True)  # sequence tylko Oracle
    name = Column(String(50), unique=True, nullable=False)
    population = Column(Integer)
    customer = relationship('Customer', back_populates="city")

    def __repr__(self):
        return "<City(name = '%s',population = '%s')>" % (self.name, self.population)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float)


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String(50))
    gender = Column(Text, server_default='F')
    cityid = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', back_populates='customer')
    order = relationship('Order', back_populates='order')
    __table_args__ = (CheckConstraint(gender.in_(['M', 'F'])),)  # tu jest tupla więc musi być przecinek


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    orderDate = Column(Date)
    customerid = Column(Integer, ForeignKey('customer.id'))
    productid = Column(Integer, ForeignKey('product.id'))


Order.customer = relationship("Customer", back_populates="order")
Customer.order = relationship("Order", order_by=Order.id, back_populates="customer")


Base.metadata.create_all(engine) # żeby to co jest w klasie było w tabeli


session.add_all(
    [
        City(name='Warszawa', population=1800000),
        City(name='Poznań', population=500000),
        City(name='Katowice', population=300000),
        City(name='Sopot', population=40000),
        City(name='Cieplewo', population=100),
        Product(name='Angry_Birds', price=10),
        Product(name='Minecraft', price=5),
        Product(name='Block Puzzle Jewel', price=8),
        Product(name='Merge Dragons', price=2),
        Customer(name='Jack Black', gender='M', cityid=2),
        Customer(name='Mary White', gender='F', cityid=3),
        Customer(name='John Brown', gender='M', cityid=2),
        Customer(name='Susan Green', gender='F', cityid=1),
        Customer(name='Tom Orange', gender='M', cityid=2),
        Order(customerid=3, productid=4, orderDate=datetime(2019, 10, 13)),
        Order(customerid=2, productid=1, orderDate=datetime(2019, 10, 10)),
        Order(customerid=5, productid=3, orderDate=datetime(2019, 10, 11)),
        Order(customerid=2, productid=3, orderDate=datetime(2019, 10, 12)),
        Order(customerid=4, productid=1, orderDate=datetime(2019, 10, 13)),
        Order(customerid=5, productid=2, orderDate=datetime(2019, 10, 10))
    ]
)
session.commit()

# susan = session.query(Customer).filter_by(name='Susan Green').one()
# print(susan.gender)
# sopot = session.query(City).filter_by(name='Sopot').all()
# print(sopot)
# all = session.query(Customer.name, Customer.gender, Customer.cityid).all()
# print(all)
# 1
# cieplewo = session.query(City).filter(City.population == 100).first()
# print(cieplewo.id, cieplewo.name)
# print('************************')
# session.delete(cieplewo)
# session.commit()
# 2
# tomOrange = session.query(Customer).filter(Customer.name == 'Tom Orange').first()
# session.delete(tomOrange)
# session.commit()
# tomOrange = session.query(Customer).filter(Customer.name == 'Tom Orange').first()
# print(tomOrange)
#
# 3 selecty
# # zwraca całą tabelę Customer
# for customer in session.query(Customer):
#     print(customer.name, customer.gender, customer.cityid)
# #
# # zwraca tylko wybrane kolumny
# for cus_name, cus_city in session.query(Customer.name, Customer.cityid):
#     print(cus_name, cus_city)
# #
# # # zmienia nazwe koluny w zwracanym obiekcie
# for row in session.query(Customer.name.label("full_name")).all():
#     print(row.full_name)
# # limit i offset ze slice
# for c in session.query(Customer).order_by(Customer.id)[0:3]:
#     print(c.name, c.id)
# to jest to samo co wyżej
# for c in session.query(Customer).order_by(Customer.id).limit(3):
#     print(c.name, c.id)
#
# for c in session.query(Customer).order_by(Customer.id).offset(3):
#     print(c.name, c.id)
# #
# for c in session.query(City).filter(City.population > 250000):
#     print(c.name, c.population)
# #
# for c in session.query(City).filter(City.population > 250000).filter(City.id < 3):
#     print(c.name, c.population)
# # equals
# for c in session.query(City).filter(City.name == 'Warszawa'):
#     print(c.name, c.population)
# # not equals
# for c in session.query(City).filter(City.name != 'Warszawa'):
#     print(c.name, c.population)
# # like
# for c in session.query(City).filter(City.name.like('%w%')):
#     print(c.name, c.population)
#
# # #in
# for c in session.query(City).filter(City.id.in_([1, 3])):
#     print(c.name, c.population, c.id)
# #
# #  not in
# for c in session.query(City).filter(~City.id.in_([1, 3])):
#     print(c.name, c.population)
# #
# # # and two examples
# from sqlalchemy import and_
# for c in session.query(Customer).filter(and_(Customer.id > 2, Customer.name.like('%e%'))):
#     print(c.name, c.id)
#
# for c in session.query(Customer).filter(Customer.id > 2, Customer.name.like('%e%')):
#     print(c.name, c.id)
# # # or
# from sqlalchemy import or_
# for c in session.query(Customer).filter(or_(Customer.id > 2, Customer.name.like('%e%'))):
#     print(c.name, c.id)
#
# # is null/not null !=
# for c in session.query(Customer).filter(Customer.name == None):
#     print(c.name)
# 4
# for c in session.query(City).order_by(City.population)[::-1]:
#     print(c.name, c.population)
# 6
# for c in session.query(City).order_by(desc(City.population)).limit(2):
#     print(c.name, c.population)

# # zwracanie listy elementów
#
# result = session.query(City).order_by(desc(City.population)).all()
# print(result)
# # zwracanie jednego elementu
# result = session.query(City).order_by(City.population).filter(City.name == "Sopot").one()
# print(result)
# # wywołanie składni sql
# # takie małe hakowanie bo po statement można pisać komendy sql
# result = session.query(City).from_statement(text("Select*from city")).all()
# print(result)
# # # count()
# result = session.query(Customer).filter(Customer.id > 1).count()
# print(result)
# result = session.query(Customer).count()
# print(result)
# # # order  coout() per Customer
from sqlalchemy import func
# result = session.query(Order.customerid, func.count(Order.customerid)).group_by(Order.customerid).all()
# print(result)
#
# max_id = session.query(func.max(Customer.id)).first()  # jak nie ma tego firsta to nic nie wyświetla
# min_id = session.query(func.min(Customer.name)).first()
# print(max_id)
# print(min_id)
# max_id = session.query(func.max(Customer.id)).scalar()  # jak jest scalar zamiast first to mamy liczbę a nie tuplę
# min_id = session.query(func.min(Customer.id)).scalar()
# print('*'*40)
# print(max_id)
# print(min_id)
#### distinct()
from sqlalchemy import distinct
# print('$'*40)
# print(session.query(City).filter(City.id < 10).all())
# print((session.query(City).filter(City.id < 10).distinct(City.population).all()))
# Zadanie
# # Zmień w tabeli Order miesiąc zamówienia na listopad we wszystkich rekordach z roku 2019
# result = session.query(Order).filter(Order.orderDate).all()
# for i in session.query(Order):
#     print(i.orderDate)
# for order in result:
#     order.orderDate = datetime(order.orderDate.year, 11, order.orderDate.day)
#
# session.commit()
# #
# for i in session.query(Order):
#     print(i.orderDate)
#                                      RELACJE
# relacje jeden do wielu
"""W przypadku relacji jeden-do-wielu tworzy się dyrektywy relationship() na obu 
klasach pokazując, które kolumny są ze sobą powiązane"""

# gdynia = City(name="Gdynia", population=250000)
#
# gdynia.customer = [Customer(name='Robert Kubica', gender='M'), Customer(name='Anna Lewandowska', gender='F')]
# session.add(gdynia)
# session.commit()
# #
# # # odczytywanie Customers korzystając z powiązanej klasy City
# #
# result = session.query(City).filter(City.name == 'Gdynia').one()
# for cus in result.customer:
#     print(cus.name)

# # masowe tworzenie połączonych obiektów
# nowe_miasta = [
#     City(
#         name="Malbork",
#         population=38000,
#         customer=[Customer(name="Oliwia Nowak", gender="F"), Customer(name="Barbara Kowalska", gender="F")]),
#     City(
#         name="Olsztyn",
#         population=170000,
#         customer=[Customer(name="Zbigniew Nowak", gender="M"), Customer(name="Jan Kowalski", gender="M")]
#     )
# ]
#
# session.add_all(nowe_miasta)
# session.commit()
# #
# result = session.query(City).all()
# for cus in result:
#     print(cus.name)

# result = session.query(City).filter(City.name == 'Olsztyn').one()
# for cus in result.customer:
#     print(cus.name)

# # zapytania z join
# session.add_all(
#     [
#         City(name='Wejherowo', population=50000),
#         City(name='Bydgoszcz', population=350000),
#         City(name='Szczecin', population=400000)
#     ]
# )
# session.commit()

# INNER JOIN z użyciem Query.filter()
# for cus, cit in session.query(Customer, City).filter(City.id == Customer.cityid).all():
#     print(cit.name, cus.name)

# INNER JOIN z użyciem Query.join()
# result = session.query(City).join(Customer).all()
# for cit in result:
#     # print(cit.name)
#     for cus in cit.customer:
#         print(cus.name, cit.name)
"""Query.join() wie jak połączyć klasy ponieważ istnieje tylko jeden klucz 
między nimi"""
# # Pokaż miasta i klientów jeśli jacyś są (LEFT JOIN)
# result = session.query(City).outerjoin(Customer).all()
# for cit in result:
#     # print(cit.name)
#     for cus in cit.customer:
#         print(cus.name)
# inner join on many tables
# result = session.query(Customer).join(City).join(Order).join(Product).all()
#
# # Wyświetl imiona, nazwiska i daty zamówień złożonych przez kobiety
result = session.query(Customer).join(Order, Customer.id == Order.customerid).filter(Customer.gender == 'F')
for i in result:
    print(i.name, i.order[0].orderDate)