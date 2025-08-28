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

CyberTODO 2077 is fully containerized and ready for deployment with Docker. This comprehensive guide covers everything from basic Docker usage to production deployment.

### Prerequisites

- **Docker**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- **Docker Compose**: Included with Docker Desktop, or install separately
- **Git**: To clone the repository

### Quick Start with Docker

#### Option 1: Using Docker Compose (Recommended)

The easiest way to run CyberTODO 2077 is with Docker Compose:

```bash
# Clone the repository
git clone https://github.com/jschroeder-mips/testing_copilot_agent.git
cd testing_copilot_agent

# Start the application
docker compose up --build

# Or run in detached mode
docker compose up --build -d
```

The application will be available at `http://localhost:5000`

To stop the application:
```bash
docker compose down
```

#### Option 2: Using Docker Directly

Build and run the container manually:

```bash
# Build the Docker image
docker build -t cybertodo .

# Run the container
docker run -p 5000:5000 cybertodo

# Or run in detached mode with a name
docker run -d --name cybertodo -p 5000:5000 cybertodo
```

### Environment Configuration

Configure the application using environment variables:

#### Development Setup
```bash
docker run -p 5000:5000 \
  -e FLASK_CONFIG=development \
  -e SECRET_KEY=your-development-secret-key \
  cybertodo
```

#### Production Setup
```bash
docker run -p 5000:5000 \
  -e FLASK_CONFIG=production \
  -e SECRET_KEY=your-strong-production-secret-key \
  -e DATABASE_URL=sqlite:///app/instance/cybertodo.db \
  cybertodo
```

### Data Persistence

#### Using Docker Volumes

To persist your data between container restarts:

```bash
# Create a named volume
docker volume create cybertodo_data

# Run with volume mounted
docker run -p 5000:5000 \
  -v cybertodo_data:/app/instance \
  cybertodo
```

#### Using Bind Mounts

Mount a local directory for data persistence:

```bash
# Create local data directory
mkdir -p ./data

# Run with bind mount
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/instance \
  cybertodo
```

### Docker Compose Configuration

#### Basic Setup (SQLite)

The default `docker-compose.yml` uses SQLite and includes volume mounting:

```yaml
version: '3.8'

services:
  cybertodo:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_CONFIG=production
      - SECRET_KEY=your-secret-key-here-change-in-production
    volumes:
      - ./instance:/app/instance
    restart: unless-stopped
```

**Important**: Before running `docker compose up`, create the instance directory:
```bash
mkdir -p instance
```

If you encounter permission issues, you can also run without volume mounting (data won't persist):
```bash
# Remove the volumes section from docker-compose.yml temporarily
docker compose up --build
```

#### Advanced Setup with PostgreSQL

For production deployment with PostgreSQL, create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  cybertodo:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_CONFIG=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://cybertodo:${DB_PASSWORD}@postgres:5432/cybertodo
    depends_on:
      - postgres
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: cybertodo
      POSTGRES_USER: cybertodo
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

Run with:
```bash
# Create environment file
echo "SECRET_KEY=your-super-secret-key" > .env
echo "DB_PASSWORD=your-db-password" >> .env

# Start with PostgreSQL
docker compose -f docker-compose.prod.yml up --build -d
```

### Docker Build Process

The Dockerfile uses a multi-stage approach for efficiency and security:

1. **Base Image**: Python 3.11 slim for minimal size
2. **Dependencies**: Installs system packages (gcc, curl) and Python dependencies
3. **Security**: Runs as non-root user `cybertodo`
4. **Health Check**: Monitors application health
5. **Fallback**: Uses pip if uv installation fails

Key features:
- **Fast Builds**: Uses uv for rapid dependency installation
- **Security**: Non-root user execution
- **Health Monitoring**: Built-in health checks
- **Flexibility**: Fallback to pip if uv fails

### Port Configuration

- **Default Port**: 5000 (Flask development server)
- **Container Port**: 5000 (exposed by Dockerfile)
- **Host Mapping**: Configurable (e.g., `-p 8080:5000` for port 8080)

Example custom port mapping:
```bash
docker run -p 8080:5000 cybertodo
# Access at http://localhost:8080
```

### Development with Docker

#### Live Development with Volume Mounting

For development with auto-reload:

```bash
docker run -p 5000:5000 \
  -v $(pwd):/app \
  -e FLASK_CONFIG=development \
  cybertodo
```

#### Development Docker Compose

Create `docker-compose.dev.yml` for development:

```yaml
version: '3.8'

services:
  cybertodo:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_CONFIG=development
      - SECRET_KEY=dev-secret-key
    volumes:
      - .:/app
      - /app/__pycache__
    restart: unless-stopped
```

### Troubleshooting

#### Common Issues

**Port Already in Use**
```bash
# Find process using port 5000
lsof -i :5000

# Use different port
docker run -p 5001:5000 cybertodo
```

**Permission Denied**
```bash
# Fix file permissions
sudo chown -R $USER:$USER ./instance
```

**Container Won't Start**
```bash
# Check logs
docker logs cybertodo

# Check with docker compose
docker compose logs cybertodo
```

**Database Issues**
```bash
# If you get "unable to open database file" error:
# 1. Ensure instance directory exists
mkdir -p instance

# 2. Check permissions (may require sudo)
ls -la instance/

# 3. Reset database inside container
docker exec -it cybertodo flask init-db

# 4. Or run without persistent volumes initially
docker run -p 5000:5000 cybertodo

# With docker compose
docker compose exec cybertodo flask init-db
```

#### Health Check

The container includes a health check endpoint:
```bash
# Check container health
docker ps  # Shows health status

# Manual health check
curl http://localhost:5000/
```

### Best Practices

#### Security
- Use strong, unique `SECRET_KEY` in production
- Don't expose unnecessary ports
- Use specific image tags instead of `latest`
- Regularly update base images for security patches

#### Performance
- Use multi-stage builds for smaller images
- Leverage Docker layer caching
- Use `.dockerignore` to exclude unnecessary files

#### Production Deployment
- Use PostgreSQL for production databases
- Implement proper logging and monitoring
- Use reverse proxy (nginx) for HTTPS termination
- Configure resource limits

#### Monitoring
```bash
# Monitor resource usage
docker stats cybertodo

# View logs in real-time
docker logs -f cybertodo
```

### Environment Variables Reference

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `FLASK_CONFIG` | Configuration mode | `development` | `production` |
| `SECRET_KEY` | Flask secret key | Random | `your-secret-key` |
| `DATABASE_URL` | Database connection | SQLite | `postgresql://user:pass@host:5432/db` |

### Container Management

#### Useful Commands

```bash
# List running containers
docker ps

# Stop container
docker stop cybertodo

# Remove container
docker rm cybertodo

# View logs
docker logs cybertodo

# Execute commands in container
docker exec -it cybertodo /bin/bash

# Rebuild and restart with compose
docker compose up --build --force-recreate
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