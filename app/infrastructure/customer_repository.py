from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.infrastructure.customer_model import CustomerModel

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def getAll(self) -> list[CustomerModel]:
        statement = select(CustomerModel)
        result = self.db.execute(statement)
        return list(result.scalars().all())
    
    def save(self, data: CustomerModel) -> CustomerModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    
    def get_by_id(self, id: int) -> CustomerModel:
        return self.db.get(CustomerModel, id)
    
    def get_by_name(self, name: str) -> list[CustomerModel]:
        stmt = select(CustomerModel).where(CustomerModel.name.ilike(f"%{name}%"))
        result = self.db.execute(stmt)
        return list(result.scalars().all())

    def count(self) -> int:
        stmt = select(func.count()).select_from(CustomerModel)
        return self.db.execute(stmt).scalar_one()

    def update(self, id: int, name: str, email: str) -> CustomerModel | None:
        customer = self.get_by_id(id)
        if not customer:
            return None
        customer.name = name
        customer.email = email
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, id: int) -> bool:
        customer = self.get_by_id(id)
        if not customer:
            return False
        self.db.delete(customer)
        self.db.commit()
        return True
