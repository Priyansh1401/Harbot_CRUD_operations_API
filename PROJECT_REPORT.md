# Employee Management REST API - Project Submission

## Project Overview

**Project Title:** Employee Management System  
**Technology Stack:** Python, FastAPI, SQLAlchemy, SQLite, JWT Authentication  
**Deployment:** Railway (Live URL: [Your Railway URL])  
**GitHub Repository:** https://github.com/Priyansh1401/Harbot_CRUD_operations_API  
**Date:** January 15, 2026  

## Objective

Build a REST API for managing employees in a company with CRUD operations, proper authentication, validation, filtering, pagination, and comprehensive testing.

## Features Implemented

### ✅ Core Functionality
- **CRUD Operations**: Create, Read, Update, Delete employees
- **Data Validation**: Email uniqueness, required fields, proper data types
- **Error Handling**: Appropriate HTTP status codes (201, 404, 400, 204)
- **Filtering & Pagination**: Filter by department/role, paginate results (10 per page)

### ✅ Authentication & Security
- **JWT Token Authentication**: Secure endpoints with Bearer tokens
- **Password Hashing**: PBKDF2-SHA256 for secure password storage
- **Protected Routes**: All employee endpoints require authentication

### ✅ Database & Models
- **SQLite Database**: Lightweight, file-based database
- **SQLAlchemy ORM**: Object-relational mapping for database operations
- **Employee Model**: id, name, email, department, role, date_joined
- **User Model**: For authentication (admin user)

### ✅ Testing
- **Unit Tests**: Comprehensive test coverage for all endpoints
- **Test Database**: Separate SQLite database for testing
- **Edge Cases**: Duplicate emails, invalid IDs, authentication failures

### ✅ Documentation
- **API Documentation**: Clear endpoint descriptions
- **Usage Instructions**: How to run locally and deploy
- **Authentication Guide**: Token-based authentication flow

## API Endpoints

### Authentication
```
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=password

Response: {"access_token": "jwt_token", "token_type": "bearer"}
```

### Employee Management
All employee endpoints require `Authorization: Bearer <token>` header.

#### Create Employee
```
POST /api/employees/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering",
  "role": "Developer"
}

Response: 201 Created
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2026-01-15T00:00:00"
}
```

#### List Employees
```
GET /api/employees/?department=Engineering&role=Developer&page=1

Response: 200 OK
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "department": "Engineering",
    "role": "Developer",
    "date_joined": "2026-01-15T00:00:00"
  }
]
```

#### Get Single Employee
```
GET /api/employees/1

Response: 200 OK
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2026-01-15T00:00:00"
}
```

#### Update Employee
```
PUT /api/employees/1
Content-Type: application/json

{
  "name": "John Smith",
  "department": "Engineering"
}

Response: 200 OK
{
  "id": 1,
  "name": "John Smith",
  "email": "john@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2026-01-15T00:00:00"
}
```

#### Delete Employee
```
DELETE /api/employees/1

Response: 204 No Content
```

## Project Structure

```
Habot_Project/
├── main.py                 # FastAPI application
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── auth.py                # Authentication logic
├── database.py            # Database configuration
├── tests/
│   ├── __init__.py
│   └── test_main.py       # Unit tests
├── requirements.txt       # Dependencies
├── README.md             # Documentation
├── .gitignore            # Git ignore rules
└── .github/
    └── copilot-instructions.md
```

## Installation & Setup

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/Priyansh1401/Harbot_CRUD_operations_API.git
cd Habot_Project
```

2. **Create Virtual Environment**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Application**
```bash
uvicorn main:app --reload
```

5. **Access API**
- Local: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs

### Testing

```bash
pytest
```

All 6 tests should pass.

## Deployment

### Railway Deployment

1. **Connect GitHub Repository**
   - Go to Railway.app
   - Create new project
   - Connect GitHub repo

2. **Automatic Deployment**
   - Railway detects Python project
   - Installs dependencies from requirements.txt
   - Runs: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Live URL**
   - Railway provides live URL
   - API accessible at: https://your-app-name.railway.app

## Authentication Flow

1. **Get Token**
   ```
   POST /token
   username=admin&password=password
   ```

2. **Use Token**
   ```
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   ```

3. **Access Protected Endpoints**
   All `/api/employees/*` endpoints require valid Bearer token

## Testing with Postman

### 1. Authentication
- Method: POST
- URL: https://your-live-url/token
- Body: x-www-form-urlencoded
  - username: admin
  - password: password
- Copy access_token from response

### 2. Create Employee
- Method: POST
- URL: https://your-live-url/api/employees/
- Headers: Authorization: Bearer <token>
- Body: raw JSON
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "department": "Engineering",
    "role": "Developer"
  }
  ```

### 3. List Employees
- Method: GET
- URL: https://your-live-url/api/employees/
- Headers: Authorization: Bearer <token>

### 4. Get Employee
- Method: GET
- URL: https://your-live-url/api/employees/1
- Headers: Authorization: Bearer <token>

### 5. Update Employee
- Method: PUT
- URL: https://your-live-url/api/employees/1
- Headers: Authorization: Bearer <token>
- Body: raw JSON
  ```json
  {
    "name": "John Smith"
  }
  ```

### 6. Delete Employee
- Method: DELETE
- URL: https://your-live-url/api/employees/1
- Headers: Authorization: Bearer <token>

## Error Handling Examples

### Duplicate Email
```
POST /api/employees/
{
  "name": "Jane Doe",
  "email": "john@example.com"
}

Response: 400 Bad Request
{
  "detail": "Email already registered"
}
```

### Employee Not Found
```
GET /api/employees/999

Response: 404 Not Found
{
  "detail": "Employee not found"
}
```

### Invalid Authentication
```
GET /api/employees/

Response: 401 Unauthorized
{
  "detail": "Could not validate credentials"
}
```

## RESTful Principles Compliance

- ✅ **Proper HTTP Methods**: GET, POST, PUT, DELETE
- ✅ **Resource-Based URLs**: /api/employees/, /api/employees/{id}
- ✅ **HTTP Status Codes**: 200, 201, 204, 400, 401, 404
- ✅ **Stateless**: No server-side sessions
- ✅ **Content Negotiation**: JSON responses
- ✅ **Idempotent Operations**: PUT and DELETE are idempotent

## Security Features

- **JWT Authentication**: Stateless token-based auth
- **Password Hashing**: PBKDF2-SHA256 with salt
- **Input Validation**: Pydantic models prevent invalid data
- **SQL Injection Protection**: SQLAlchemy parameterized queries
- **CORS Ready**: FastAPI handles CORS automatically

## Performance Considerations

- **Pagination**: Limits results to 10 employees per page
- **Database Indexing**: Email field indexed for uniqueness
- **Efficient Queries**: SQLAlchemy optimizes database access
- **Lightweight Dependencies**: Minimal package footprint

## Future Enhancements

- PostgreSQL database for production
- Role-based access control (RBAC)
- API rate limiting
- Comprehensive logging
- Docker containerization
- API versioning
- Swagger/OpenAPI documentation

## Conclusion

This project demonstrates a complete REST API implementation with modern Python technologies. The API follows RESTful principles, includes proper authentication, comprehensive testing, and is production-ready with Railway deployment.

**Live Demo:** [Insert your Railway URL here]  
**GitHub:** https://github.com/Priyansh1401/Harbot_CRUD_operations_API

---

*Submitted by: Priyansh Aggarwal*  
*Position: Python Backend Developer*  
*Date: January 15, 2026*</content>
<parameter name="filePath">c:\Users\Priyansh Aggarwal\Desktop\Projects\Habot_Project\PROJECT_REPORT.md