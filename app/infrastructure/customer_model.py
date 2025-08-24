from sqlalchemy import Column, Integer, String
from app.infrastructure.session import Base
from app.domain.customer import Customer

class CustomerModel(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)

    def to_domain(self) -> Customer:
        return Customer(self.id, self.name, self.email)