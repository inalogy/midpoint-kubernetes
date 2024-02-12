from datetime import date
from typing import Optional

from pydantic import BaseModel


#### Department
class DepartmentBase(BaseModel):
    name: str

class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

class DepartmentModel(DepartmentBase):
    ...

    
#### POSITIONS
class PositionBase(BaseModel):
    name: str

class Position(PositionBase):
    id: int

    class Config:
        orm_mode = True

class PositionModel(PositionBase):
    ...

#### EMPLOYEE
class EmployeeBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    sex: Optional[str]
    birthdate: Optional[date]
    id_card: Optional[str]
    personal_email: Optional[str]
    personal_phone: Optional[str]
    iban: Optional[str]
    home_street: Optional[str]
    home_city: Optional[str]
    home_postal_code: Optional[str]
    home_country: Optional[str]
    work_street: Optional[str]
    work_city: Optional[str]
    work_postal_code: Optional[str]
    work_country: Optional[str]
    language: Optional[str]
    nationality: Optional[str]
    employment_type: Optional[str]
    division: Optional[str]
    picture: Optional[bytes]

class EmployeeCreate(EmployeeBase):
    department_id: int
    position_id: int

class EmployeeUpdate(EmployeeBase):
    department_id: int
    position_id: int

class Employee(EmployeeBase):
    id: int
    department_id: int
    position_id: int
    department: Department
    position: Position

    class Config:
        orm_mode = True

        
