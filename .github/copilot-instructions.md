# Testing Copilot Agent Repository

Python Flask TODO application repository for testing GitHub Copilot coding agents. This repository is designed to become a full-featured Flask web application with SQLAlchemy, user authentication, CRUD operations, and a Cyberpunk-themed frontend.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Initial Setup and Environment
- Bootstrap the Python environment:
  - `python3 --version` - should show Python 3.12+
  - `python3 -m venv venv` - creates virtual environment in ~3 seconds
  - `source venv/bin/activate` - activates virtual environment
  - ALWAYS activate the virtual environment before running any Python commands

### Installing Dependencies
- Install Flask and core dependencies:
  - `pip install flask sqlalchemy flask-sqlalchemy` - may fail due to network limitations. If timeout occurs, use `pip install --timeout 120 flask sqlalchemy flask-sqlalchemy` or install packages individually
  - Install development and testing tools:
  - `pip install pytest black flake8 mypy` - may fail due to network limitations. If timeout occurs, install packages individually
  - Install additional dependencies as needed for the Flask TODO app:
  - `pip install flask-login flask-wtf wtforms` - for authentication
  - `pip install flask-swagger-ui` - for API documentation
- **NETWORK ISSUES**: pip install commands may fail with "Read timed out" errors due to firewall limitations. If this occurs:
  - Try installing packages individually: `pip install flask`, then `pip install sqlalchemy`, etc.
  - Use longer timeouts: `pip install --timeout 120 flask`
  - Document any persistent network failures as "cannot verify due to network limitations"

### Building and Running the Application
- ALWAYS run the bootstrapping steps first before attempting to run any application code
- Start the Flask development server:
  - `python app.py` or `flask run` - starts immediately
  - Development server runs on http://127.0.0.1:5000 by default
  - Use `Ctrl+C` to stop the server
- NEVER CANCEL: Allow the development server to start completely before testing

### Testing
- Run the test suite:
  - `pytest` - runs all tests in ~1 second for basic tests, NEVER CANCEL
  - `pytest -v` - verbose output for detailed test results
  - `pytest tests/` - run tests from specific directory
  - Test suite timing scales with application complexity - expect 5-15 seconds for a full TODO app test suite

### Code Quality and Linting
- ALWAYS run these commands before committing changes:
  - `black .` - formats code automatically in ~0.1 seconds
  - `black --check .` - checks formatting without changes
  - `flake8 .` - lints code for PEP8 compliance in ~0.2 seconds
  - `mypy .` - type checking takes ~4 seconds, NEVER CANCEL
- CI/CD will fail if code quality checks do not pass

## Validation

### Manual Testing Requirements
- ALWAYS manually test the application after making changes:
  - Start the Flask development server
  - Navigate to http://127.0.0.1:5000 in a browser or test with curl
  - Test the main user flows:
    - User registration and login
    - Creating, reading, updating, and deleting TODO items
    - User authentication and session management
- For API endpoints, test with curl or a tool like Postman:
  - `curl -X GET http://127.0.0.1:5000/api/todos`
  - `curl -X POST http://127.0.0.1:5000/api/todos -H "Content-Type: application/json" -d '{"title": "Test TODO"}'`

### Development Workflow Validation
- After making any changes to the application:
  1. Run linting: `black . && flake8 . && mypy .`
  2. Run tests: `pytest -v`
  3. Start the application: `python app.py`
  4. Test functionality manually in browser or with curl
  5. Stop the application with Ctrl+C

## Expected Project Structure

Based on repository requirements and Flask best practices, the project will eventually contain:

```
/
├── app.py                 # Main Flask application entry point
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── models/               # SQLAlchemy database models
│   ├── __init__.py
│   ├── user.py          # User model with authentication
│   └── todo.py          # TODO item model
├── routes/               # Flask route handlers
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── api.py           # REST API routes
│   └── main.py          # Main application routes
├── templates/            # Jinja2 HTML templates
│   ├── base.html        # Base template with Bulma CSS
│   ├── login.html       # User login page
│   ├── register.html    # User registration page
│   └── todos.html       # TODO list interface
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_auth.py     # Authentication tests
│   ├── test_api.py      # API endpoint tests
│   └── test_models.py   # Model tests
├── migrations/          # Database migration files
└── instance/            # Instance-specific files (SQLite DB)
```

## Technology Stack Requirements

- **Backend**: Flask with SQLAlchemy ORM
- **Database**: SQLite for development (stored in instance/ directory)
- **Authentication**: Flask-Login for session management
- **Frontend**: Bulma CSS framework with FontAwesome icons
- **Theme**: Dark Cyberpunk aesthetic
- **API Documentation**: Swagger/OpenAPI with Flask-RESTX or Flask-SWAGGER-UI
- **Code Quality**: Black (formatting), Flake8 (linting), MyPy (type checking)
- **Testing**: Pytest with Flask test client
- **Deployment**: Docker-ready (future requirement)

## Common Development Tasks

### Creating Database Models
- Always use SQLAlchemy ORM with type hints
- Follow the pattern: `from flask_sqlalchemy import SQLAlchemy`
- Include proper relationships between User and TODO models
- Example: `db.relationship('Todo', backref='user', lazy=True)`

### API Development
- Use Flask-RESTX or similar for API documentation
- Always include proper HTTP status codes
- Implement CRUD operations for TODO items
- Include authentication checks on protected endpoints

### Frontend Development
- Use Bulma CSS framework for responsive design
- Implement dark theme by default
- Include FontAwesome icons for UI elements
- Follow mobile-first responsive design principles

## Timeout Settings and Performance

- **Virtual Environment Creation**: 3 seconds (use 15 second timeout)
- **Package Installation**: May fail due to network timeouts (use 120+ second timeout)
- **Code Formatting (Black)**: 0.1 seconds (use 5 second timeout) - requires installation
- **Linting (Flake8)**: 0.2 seconds (use 5 second timeout) - requires installation  
- **Type Checking (MyPy)**: 4 seconds (use 15 second timeout, NEVER CANCEL) - requires installation
- **Test Execution**: 1-15 seconds depending on test coverage (use 30 second timeout) - requires pytest installation
- **Flask Development Server Startup**: Immediate (use 10 second timeout)
- **Python Syntax Checking**: Use `python3 -m py_compile filename.py` for basic syntax validation without external dependencies

## Common Commands Reference

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Verify basic Python functionality
python3 --version  # Should show Python 3.12+
python3 -c "print('Python environment ready')"

# Basic syntax checking (no external dependencies required)
python3 -m py_compile filename.py

# Install dependencies (may fail due to network limitations)
pip install --timeout 120 flask sqlalchemy flask-sqlalchemy flask-login flask-wtf wtforms pytest black flake8 mypy
```

### Development Workflow
```bash
# Format and lint code
black .
flake8 .
mypy .

# Run tests
pytest -v

# Start development server
python app.py
# OR
flask run
```

### Repository Structure Commands
```bash
# List repository contents
ls -la

# Show current repository structure
find . -type f -name "*.py" | head -20
```

## Current Repository State

The following are outputs from frequently run commands in the current repository state. Reference them instead of running bash commands to save time.

### Repository Root Structure
```bash
$ ls -la
total 68
drwxr-xr-x 6 runner docker  4096 Aug 28 14:47 .
drwxr-xr-x 3 runner docker  4096 Aug 28 14:39 ..
drwxr-xr-x 7 runner docker  4096 Aug 28 14:42 .git
drwxr-xr-x 2 runner docker  4096 Aug 28 14:47 .github
-rw-r--r-- 1 runner docker  4688 Aug 28 14:40 .gitignore
-rw-r--r-- 1 runner docker 34523 Aug 28 14:40 LICENSE
```

### Python Files Check
```bash
$ find . -name "*.py" -not -path "./venv/*" | head -10
# Currently no Python application files - repository is in initial state
```

### Key Files Present
- **.gitignore**: Python-focused with comprehensive exclusions (4,688 bytes)
- **LICENSE**: GNU AGPL v3 license file (34,523 bytes)
- **.github/copilot-instructions.md**: These instructions