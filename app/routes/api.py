"""RESTful API routes with Swagger documentation."""

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_login import login_required, current_user
from app import db
from app.models.todo import Todo, TodoStatus, TodoPriority
from app.models.user import User

api_blueprint = Blueprint('api', __name__)
api = Api(
    api_blueprint,
    version='1.0',
    title='CyberTODO API',
    description='RESTful API for the CyberTODO application',
    doc='/docs/'
)

# Define namespaces
todos_ns = Namespace('todos', description='TODO operations')
users_ns = Namespace('users', description='User operations')

api.add_namespace(todos_ns, path='/todos')
api.add_namespace(users_ns, path='/users')

# API Models for documentation
todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='TODO ID'),
    'title': fields.String(required=True, description='TODO title'),
    'description': fields.String(description='TODO description'),
    'status': fields.String(enum=['pending', 'in_progress', 'completed'], description='TODO status'),
    'priority': fields.String(enum=['low', 'medium', 'high', 'critical'], description='TODO priority'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp'),
    'due_date': fields.DateTime(description='Due date'),
    'user_id': fields.Integer(readonly=True, description='Owner user ID'),
    'is_overdue': fields.Boolean(readonly=True, description='Whether the TODO is overdue')
})

todo_input_model = api.model('TodoInput', {
    'title': fields.String(required=True, description='TODO title'),
    'description': fields.String(description='TODO description'),
    'status': fields.String(enum=['pending', 'in_progress', 'completed'], default='pending'),
    'priority': fields.String(enum=['low', 'medium', 'high', 'critical'], default='medium'),
    'due_date': fields.DateTime(description='Due date (ISO format)')
})

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'username': fields.String(readonly=True, description='Username'),
    'email': fields.String(readonly=True, description='Email address'),
    'created_at': fields.DateTime(readonly=True, description='Account creation timestamp'),
    'todo_count': fields.Integer(readonly=True, description='Number of TODOs')
})


@todos_ns.route('/')
class TodoList(Resource):
    """TODO list operations."""
    
    @todos_ns.doc('list_todos')
    @todos_ns.marshal_list_with(todo_model)
    @login_required
    def get(self):
        """Fetch all TODOs for the current user."""
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = current_user.todos
        
        if status:
            query = query.filter(Todo.status == status)
        if priority:
            query = query.filter(Todo.priority == priority)
        
        todos = query.order_by(Todo.created_at.desc()).all()
        return [todo.to_dict() for todo in todos]
    
    @todos_ns.doc('create_todo')
    @todos_ns.expect(todo_input_model)
    @todos_ns.marshal_with(todo_model, code=201)
    @login_required
    def post(self):
        """Create a new TODO item."""
        data = request.get_json()
        
        if not data or not data.get('title'):
            api.abort(400, 'Title is required')
        
        todo = Todo(
            title=data['title'],
            description=data.get('description'),
            status=TodoStatus(data.get('status', 'pending')),
            priority=TodoPriority(data.get('priority', 'medium')),
            user_id=current_user.id
        )
        
        if data.get('due_date'):
            try:
                todo.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                api.abort(400, 'Invalid due_date format. Use ISO format.')
        
        db.session.add(todo)
        db.session.commit()
        
        return todo.to_dict(), 201


@todos_ns.route('/<int:id>')
@todos_ns.param('id', 'The TODO identifier')
class TodoResource(Resource):
    """Single TODO operations."""
    
    @todos_ns.doc('get_todo')
    @todos_ns.marshal_with(todo_model)
    @login_required
    def get(self, id):
        """Fetch a specific TODO by ID."""
        todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
        if not todo:
            api.abort(404, 'TODO not found')
        return todo.to_dict()
    
    @todos_ns.doc('update_todo')
    @todos_ns.expect(todo_input_model)
    @todos_ns.marshal_with(todo_model)
    @login_required
    def put(self, id):
        """Update a specific TODO."""
        todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
        if not todo:
            api.abort(404, 'TODO not found')
        
        data = request.get_json()
        if not data:
            api.abort(400, 'No data provided')
        
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        
        if 'status' in data:
            todo.status = TodoStatus(data['status'])
        if 'priority' in data:
            todo.priority = TodoPriority(data['priority'])
        
        if data.get('due_date'):
            try:
                todo.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                api.abort(400, 'Invalid due_date format. Use ISO format.')
        
        todo.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return todo.to_dict()
    
    @todos_ns.doc('delete_todo')
    @login_required
    def delete(self, id):
        """Delete a specific TODO."""
        todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
        if not todo:
            api.abort(404, 'TODO not found')
        
        db.session.delete(todo)
        db.session.commit()
        
        return '', 204


@users_ns.route('/profile')
class UserProfile(Resource):
    """Current user profile operations."""
    
    @users_ns.doc('get_profile')
    @users_ns.marshal_with(user_model)
    @login_required
    def get(self):
        """Get current user profile."""
        return current_user.to_dict()