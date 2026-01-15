from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import engine, Base, SessionLocal
from models import Employee, User
from schemas import EmployeeCreate, Employee as EmployeeSchema, EmployeeUpdate, UserCreate, Token
from auth import get_current_user, get_db, authenticate_user, create_access_token, get_password_hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API", description="A REST API to manage employees", version="1.0")

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/employees/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Check if email already exists
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/api/employees/", response_model=List[EmployeeSchema])
def list_employees(
    skip: int = 0,
    limit: int = 10,
    department: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department == department)
    if role:
        query = query.filter(Employee.role == role)
    employees = query.offset(skip).limit(limit).all()
    return employees

@app.get("/api/employees/{employee_id}", response_model=EmployeeSchema)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/api/employees/{employee_id}", response_model=EmployeeSchema)
def update_employee(employee_id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Check email uniqueness if updating email
    if employee_update.email:
        existing = db.query(Employee).filter(Employee.email == employee_update.email, Employee.id != employee_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    for key, value in employee_update.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

@app.delete("/api/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted"}

# To create a default user for testing
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        hashed_password = get_password_hash("password")
        db_user = User(username="admin", hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
    db.close()