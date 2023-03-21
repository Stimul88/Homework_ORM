import sqlalchemy
from sqlalchemy.orm import sessionmaker

from Homework_ORM import create_tables, Book, Publisher, Shop, Stock, Sale

DSN = "postgresql://postgres:9012@localhost:5432/Homework_ORM"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()

# создание объектов
jr = Publisher(name='Джоан Роулинг')

jt = Publisher(name='Джон Толкин')

ns1 = Shop(name='Буквоед')

ns2 = Shop(name='Лабиринт ')

b1 = Book(title='Гарри Поттер и философский камень', publisher=jr)
b2 = Book(title='Гарри Поттер и тайная комната', publisher=jr)

s1 = Stock(book=b1, shop=ns1, count='5')
s2 = Stock(book=b2, shop=ns1, count='2')

sl1 = Sale(price='500', date_sale='09-11-2022', stock=s1, count='2')
sl2 = Sale(price='600', date_sale='08-11-2022', stock=s2, count='5')

b3 = Book(title='Хоббит', publisher=jt)
b4 = Book(title='Властелин колец. Хранители кольца', publisher=jt)

s3 = Stock(book=b3, shop=ns2, count='6')
s4 = Stock(book=b4, shop=ns2, count='3')

sl3 = Sale(price='800', date_sale='07-11-2022', stock=s3, count='7')
sl4 = Sale(price='400', date_sale='05-11-2022', stock=s4, count='9')

session.add(jr)
session.add(jt)
session.add_all([b1, b2, b3, b4])
session.add(ns2)
session.add(ns1)
session.add_all([s1, s2, s3, s4])
session.add_all([sl1, sl2, sl3, sl4])
session.commit()

query = session.query(Publisher, Book, Stock, Sale, Shop)
query = query.join(Book, Book.publisher_id == Publisher.id)
query = query.join(Stock, Stock.book_id == Book.id)
query = query.join(Sale, Sale.stock_id == Stock.id)
query = query.join(Shop, Shop.id == Stock.shop_id)
records = query

ql = input('Введите имя или идентификатор издателя: ')
if ql.isdigit():
    for publisher, book, stock, sale, shop in records.filter(Publisher.id == ql):
        print(book.title, shop.name, sale.price, sale.date_sale)
else:
    for publisher, book, stock, sale, shop in records.filter(Publisher.name == ql):
        print(book.title, shop.name, sale.price, sale.date_sale)