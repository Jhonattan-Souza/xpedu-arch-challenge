from sqlalchemy.orm import Session
from app.infrastructure.customer_model import CustomerModel
from app.infrastructure.customer_repository import CustomerRepository
from app.domain.customer import Customer
from app.routers.create_customer_request import CreateCustomerRequest

class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def save(self, request: CreateCustomerRequest) -> Customer:
        customer_model = CustomerModel()
        customer_model.name = request.name
        customer_model.email = request.email

        return self.repository.save(customer_model)
        
    def get_all(self) -> list[Customer]:
        return [c.to_domain() for c in self.repository.getAll()]
    
    def get_by_id(self, id: int) -> Customer:
        customer = self.repository.get_by_id(id)
        
        return customer.to_domain() if customer else None
    
    def get_by_name(self, name: str) -> list[Customer]:
        customers = self.repository.get_by_name(name)
        return [c.to_domain() for c in customers]

    def count(self) -> int:
        return self.repository.count()

    def update(self, id: int, request: CreateCustomerRequest) -> Customer | None:
        updated = self.repository.update(id, request.name, request.email)
        return updated.to_domain() if updated else None

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
