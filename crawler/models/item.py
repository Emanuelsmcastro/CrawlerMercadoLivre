from config.config_db import Base
from sqlalchemy import Column, Float, String, Integer

class ProductModel(Base):
    __tablename__ = 'product'
    id = Column(Integer, autoincrement=True, primary_key=True)
    link = Column(String)
    title = Column(String)
    currency = Column(String)
    price = Column(Float)
    seller = Column(String)
    image = Column(String)
    