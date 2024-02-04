from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Base 생성
from config import *

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

# engine = create_engine(os.getenv('RDS_DATABASE_URL'),connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# Base = declarative_base()

def get_db_session():
	db = SessionLocal()
	try:
		yield db # DB 연결 성공한 경우, DB 세션 시작
	finally:
		db.close()
		# db 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

# class Bills(Base):
#     __tablename__ = "bills"

#     bill_no = Column(Integer, primary_key=True)
#     bill_id = Column(String, nullable=False)
#     title = Column(Text, nullable=False)
#     file_link = Column(Text, nullable=False)

#     # status
#     # main_category_id
#     # main_category = relationship("MainCategory", backref="")
#     # council_name = Column(String, nullable=True)
#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime, nullable=False)
    # resulted_at = Column(DateTime, nullable=True)
    # deleted_at = Column(DateTime, nullable=True)

# class MainCategory:
#     __tablename__ = "main_category"

#     id = Column(Integer, primary_key=True)
#     council_name Column(String, nullable=True)
#     name = Column(String, nullable=True)

