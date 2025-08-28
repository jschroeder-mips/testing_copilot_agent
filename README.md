# CyberTODO 2077

A cyberpunk-themed TODO application built with Flask, featuring a dark aesthetic inspired by futuristic dystopian themes.

## Features

- ✨ **User Authentication**: Secure login and registration system
- 📱 **Mobile-Ready**: Responsive design with Bulma CSS framework
- 🌙 **Dark Theme**: Cyberpunk-inspired dark theme by default
- 🎨 **Modern UI**: Clean interface with FontAwesome icons
- 🔄 **CRUD Operations**: Create, read, update, and delete TODO items
- 📊 **API Documentation**: Swagger-documented RESTful API
- 🏷️ **Priority Levels**: Critical, High, Medium, Low priority tasks
- 📅 **Due Dates**: Set and track task deadlines
- 🔍 **Filtering**: Filter tasks by status and priority
- 💾 **SQLite Database**: Lightweight database storage
- 🔒 **Type Safety**: Full Python type hints for better code quality

## Technology Stack

- **Backend**: Flask 3.0, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: Bulma CSS, FontAwesome, Vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API**: Flask-RESTX with Swagger documentation
- **Authentication**: Werkzeug password hashing

## Quick Start

### Prerequisites

- Python 3.8+
- uv (recommended) or pip

> **Note**: [uv](https://docs.astral.sh/uv/) is a fast Python package manager written in Rust. It provides significantly faster dependency resolution and installation compared to pip, making development more efficient.

### Installation

#### Option 1: Using uv (recommended)

1. Install uv:
```bash
pip install uv
```

2. Clone the repository:
```bash
git clone https://github.com/jschroeder-mips/testing_copilot_agent.git
cd testing_copilot_agent
```

3. Create and activate virtual environment with dependencies:
```bash
uv sync
```

4. Initialize the database:
```bash
uv run python run.py init-db
```

5. Run the application:
```bash
uv run python run.py
```

#### Option 2: Using pip

1. Clone the repository:
```bash
git clone https://github.com/jschroeder-mips/testing_copilot_agent.git
cd testing_copilot_agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python run.py init-db
```

5. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## API Documentation

The REST API is fully documented with Swagger and available at:
- **API Docs**: `http://localhost:5000/api/docs/`

### API Endpoints

- `GET /api/todos` - List all todos for current user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `GET /api/users/profile` - Get user profile

## Environment Variables

- `FLASK_CONFIG`: Configuration mode (`development`, `production`, `testing`)
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string

## Configuration

The application supports multiple configurations:

- **Development**: Debug mode enabled, SQLite database
- **Production**: Optimized for deployment, environment-based database
- **Testing**: In-memory database, CSRF disabled

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: User email address
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

### Todo
- `id`: Primary key
- `title`: Task title
- `description`: Optional task description
- `status`: Task status (pending, in_progress, completed)
- `priority`: Task priority (low, medium, high, critical)
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp
- `due_date`: Optional due date
- `user_id`: Foreign key to User

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

The project follows PEP8 standards. Run linting with:

```bash
flake8 app/ tests/
```

### Database Operations

Reset the database:
```bash
python run.py reset-db
```

Access Flask shell with models:
```bash
flask shell
```

## Docker Deployment

The application is designed to be Docker-ready and uses uv for fast, reliable dependency management:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .
RUN uv run python run.py init-db

EXPOSE 5000
CMD ["uv", "run", "python", "run.py"]
```

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Input validation and sanitization
- SQL injection prevention with SQLAlchemy ORM

## Mobile Experience

The application is fully responsive and optimized for mobile devices:
- Touch-friendly interface
- Responsive navigation
- Mobile-optimized forms
- Gesture support

## Cyberpunk Theme

The UI features a distinctive cyberpunk aesthetic:
- Neon cyan (#00ffff) and magenta (#ff00ff) accents
- Dark background gradients
- Glowing effects and animations
- Monospace typography
- Futuristic UI elements

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Bulma CSS framework for responsive design
- FontAwesome for iconography
- Flask ecosystem for robust web development
- Cyberpunk 2077 for aesthetic inspiration