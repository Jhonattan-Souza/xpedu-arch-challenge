from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.routers.create_customer_request import CreateCustomerRequest
from app.services.customer_service import CustomerService
from app.infrastructure.session import get_db
from app.routers.customer_response import CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("", response_model=CustomerResponse, status_code=201)
def post(request: CreateCustomerRequest, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.save(request)

@router.get("", response_model=list[CustomerResponse])
def get_all(db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_all()

@router.get("/id/{id}", response_model=CustomerResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    
    customer = service.get_by_id(id)
    
    if customer:
        return customer

    raise HTTPException(status_code=404, detail="Customer not found") 

@router.get("/by-name", response_model=list[CustomerResponse])
def get_by_name(name: str = Query(...), db: Session = Depends(get_db)):
    service = CustomerService(db)
    customers = service.get_by_name(name)
    return customers

@router.get("/count", response_model=int)
def count(db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.count()

@router.put("/id/{id}", response_model=CustomerResponse)
def update(id: int, request: CreateCustomerRequest, db: Session = Depends(get_db)):
    service = CustomerService(db)
    customer = service.update(id, request)

    if customer:
        return customer
    
    raise HTTPException(status_code=404, detail="Customer not found")

@router.delete("/id/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    if service.delete(id):
        return
    
    raise HTTPException(status_code=404, detail="Customer not found")
