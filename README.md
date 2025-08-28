# Cyberpunk TODO 2077

A dark-themed, cyberpunk-styled TODO application built with Flask, featuring user authentication, RESTful API with Swagger documentation, and a mobile-responsive interface.

## 🔮 Features

- **User Authentication**: Secure registration and login system
- **Individual TODO Lists**: Each user has their own isolated task list
- **CRUD API**: Complete RESTful API with Swagger documentation
- **Mobile-Ready**: Responsive design using Bulma CSS framework
- **Dark Cyberpunk Theme**: Futuristic interface with neon accents
- **Type Safety**: Full Python typing support
- **PEP8 Compliant**: Professional code standards
- **Docker Ready**: Easy deployment with Docker containers

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- Docker (optional)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd testing_copilot_agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Web Interface: http://localhost:5000
   - API Documentation: http://localhost:5000/api/docs/

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - Web Interface: http://localhost:5000
   - API Documentation: http://localhost:5000/api/docs/

## 🎮 Demo Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📡 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### TODO Operations
- `GET /api/todos` - Get all todos for user
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status
- `GET /api/stats` - Get user statistics

### Documentation
- `GET /api/docs/` - Swagger API documentation

## 🛠 Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **API Documentation**: Flask-RESTX (Swagger)
- **Frontend**: Bulma CSS + FontAwesome
- **Type Checking**: Python typing
- **Containerization**: Docker + Docker Compose

## 🎨 Theme

The application features a cyberpunk aesthetic with:
- Dark color scheme with neon accents
- Futuristic typography and icons
- Animated elements and effects
- Mobile-first responsive design
- Accessibility-compliant color contrast

## 🔐 Security Features

- Password hashing with Werkzeug
- CSRF protection
- SQL injection prevention
- User session management
- Input validation and sanitization

## 🏗 Project Structure

```
.
├── app.py                 # Main Flask application
├── config.py             # Application configuration
├── models.py             # Database models
├── auth.py               # Authentication blueprint
├── api.py                # API blueprint with Swagger
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── 404.html
│   └── 500.html
└── static/             # Static assets
    ├── css/
    │   └── style.css   # Cyberpunk theme
    └── js/
        └── app.js      # Frontend JavaScript
```

## 📱 Mobile Support

The application is fully responsive and optimized for:
- Desktop browsers
- Tablets
- Mobile phones
- Touch interfaces

## 🔄 Future Enhancements

- Real-time notifications
- Task scheduling and reminders
- Collaborative todo lists
- File attachments
- Advanced filtering and search
- Data export functionality
- Progressive Web App (PWA) features

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Welcome to the future of task management. The year is 2077, and your neural TODO list awaits.** 🔮