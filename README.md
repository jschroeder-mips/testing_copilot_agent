# CyberTODO 2077

A cyberpunk-themed TODO application built with Flask, featuring a dark aesthetic inspired by futuristic dystopian themes.

## Features

- ✨ **User Authentication**: Secure login and registration system
- 📱 **Mobile-Ready**: Responsive design with Bulma CSS framework
- 🌙 **Dark Theme**: Cyberpunk-inspired dark theme by default
- 🎨 **Modern UI**: Clean interface with FontAwesome icons
- 🔄 **CRUD Operations**: Create, read, update, and delete TODO items
- 📊 **API Documentation**: Swagger-documented RESTful API
- 🤖 **MCP Server**: Model Context Protocol server for LLM integration
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

## MCP Server for LLM Integration

CyberTODO includes a Model Context Protocol (MCP) server that enables LLMs to manage todos programmatically.

### Starting the MCP Server

```bash
# Start the MCP server
python mcp_server/run_server.py
```

### Available MCP Tools

- **list_todos**: List todos with optional filtering
- **create_todo**: Create new todo items
- **get_todo**: Get specific todo by ID
- **update_todo**: Update existing todos
- **delete_todo**: Delete todos
- **get_user_info**: Get user information

### MCP Configuration Example

```json
{
  "mcpServers": {
    "cybertodo": {
      "command": "python",
      "args": ["/path/to/cybertodo/mcp_server/run_server.py"],
      "env": {
        "MCP_DEFAULT_API_KEY": "cyber-todo-2077-dev-key"
      }
    }
  }
}
```

For detailed MCP server documentation, see [`mcp_server/README.md`](mcp_server/README.md).

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

## Docker Installation & Deployment

CyberTODO 2077 provides comprehensive Docker support for easy deployment and development. The application includes a production-ready Dockerfile and Docker Compose configuration.

### Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose v2.0+ (included with Docker Desktop)

### Quick Start with Docker Compose (Recommended)

The easiest way to run CyberTODO is using Docker Compose:

1. **Clone the repository:**
```bash
git clone https://github.com/jschroeder-mips/testing_copilot_agent.git
cd testing_copilot_agent
```

2. **Start the application:**
```bash
docker compose up -d
```

3. **Access the application:**
   - Open your browser and navigate to `http://localhost:5000`
   - The application will be ready to use with a fresh database

4. **Stop the application:**
```bash
docker compose down
```

### Manual Docker Commands

If you prefer to use Docker directly without Compose:

#### Building the Image

```bash
# Build the Docker image
docker build -t cybertodo:latest .
```

#### Running the Container

```bash
# Run with default settings
docker run -d \
  --name cybertodo \
  -p 5000:5000 \
  cybertodo:latest

# Run with custom configuration
docker run -d \
  --name cybertodo \
  -p 5000:5000 \
  -e FLASK_CONFIG=production \
  -e SECRET_KEY=your-secret-key-here \
  -v cybertodo_data:/app/instance \
  cybertodo:latest
```

### Environment Variables

Configure the application using these environment variables:

| Variable | Description | Default | Examples |
|----------|-------------|---------|----------|
| `FLASK_CONFIG` | Application configuration mode | `production` | `development`, `production`, `testing` |
| `SECRET_KEY` | Flask secret key for sessions | Auto-generated | `your-secure-secret-key` |
| `DATABASE_URL` | Database connection string | `sqlite:///todo_app.db` | `postgresql://user:pass@host:port/db` |

### Data Persistence

#### Using Docker Volumes (Recommended)

```bash
# Create a named volume for data persistence
docker volume create cybertodo_data

# Run with volume mounted
docker run -d \
  --name cybertodo \
  -p 5000:5000 \
  -v cybertodo_data:/app/instance \
  cybertodo:latest
```

#### Using Bind Mounts

```bash
# Create local instance directory
mkdir -p ./instance

# Run with bind mount
docker run -d \
  --name cybertodo \
  -p 5000:5000 \
  -v $(pwd)/instance:/app/instance \
  cybertodo:latest
```

### Production Deployment

For production environments, consider these configurations:

#### Docker Compose with Custom Settings

Create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  cybertodo:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_CONFIG=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - cybertodo_data:/app/instance
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  cybertodo_data:
```

Run with:
```bash
# Set environment variables
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="your-database-url"

# Deploy
docker compose -f docker-compose.prod.yml up -d
```

#### With PostgreSQL Database

For production with PostgreSQL, update your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  cybertodo:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_CONFIG=production
      - SECRET_KEY=your-secret-key-here
      - DATABASE_URL=postgresql://cybertodo:changeme@postgres:5432/cybertodo
    depends_on:
      - postgres
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: cybertodo
      POSTGRES_USER: cybertodo
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Development with Docker

For development with live code reloading:

```bash
# Run in development mode with bind mounts
docker run -it \
  --name cybertodo-dev \
  -p 5000:5000 \
  -v $(pwd):/app \
  -e FLASK_CONFIG=development \
  cybertodo:latest
```

Or create a `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  cybertodo:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_CONFIG=development
    volumes:
      - .:/app
      - /app/instance
    command: ["python", "run.py"]
```

### Container Features

The Docker image includes:

- **Multi-stage build**: Optimized for production with minimal attack surface
- **Non-root user**: Runs as `cybertodo` user for security
- **Health checks**: Built-in health monitoring
- **Dependency management**: Uses uv for fast package installation with pip fallback
- **Signal handling**: Proper shutdown handling
- **Environment flexibility**: Works with SQLite (default) or PostgreSQL

### Troubleshooting

#### Common Issues and Solutions

**1. Container exits immediately:**
```bash
# Check logs
docker logs cybertodo

# Common fix: ensure proper permissions
docker run --user $(id -u):$(id -g) ...
```

**2. Database permission errors:**
```bash
# Fix: Use named volumes instead of bind mounts
docker volume create cybertodo_data
docker run -v cybertodo_data:/app/instance ...
```

**3. Port already in use:**
```bash
# Check what's using the port
sudo netstat -tlnp | grep :5000

# Use different port
docker run -p 8080:5000 cybertodo:latest
```

**4. Build fails with network issues:**
```bash
# Build with network host mode
docker build --network=host -t cybertodo:latest .
```

**5. Container can't connect to database:**
```bash
# Check container logs
docker logs cybertodo

# Verify environment variables
docker inspect cybertodo | grep -A 10 Env
```

### Performance Tuning

For high-traffic production deployments:

```bash
# Run multiple instances behind a load balancer
docker run -d --name cybertodo-1 -p 5001:5000 cybertodo:latest
docker run -d --name cybertodo-2 -p 5002:5000 cybertodo:latest
docker run -d --name cybertodo-3 -p 5003:5000 cybertodo:latest
```

### Monitoring

Set up monitoring with Docker:

```bash
# View real-time logs
docker logs -f cybertodo

# Monitor resource usage
docker stats cybertodo

# Health check status
docker inspect cybertodo | grep -A 5 Health
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