"""API blueprint for CRUD operations with Swagger documentation."""
from datetime import datetime
from typing import List, Dict, Any, Optional
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_restx import Api, Resource, fields, Namespace
from models import db, Todo, User

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize Flask-RESTX
api = Api(
    api_bp,
    title='Cyberpunk TODO API',
    version='2.0',
    description='A cyberpunk-themed TODO application API with full CRUD operations',
    doc='/docs/',
    theme='cyberpunk'
)

# Create namespace
todo_ns = Namespace('todos', description='TODO operations', path='/')
api.add_namespace(todo_ns)

# Define models for Swagger documentation
todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='Todo unique identifier'),
    'title': fields.String(required=True, description='Todo title', max_length=200),
    'description': fields.String(description='Todo description'),
    'completed': fields.Boolean(description='Todo completion status', default=False),
    'priority': fields.String(description='Todo priority level', 
                             enum=['low', 'medium', 'high', 'critical'], default='medium'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp'),
    'due_date': fields.DateTime(description='Due date for the todo'),
    'user_id': fields.Integer(readonly=True, description='Owner user ID')
})

todo_input_model = api.model('TodoInput', {
    'title': fields.String(required=True, description='Todo title', max_length=200),
    'description': fields.String(description='Todo description'),
    'priority': fields.String(description='Todo priority level', 
                             enum=['low', 'medium', 'high', 'critical'], default='medium'),
    'due_date': fields.String(description='Due date in ISO format (YYYY-MM-DDTHH:MM:SS)')
})

todo_update_model = api.model('TodoUpdate', {
    'title': fields.String(description='Todo title', max_length=200),
    'description': fields.String(description='Todo description'),
    'completed': fields.Boolean(description='Todo completion status'),
    'priority': fields.String(description='Todo priority level', 
                             enum=['low', 'medium', 'high', 'critical']),
    'due_date': fields.String(description='Due date in ISO format (YYYY-MM-DDTHH:MM:SS)')
})

error_model = api.model('Error', {
    'message': fields.String(description='Error message'),
    'code': fields.Integer(description='Error code')
})


def require_auth() -> Optional[Dict[str, Any]]:
    """Check if user is authenticated."""
    if not current_user.is_authenticated:
        return {'message': 'Authentication required', 'code': 401}, 401
    return None


@todo_ns.route('/todos')
class TodoListAPI(Resource):
    """API for getting all todos and creating new ones."""
    
    @todo_ns.doc('get_todos')
    @todo_ns.marshal_list_with(todo_model)
    @todo_ns.response(401, 'Authentication required', error_model)
    def get(self) -> List[Dict[str, Any]]:
        """Get all todos for the current user."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        # Get query parameters
        completed = request.args.get('completed')
        priority = request.args.get('priority')
        
        # Start with user's todos
        query = Todo.query.filter_by(user_id=current_user.id)
        
        # Apply filters
        if completed is not None:
            completed_bool = completed.lower() == 'true'
            query = query.filter_by(completed=completed_bool)
        
        if priority:
            query = query.filter_by(priority=priority)
        
        # Order by creation date (newest first)
        todos = query.order_by(Todo.created_at.desc()).all()
        
        return [todo.to_dict() for todo in todos]
    
    @todo_ns.doc('create_todo')
    @todo_ns.expect(todo_input_model)
    @todo_ns.marshal_with(todo_model, code=201)
    @todo_ns.response(400, 'Invalid input', error_model)
    @todo_ns.response(401, 'Authentication required', error_model)
    def post(self) -> Dict[str, Any]:
        """Create a new todo."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        data = request.get_json()
        
        if not data or not data.get('title'):
            return {'message': 'Title is required', 'code': 400}, 400
        
        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return {'message': 'Invalid due_date format. Use ISO format.', 'code': 400}, 400
        
        todo = Todo(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=due_date,
            user_id=current_user.id
        )
        
        try:
            db.session.add(todo)
            db.session.commit()
            return todo.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to create todo', 'code': 500}, 500


@todo_ns.route('/todos/<int:todo_id>')
class TodoAPI(Resource):
    """API for individual todo operations."""
    
    def _get_user_todo(self, todo_id: int) -> Optional[Todo]:
        """Get todo belonging to current user."""
        return Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    
    @todo_ns.doc('get_todo')
    @todo_ns.marshal_with(todo_model)
    @todo_ns.response(401, 'Authentication required', error_model)
    @todo_ns.response(404, 'Todo not found', error_model)
    def get(self, todo_id: int) -> Dict[str, Any]:
        """Get a specific todo."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        todo = self._get_user_todo(todo_id)
        if not todo:
            return {'message': 'Todo not found', 'code': 404}, 404
        
        return todo.to_dict()
    
    @todo_ns.doc('update_todo')
    @todo_ns.expect(todo_update_model)
    @todo_ns.marshal_with(todo_model)
    @todo_ns.response(400, 'Invalid input', error_model)
    @todo_ns.response(401, 'Authentication required', error_model)
    @todo_ns.response(404, 'Todo not found', error_model)
    def put(self, todo_id: int) -> Dict[str, Any]:
        """Update a specific todo."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        todo = self._get_user_todo(todo_id)
        if not todo:
            return {'message': 'Todo not found', 'code': 404}, 404
        
        data = request.get_json()
        if not data:
            return {'message': 'No data provided', 'code': 400}, 400
        
        # Parse due_date if provided
        due_date = None
        if 'due_date' in data and data['due_date']:
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return {'message': 'Invalid due_date format. Use ISO format.', 'code': 400}, 400
        
        # Update fields
        if 'title' in data:
            todo.title = data['title']
        if 'description' in data:
            todo.description = data['description']
        if 'completed' in data:
            todo.completed = data['completed']
        if 'priority' in data:
            todo.priority = data['priority']
        if 'due_date' in data:
            todo.due_date = due_date
        
        todo.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return todo.to_dict()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to update todo', 'code': 500}, 500
    
    @todo_ns.doc('delete_todo')
    @todo_ns.response(204, 'Todo deleted successfully')
    @todo_ns.response(401, 'Authentication required', error_model)
    @todo_ns.response(404, 'Todo not found', error_model)
    def delete(self, todo_id: int) -> tuple:
        """Delete a specific todo."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        todo = self._get_user_todo(todo_id)
        if not todo:
            return {'message': 'Todo not found', 'code': 404}, 404
        
        try:
            db.session.delete(todo)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to delete todo', 'code': 500}, 500


@todo_ns.route('/todos/<int:todo_id>/toggle')
class TodoToggleAPI(Resource):
    """API for toggling todo completion status."""
    
    @todo_ns.doc('toggle_todo')
    @todo_ns.marshal_with(todo_model)
    @todo_ns.response(401, 'Authentication required', error_model)
    @todo_ns.response(404, 'Todo not found', error_model)
    def patch(self, todo_id: int) -> Dict[str, Any]:
        """Toggle the completion status of a todo."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        if not todo:
            return {'message': 'Todo not found', 'code': 404}, 404
        
        todo.toggle_completed()
        
        try:
            db.session.commit()
            return todo.to_dict()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to toggle todo', 'code': 500}, 500


@todo_ns.route('/stats')
class TodoStatsAPI(Resource):
    """API for todo statistics."""
    
    @todo_ns.doc('get_stats')
    @todo_ns.response(401, 'Authentication required', error_model)
    def get(self) -> Dict[str, Any]:
        """Get todo statistics for the current user."""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        total_todos = Todo.query.filter_by(user_id=current_user.id).count()
        completed_todos = Todo.query.filter_by(user_id=current_user.id, completed=True).count()
        pending_todos = total_todos - completed_todos
        
        # Priority breakdown
        priority_stats = {}
        for priority in ['low', 'medium', 'high', 'critical']:
            priority_stats[priority] = Todo.query.filter_by(
                user_id=current_user.id, 
                priority=priority,
                completed=False
            ).count()
        
        return {
            'total': total_todos,
            'completed': completed_todos,
            'pending': pending_todos,
            'completion_rate': round((completed_todos / total_todos * 100) if total_todos > 0 else 0, 2),
            'priority_breakdown': priority_stats
        }