from sqlalchemy.orm import Session
from config import config_db
from models.item import ProductModel


class RepositoryProduct:
    
    def __init__(self, session: Session = config_db.SessionLocal()) -> None:
        self.session = session
    
    def insert_product(self, item: dict) -> ProductModel:
        product = ProductModel(**item)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product