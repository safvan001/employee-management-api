from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee
from datetime import date


class EmployeeAPITestCase(TestCase):
    """Test cases for Employee API endpoints."""
    
    def setUp(self):
        """Set up test data and authenticated client."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create authenticated client
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Sample employee data
        self.employee_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'department': 'Engineering',
            'role': 'Developer'
        }
    
    def test_create_employee_success(self):
        """Test creating an employee with valid data."""
        response = self.client.post('/api/employees/', self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, 'John Doe')
        self.assertEqual(Employee.objects.get().email, 'john.doe@example.com')
    
    def test_create_employee_duplicate_email(self):
        """Test creating an employee with duplicate email returns 400."""
        Employee.objects.create(**self.employee_data)
        response = self.client.post('/api/employees/', self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_create_employee_empty_name(self):
        """Test creating an employee with empty name returns 400."""
        invalid_data = self.employee_data.copy()
        invalid_data['name'] = ''
        response = self.client.post('/api/employees/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_employee_invalid_email(self):
        """Test creating an employee with invalid email returns 400."""
        invalid_data = self.employee_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post('/api/employees/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_employees(self):
        """Test listing all employees."""
        # Create multiple employees
        Employee.objects.create(
            name='Alice Smith',
            email='alice@example.com',
            department='HR',
            role='Manager'
        )
        Employee.objects.create(
            name='Bob Johnson',
            email='bob@example.com',
            department='Sales',
            role='Analyst'
        )
        
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_list_employees_pagination(self):
        """Test pagination with more than 10 employees."""
        # Create 15 employees
        for i in range(15):
            Employee.objects.create(
                name=f'Employee {i}',
                email=f'employee{i}@example.com',
                department='Engineering'
            )
        
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        
        # Test second page
        response = self.client.get('/api/employees/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
    
    def test_list_employees_filter_by_department(self):
        """Test filtering employees by department."""
        Employee.objects.create(
            name='Alice Smith',
            email='alice@example.com',
            department='HR',
            role='Manager'
        )
        Employee.objects.create(
            name='Bob Johnson',
            email='bob@example.com',
            department='Engineering',
            role='Developer'
        )
        
        response = self.client.get('/api/employees/?department=HR')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['department'], 'HR')
    
    def test_list_employees_filter_by_role(self):
        """Test filtering employees by role."""
        Employee.objects.create(
            name='Alice Smith',
            email='alice@example.com',
            department='HR',
            role='Manager'
        )
        Employee.objects.create(
            name='Bob Johnson',
            email='bob@example.com',
            department='Engineering',
            role='Developer'
        )
        
        response = self.client.get('/api/employees/?role=Manager')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['role'], 'Manager')
    
    def test_retrieve_employee_success(self):
        """Test retrieving a single employee by ID."""
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.get(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['email'], 'john.doe@example.com')
    
    def test_retrieve_employee_not_found(self):
        """Test retrieving a non-existent employee returns 404."""
        response = self.client.get('/api/employees/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_employee_success(self):
        """Test updating an employee with valid data."""
        employee = Employee.objects.create(**self.employee_data)
        update_data = {
            'name': 'John Updated',
            'email': 'john.updated@example.com',
            'department': 'Sales',
            'role': 'Manager'
        }
        response = self.client.put(f'/api/employees/{employee.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.name, 'John Updated')
        self.assertEqual(employee.email, 'john.updated@example.com')
    
    def test_update_employee_duplicate_email(self):
        """Test updating an employee with duplicate email returns 400."""
        employee1 = Employee.objects.create(**self.employee_data)
        employee2 = Employee.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            department='HR'
        )
        
        update_data = self.employee_data.copy()
        update_data['email'] = 'jane@example.com'
        response = self.client.put(f'/api/employees/{employee1.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_employee_success(self):
        """Test deleting an employee returns 204."""
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.delete(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
    
    def test_delete_employee_not_found(self):
        """Test deleting a non-existent employee returns 404."""
        response = self.client.delete('/api/employees/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_authentication_required(self):
        """Test that unauthenticated requests are rejected."""
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_employee_date_joined_auto_generated(self):
        """Test that date_joined is automatically generated."""
        employee = Employee.objects.create(**self.employee_data)
        self.assertIsNotNone(employee.date_joined)
        self.assertEqual(employee.date_joined, date.today())
