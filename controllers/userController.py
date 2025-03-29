from models.User import User
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token  

def get_all_users():
    try:
        return [user.to_dict() for user in User.query.all()]    
    except Exception as error:
        print(f"ERROR {error}")

# -----------------------------------------------------------------------------------------------------
def create_user(name, email,password):
    try:
        new_user = User(name,email,password)
    
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg' : 'Error al crear usuario'}),500

# -----------------------------------------------------------------------------------------------------
def update_user(user_id, name, email):
    try:
        user = User.query.get(user_id)
        if not user:
            return {"error": "Usuario no encontrado"}, 404

        user.name = name if name else user.name
        user.email = email if email else user.email
        
        db.session.commit()
        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        return {"error": str(e)}, 500

# -----------------------------------------------------------------------------------------------------
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return {"error": "Usuario no encontrado"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}, 200
    except Exception as e:
        print(f"ERROR {e}")
        return {"error": str(e)}, 500

# -----------------------------------------------------------------------------------------------------
def login_user(email, password):
    user = User.query.filter_by(email=email).first();
    if user and user.check_password(password):
            access_token = create_access_token(identity=user.id);
            return jsonify ( {
                'access_token': access_token,
                'user': {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
        })
    return jsonify({"msg":"Credenciales invalidas"}),401