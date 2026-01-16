# Quick Setup Guide

## Step-by-Step Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create database migrations:**
   ```bash
   python manage.py makemigrations
   ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a test user for authentication:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create a username and password.

5. **Run the server:**
   ```bash
   python manage.py runserver
   ```

6. **Test the API:**
   - The API will be available at `http://127.0.0.1:8000/api/`
   - Get a token: `POST http://127.0.0.1:8000/api/token/` with your username and password
   - Use the token in the Authorization header: `Bearer <your_token>`

## Running Tests

```bash
python manage.py test
```

## Common Issues

- **ModuleNotFoundError**: Make sure you've activated your virtual environment and installed requirements
- **Database errors**: Run `python manage.py migrate` to set up the database
- **Authentication errors**: Make sure you've created a user with `createsuperuser`
