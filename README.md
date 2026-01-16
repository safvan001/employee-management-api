# Employee Management API

A RESTful API for managing employees in a company, built with Django REST Framework. This API provides CRUD operations for employee management with authentication, filtering, and pagination.

## Overview

This API allows you to:
- Create, read, update, and delete employees
- Filter employees by department and role
- Paginate through employee lists (10 per page)
- Authenticate using JWT tokens

## Features

- ✅ RESTful API design with proper HTTP methods and status codes
- ✅ JWT-based authentication
- ✅ Email validation and uniqueness checks
- ✅ Filtering by department and role
- ✅ Pagination (10 employees per page)
- ✅ Comprehensive error handling
- ✅ Unit tests for all endpoints
- ✅ Clean, modular code structure

## Project Structure

```
employee-management-api/
├── employee_management/      # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── employees/               # Employees app
│   ├── __init__.py
│   ├── models.py           # Employee model
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── urls.py             # App URL routing
│   ├── admin.py            # Django admin configuration
│   ├── apps.py
│   └── tests.py            # Unit tests
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd employee-management-api
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (REQUIRED for authentication):**
   ```bash
   python manage.py createsuperuser
   ```
   **Note:** You must create a user account first. This user will be used to authenticate and obtain JWT tokens. Without a user account, you cannot access any API endpoints. Django uses its built-in user management system, so there's no separate user registration API endpoint.

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/`
   
   **Important:** You must create a user first (step 5) before you can authenticate and use the API endpoints.

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api
```

### Authentication

All endpoints require JWT authentication. 

**Prerequisites:** Before you can authenticate, you must create a user account using:
```bash
python manage.py createsuperuser
```

This is a one-time setup step. Django uses its built-in user management system, so there's no separate user registration API endpoint.

To authenticate:

1. **Obtain a token:**
   ```http
   POST /api/token/
   Content-Type: application/json

   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

   **Response:**
   ```json
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
   }
   ```

2. **Use the token in requests:**
   Add the access token to the Authorization header:
   ```
   Authorization: Bearer <your_access_token>
   ```

3. **Refresh token (optional):**
   ```http
   POST /api/token/refresh/
   Content-Type: application/json

   {
     "refresh": "your_refresh_token"
   }
   ```

### Employee Model

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2025-01-09"
}
```

**Field Descriptions:**
- `id`: Unique identifier (auto-generated, read-only)
- `name`: Employee name (required, cannot be empty)
- `email`: Email address (required, must be unique and valid)
- `department`: Department name (optional, e.g., "HR", "Engineering", "Sales")
- `role`: Job role (optional, e.g., "Manager", "Developer", "Analyst")
- `date_joined`: Date when employee joined (auto-generated, read-only)

### API Endpoints

#### 1. Create Employee

**POST** `/api/employees/`

Create a new employee.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2025-01-09"
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["An employee with this email already exists."]
}
```

**Example using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "role": "Developer"
  }'
```

#### 2. List All Employees

**GET** `/api/employees/`

Retrieve a paginated list of all employees (10 per page).

**Query Parameters:**
- `page`: Page number (default: 1)
- `department`: Filter by department (e.g., `?department=HR`)
- `role`: Filter by role (e.g., `?role=Manager`)

**Success Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/employees/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "department": "Engineering",
      "role": "Developer",
      "date_joined": "2025-01-09"
    },
    ...
  ]
}
```

**Examples:**
```bash
# Get all employees
curl -X GET http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by department
curl -X GET "http://127.0.0.1:8000/api/employees/?department=HR" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by role
curl -X GET "http://127.0.0.1:8000/api/employees/?role=Manager" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get page 2
curl -X GET "http://127.0.0.1:8000/api/employees/?page=2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 3. Retrieve Single Employee

**GET** `/api/employees/{id}/`

Retrieve a specific employee by ID.

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2025-01-09"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/employees/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Update Employee

**PUT** `/api/employees/{id}/`

Update an employee (all fields required).

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "department": "Sales",
  "role": "Manager"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john.updated@example.com",
  "department": "Sales",
  "role": "Manager",
  "date_joined": "2025-01-09"
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["An employee with this email already exists."]
}
```

**Example:**
```bash
curl -X PUT http://127.0.0.1:8000/api/employees/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "email": "john.updated@example.com",
    "department": "Sales",
    "role": "Manager"
  }'
```

#### 5. Delete Employee

**DELETE** `/api/employees/{id}/`

Delete an employee.

**Success Response (204 No Content):**
(No response body)

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/employees/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## HTTP Status Codes

The API uses the following HTTP status codes:

- **200 OK**: Successful GET, PUT request
- **201 Created**: Successful POST request (employee created)
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Validation error (e.g., duplicate email, empty name)
- **401 Unauthorized**: Missing or invalid authentication token
- **404 Not Found**: Employee with specified ID does not exist

## Testing

Run the test suite:

```bash
python manage.py test
```

The test suite includes:
- Creating employees with valid and invalid data
- Testing duplicate email validation
- Testing empty name validation
- Listing employees with pagination
- Filtering by department and role
- Retrieving, updating, and deleting employees
- Testing authentication requirements
- Testing 404 errors for non-existent employees

## Using Postman

### Setting Up Authentication

**Note:** You must create a user account first using `python manage.py createsuperuser` before you can authenticate.

1. **Get Access Token:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/token/`
   - Body (raw JSON):
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```
   - Copy the `access` token from the response

2. **Configure Authorization:**
   - Go to the Authorization tab
   - Type: Bearer Token
   - Token: Paste your access token

### Testing Endpoints

1. **Create Employee:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/employees/`
   - Body (raw JSON):
     ```json
     {
       "name": "John Doe",
       "email": "john.doe@example.com",
       "department": "Engineering",
       "role": "Developer"
     }
     ```
   - Expected: 201 Created

2. **Test Duplicate Email:**
   - Use the same email again
   - Expected: 400 Bad Request with error message

3. **List Employees:**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/employees/`
   - Expected: 200 OK with paginated results

4. **Filter by Department:**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/employees/?department=Engineering`
   - Expected: 200 OK with filtered results

5. **Retrieve Employee:**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/employees/1/`
   - Expected: 200 OK with employee data

6. **Test 404 Error:**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/employees/999/`
   - Expected: 404 Not Found

7. **Update Employee:**
   - Method: PUT
   - URL: `http://127.0.0.1:8000/api/employees/1/`
   - Body (raw JSON):
     ```json
     {
       "name": "John Updated",
       "email": "john.updated@example.com",
       "department": "Sales",
       "role": "Manager"
     }
     ```
   - Expected: 200 OK with updated data

8. **Delete Employee:**
   - Method: DELETE
   - URL: `http://127.0.0.1:8000/api/employees/1/`
   - Expected: 204 No Content

## Django Admin

Access the Django admin interface at `http://127.0.0.1:8000/admin/` using your superuser credentials to manage employees through the web interface.

## Error Handling

The API provides detailed error messages:

- **Validation Errors (400):**
  ```json
  {
    "name": ["Name cannot be empty."],
    "email": ["An employee with this email already exists."]
  }
  ```

- **Not Found (404):**
  ```json
  {
    "detail": "Not found."
  }
  ```

- **Unauthorized (401):**
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## Development Notes

- The project uses SQLite by default for simplicity. For production, consider using PostgreSQL or MySQL.
- JWT tokens expire after 1 hour. Use the refresh token endpoint to get a new access token.
- The API is configured for development. For production, update `DEBUG = False` and configure proper `ALLOWED_HOSTS` in `settings.py`.

## License

This project is created for assessment purposes.
