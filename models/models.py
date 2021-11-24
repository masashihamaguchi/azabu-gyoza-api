from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import csv

databese_file = 'db/production.db'
engine = create_engine('sqlite:///' + databese_file, encoding='utf-8')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    category_id = Column(Text, nullable=False, unique=True)
    category = Column(Text, nullable=False)
    category_name = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __init__(self, category_id, category, category_name):
        self.category_id = category_id
        self.category = category
        self.category_name = category_name


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(Text, nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    category = relationship('Category')

    def __init__(self, name, category_id, price):
        self.name = name
        self.category_id = category_id
        self.price = price


# init function
def init_db():
    Base.metadata.create_all(bind=engine)
    print(engine.engine)
    # create tables
    tables = Base.metadata.tables.keys()
    print(tables)
    if 'categories' not in tables or 'menus' not in tables:
        print('create tables ...')
        Base.metadata.create_all(bind=engine)
        print('complete!')
    else:
        print('already created!')

    # insert data
    if session.query(Category.id).count() == 0:
        print('insert categories...')
        try:
            with open('csv/categories.csv', 'r') as file:
                records = csv.DictReader(file)
                for r in records:
                    record = Category(**{
                        'category_id': r.get('category_id'),
                        'category': r.get('category'),
                        'category_name': r.get('category_name')
                    })
                    session.add(record)
                session.commit()
            print('complete!')
        except IOError:
            session.rollback()
            print(IOError)
            print('error')
        finally:
            pass

    if session.query(Menu.id).count() == 0:
        print('insert menus...')
        try:
            with open('csv/menus.csv', 'r') as file:
                records = csv.DictReader(file)
                for r in records:
                    record = Menu(**{
                        'name': r.get('name'),
                        'category_id': r.get('category_id'),
                        'price': r.get('price')
                    })
                    session.add(record)
                session.commit()
            print('complete!')
        except IOError:
            session.rollback()
            print(IOError)
            print('error')
        finally:
            pass


# create DB and insert records
init_db()
