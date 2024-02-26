from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Base 생성
from config import *
import datetime
from enum import Enum

# class engineconn:

#     def __init__(self):
#         self.engine = create_engine(DB_URL, pool_recycle = 500)

#     def sessionmaker(self):
#         Session = sessionmaker(bind=self.engine)
#         session = Session()
#         return session

#     def connection(self):
#         conn = self.engine.connect()
#         return conn

engine = create_engine(os.getenv('RDS_DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db_session():
	db = SessionLocal()
	try:
		yield db # DB 연결 성공한 경우, DB 세션 시작
	finally:
		db.close()
		# db 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

class Bills(Base):
    __tablename__ = "bills"

    bill_no = Column(Integer, primary_key=True)
    bill_id = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    file_link = Column(Text, nullable=False)
    proposer = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
    # status
    # main_category_id
    # main_category = relationship("MainCategory", backref="")
    # council_name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    # resulted_at = Column(DateTime, nullable=True)
    # deleted_at = Column(DateTime, nullable=True)

# class Email(Base):
#     __tablename__ = 'email'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     receiver_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     receiver = relationship("User", back_populates="emails")
#     subject = Column(String, nullable=False)
#     message_body = Column(String, nullable=False)

#     def __init__(self, receiver, subject, message_body):
#         self.receiver = receiver
#         self.subject = subject
#         self.message_body = message_body

# class Keyword(Base):
#     __tablename__ = 'keyword'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     value = Column(String, nullable=False, unique=True)
#     subscriptions = relationship("Subscription", back_populates="keyword", cascade="all, delete-orphan")

#     def __init__(self, value):
#         self.value = value

# class Role(Enum):
#     GUEST = "ROLE_GUEST"
#     USER = "ROLE_USER"

# class Subscription(Base):
#     __tablename__ = 'subscription'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     keyword_id = Column(Integer, ForeignKey('keyword.id'), nullable=False)
#     user = relationship("User", back_populates="subscriptions")
#     keyword = relationship("Keyword", back_populates="subscriptions")

#     def __init__(self, user, keyword):
#         self.user = user
#         self.keyword = keyword

# class User(Base):
#     __tablename__ = 'user'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     picture = Column(String)
#     role = Column(String, nullable=False)
#     subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

#     def __init__(self, name, email, picture, role, subscriptions=None):
#         self.name = name
#         self.email = email
#         self.picture = picture
#         self.role = role
#         self.subscriptions = subscriptions if subscriptions is not None else []

#     def update(self, name, picture):
#         self.name = name
#         self.picture = picture
#         return self

#     def get_role_key(self):
#         return self.role

def insert_bill_metadata(bill_no, bill_id, date, proposer, title, file_link, ):
    with SessionLocal() as db:
        db.add(
            Bills(
	    		bill_no = bill_no, 
	    	    bill_id = bill_id, 
	    	    file_link = file_link, 
				proposer = proposer,
				date = date,
	    	    title = title, 
	    	    created_at=datetime.datetime.now(), 
	    	    updated_at=datetime.datetime.now()
            )
        ) 
        db.commit()

def exist_bill_metadata(bill_no) -> bool:
    with SessionLocal() as db:
        return db.query(Bills).filter(Bills.bill_no == bill_no).first() is not None

if __name__ == "__main__":
	insert_bill_metadata(1, "pdsf", "1", "1")
# class MainCategory:
#     __tablename__ = "main_category"

#     id = Column(Integer, primary_key=True)
#     council_name Column(String, nullable=True)
#     name = Column(String, nullable=True)

