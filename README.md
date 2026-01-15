# Employee Management API

A REST API to manage employees in a company, built with FastAPI.

## Features

- CRUD operations for employees
- JWT-based authentication
- Filtering and pagination
- Validation and error handling

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`

## API Documentation

### Authentication

To access the API, you need to authenticate first.

POST /token

Body:
```json
{
  "username": "admin",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "token_here",
  "token_type": "bearer"
}
```

Use the token in the Authorization header: `Bearer <token>`

### Endpoints

#### Create Employee
POST /api/employees/

Body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering",
  "role": "Developer"
}
```

#### List Employees
GET /api/employees/?department=Engineering&role=Developer&page=1

#### Get Employee
GET /api/employees/{id}

#### Update Employee
PUT /api/employees/{id}

Body: Partial update fields

#### Delete Employee
DELETE /api/employees/{id}

## Running Tests

`pytest`

## Deployment

The API can be deployed to any platform supporting Python, such as Heroku, Railway, or Render.