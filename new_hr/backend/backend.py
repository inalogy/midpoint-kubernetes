import os
import sys
from typing import List

import uvicorn
from base_models import Department as DepartmentObj
from base_models import DepartmentModel
from base_models import Employee as EmployeeObj
from base_models import EmployeeCreate, EmployeeUpdate
from base_models import Position as PositionObj
from base_models import PositionBase
from csv_data_import import create_database_with_data
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Department, Employee, Position, SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy_utils import create_database, database_exists

app = FastAPI()

APP_ORIGIN = os.getenv("APP_ORIGIN", "*")

origins = [
    APP_ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("https")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    return response

def get_db():
    with SessionLocal() as db:
        yield db

@app.get("/api/employees")
def read_employees(db = Depends(get_db)):
    """ Gets all the people infomation """
    with db as ctx:
        query = select(Employee).options(joinedload(Employee.position), joinedload(Employee.department))
        result = ctx.execute(query)
        result = result.fetchall()
    data = [row for row, in result]
    return data

@app.get("/api/employees/{employee_id}", response_model=EmployeeObj)
def read_employee(employee_id: int, db = Depends(get_db)):
    """ Get one employee by ID """
    with db as ctx:
        query = select(Employee).options(joinedload(Employee.position), joinedload(Employee.department)).filter(Employee.id == employee_id)
        #.first()
        employee = ctx.execute(query)
        employee = employee.fetchall()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        data = [row for row, in employee]
        return data[0]

@app.post("/api/employees")
def create_employee(employee_data: EmployeeCreate, db = Depends(get_db)):
    """ Create a new employee """
    with db as ctx:
        # Create Employee object from request data
        department = ctx.query(Department).filter(Department.id == 1).first()
        position = ctx.query(Position).filter(Position.id == 1).first()

        # Create a new employee
        new_employee_data = {
            "department_id": department.id,
            "position_id": position.id,
            **employee_data.model_dump()
        }
        new_employee = Employee(**new_employee_data)

        # Add the new employee to the session and commit
        ctx.add(new_employee)
        ctx.commit()
        ctx.refresh(new_employee)

    return new_employee

@app.delete("/api/employees/{employee_id}")
def delete_employee(employee_id: int, db = Depends(get_db)):
    """ Delete an employee by ID """
    with db as ctx:
        employee = ctx.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        ctx.delete(employee)
        ctx.commit()
        return {"message": "Employee deleted successfully"}

@app.put("/api/employees/{employee_id}")
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db = Depends(get_db)):
    """ Update an employee by ID """
    with db as ctx:
        employee = ctx.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        for field, value in employee_data.dict().items():
            setattr(employee, field, value)
        ctx.commit()
        return {"message": "Employee updated successfully"}

### DEPARTMENT
@app.post("/api/departments", response_model=DepartmentObj)
def create_department(department_data: DepartmentModel, db = Depends(get_db)):
    """ Create a new department """
    with db as ctx:
        department = Department(**department_data.dict())
        ctx.add(department)
        ctx.commit()
        ctx.refresh(department)
        return department

@app.get("/api/departments", response_model=List[DepartmentObj])
def read_departments(db = Depends(get_db)):
    """ Get a department by ID """
    with db as ctx:
        departments = ctx.execute(select(Department))
        departments = departments.fetchall()
        if not departments:
            raise HTTPException(status_code=404, detail="No departments found")
    return [row for row, in departments]

@app.get("/api/departments/{department_id}", response_model=DepartmentObj)
def read_department(department_id: int, db = Depends(get_db)):
    """ Get a department by ID """
    with db as ctx:
        department = ctx.query(Department).get(department_id)
        if not department:
            raise HTTPException(
                status_code=404,
                detail=f"Department with id: {department_id} not found")
        return department

@app.put("/api/departments/{department_id}", response_model=DepartmentObj)
def update_department(department_id: int, department_data: DepartmentModel,
                      db = Depends(get_db)):
    """ Update a department by ID """
    with db as ctx:
        department = ctx.query(Department).get(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        for field, value in department_data.dict().items():
            setattr(department, field, value)
        ctx.commit()
        ctx.refresh(department)
        return department

@app.delete("/api/departments/{department_id}")
def delete_department(department_id: int, db = Depends(get_db)):
    """ Delete a department by ID """
    with db as ctx:
        department = ctx.query(Department).get(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        ctx.delete(department)
        ctx.commit()
        return {"message": "Department deleted successfully"}


### POSITION
@app.post("/api/positions", response_model=PositionBase)
def create_position(position_data: PositionBase, db = Depends(get_db)):
    """ Create a new department """
    with db as ctx:
        position = Position(**position_data.dict())
        ctx.add(position)
        ctx.commit()
        ctx.refresh(position)
        return position

@app.get("/api/positions", response_model=List[PositionObj])
def read_positions(db = Depends(get_db)):
    """ Get a department by ID """
    with db as ctx:
        positions = ctx.execute(select(Position))
        positions = positions.fetchall()
        if not positions:
            raise HTTPException(status_code=404, detail="No departments found")
    return [row for row, in positions]

@app.get("/api/positions/{position_id}", response_model=PositionObj)
def read_position(position_id: int, db = Depends(get_db)):
    """ Get a department by ID """
    with db as ctx:
        department = ctx.query(Position).get(position_id)
        if not department:
            raise HTTPException(
                status_code=404,
                detail=f"Position with id: {position_id} not found")
        return department

@app.put("/api/positions/{position_id}", response_model=PositionBase)
def update_position(position_id: int, position_data: PositionBase,
                      db = Depends(get_db)):
    with db as ctx:
        position = ctx.query(Position).get(position_id)
        if not position:
            raise HTTPException(status_code=404, detail="Position not found!")
        for field, value in position_data.dict().items():
            setattr(position, field, value)
        ctx.commit()
        ctx.refresh(position)
        return position

@app.delete("/api/positions/{position_id}")
def delete_position(position_id: int, db = Depends(get_db)):
    with db as ctx:
        position = ctx.query(Position).get(position_id)
        if not position:
            raise HTTPException(status_code=404, detail="Position not found!")
        ctx.delete(position)
        ctx.commit()
        return {"message": "Position deleted successfully"}



if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Usage: python app.py [run | init-db]")
    if sys.argv[1] == "run":
        uvicorn.run(app, port=8000, host='0.0.0.0')
    elif sys.argv[1] == "init-db":
        create_database_with_data()
