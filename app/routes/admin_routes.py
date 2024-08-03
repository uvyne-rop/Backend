from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Spaces
from sqlalchemy.exc import IntegrityError
from functools import wraps

# Blueprint for admin routes
admin_bp = Blueprint('admin_bp', __name__)

# Decorator to ensure the user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({"message": "Access denied, admin only"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Create a new space
@admin_bp.route('/admin/spaces', methods=['POST'])
@login_required
@admin_required
def create_space():
    data = request.get_json()
    name = data.get('name')
    image_url = data.get('image_url')
    status = data.get('status')
    location = data.get('location')
    description = data.get('description')
    amount = data.get('amount')

    if not name or not description or not location or not amount or not image_url or not status:
        return jsonify({"message": "All fields are required."}), 400

    new_space = Spaces(
        image_url=image_url,
        name=name,
        description=description,
        location=location,
        amount=amount,
        status=status

    )

    db.session.add(new_space)
    db.session.commit()

    return jsonify({"message": "Space created successfully", "space": new_space.to_dict()}), 201

# Get all spaces
@admin_bp.route('/admin/spaces', methods=['GET'])
@login_required
@admin_required
def get_spaces():
    spaces = Spaces.query.all()
    spaces_list = [space.to_dict() for space in spaces]
    return jsonify(spaces_list), 200

# Get a specific space
@admin_bp.route('/admin/spaces/<int:space_id>', methods=['GET'])
@login_required
@admin_required
def get_space(space_id):
    space = Spaces.query.get_or_404(space_id)
    return jsonify(space.to_dict()), 200

# Update a space
@admin_bp.route('/admin/spaces/<int:space_id>', methods=['PUT'])
@login_required
@admin_required
def update_space(space_id):
    data = request.get_json()
    space = Spaces.query.get_or_404(space_id)

    space.image_url = data.get('image_url', space.image_url)
    space.name = data.get('name', space.name)
    space.description = data.get('description', space.description)
    space.location = data.get('location', space.location)
    space.amount = data.get('amount', space.amount)
    space.status = data.get('status', space.status)
    

    db.session.commit()
    
    return jsonify({"message": "Space updated successfully", "space": space.to_dict()}), 200

# Delete a space
@admin_bp.route('/admin/spaces/<int:space_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_space(space_id):
    space = Spaces.query.get_or_404(space_id)
    db.session.delete(space)
    db.session.commit()
    
    return jsonify({"message": "Space deleted successfully"}), 200
