"""Main Flask application for the Cyberpunk TODO app."""
import os
from typing import Optional
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import db, User, Todo
from auth import auth
from api import api_bp
from config import config


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access your TODO list.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        """Load user for Flask-Login."""
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(api_bp)
    
    # Main routes
    @app.route('/')
    @login_required
    def index() -> str:
        """Main application page."""
        todos = current_user.get_todos()
        pending_todos = current_user.get_pending_todos()
        completed_todos = current_user.get_completed_todos()
        
        stats = {
            'total': len(todos),
            'pending': len(pending_todos),
            'completed': len(completed_todos),
            'completion_rate': round((len(completed_todos) / len(todos) * 100) if todos else 0, 1)
        }
        
        return render_template('index.html', 
                             todos=todos, 
                             pending_todos=pending_todos,
                             completed_todos=completed_todos,
                             stats=stats)
    
    @app.route('/health')
    def health() -> dict:
        """Health check endpoint."""
        return {'status': 'online', 'message': 'Cyberpunk TODO App is running'}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error) -> tuple:
        """Handle 404 errors."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error) -> tuple:
        """Handle 500 errors."""
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("📊 Database tables created")
        
        # Create default admin user if it doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@cyberpunk-todo.com',
                password='admin123'
            )
            db.session.add(admin_user)
            db.session.flush()  # This assigns the ID without committing
            
            # Create some sample todos
            sample_todos = [
                Todo(
                    title='Hack the Gibson',
                    description='Break into the mainframe and retrieve the data',
                    priority='critical',
                    user_id=admin_user.id
                ),
                Todo(
                    title='Upgrade neural implants',
                    description='Visit the ripperdoc for cybernetic enhancements',
                    priority='high',
                    user_id=admin_user.id
                ),
                Todo(
                    title='Meet with fixer',
                    description='Discuss new job opportunities in Night City',
                    priority='medium',
                    user_id=admin_user.id
                ),
                Todo(
                    title='Buy new ICE breaker',
                    description='Get better software for netrunning',
                    priority='low',
                    user_id=admin_user.id
                )
            ]
            
            for todo in sample_todos:
                db.session.add(todo)
            
            try:
                db.session.commit()
                print("✅ Default admin user and sample todos created")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error creating default data: {e}")
        else:
            print("👤 Admin user already exists")
    
    return app


# Create the main blueprint for non-auth routes
main = Flask(__name__)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)