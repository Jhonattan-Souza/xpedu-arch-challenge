from pydantic import BaseModel
from pydantic import ConfigDict

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)

