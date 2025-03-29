from flask import Blueprint, jsonify, request
from controllers.userController import get_all_users, create_user,update_user,delete_user,login_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    user = get_all_users()
    return jsonify(user)
#-----------------------------------------------------------------------------------------------------
@user_bp.route('/post', methods=['POST'])
def user_store():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        if not name or not email:
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        print(f"NAME {name} --- email {email} --- {password}")
        new_user = create_user(name, email,password)
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#-----------------------------------------------------------------------------------------------------
@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        name = data.get('name')
        email = data.get('email')
        
        updated_user = update_user(user_id, name, email)
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------------------------------------------------
@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):
    try:
        result = delete_user(user_id)
        return jsonify(result), result[1] if isinstance(result, tuple) else 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# -----------------------------------------------------------------------------------------------------
@user_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json();
    return login_user(data.get('email'),data.get('password'));
# -----------------------------------------------------------------------------------------------------

