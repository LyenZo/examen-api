import re
from models.User import User
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token  

# -----------------------------------------------------------------------------------------------------
def validar_email(email):
    """Validación simple de email."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validar_contraseña(password):
    """Verifica la complejidad de la contraseña (por ejemplo, al menos 8 caracteres)."""
    return len(password) >= 8

# -----------------------------------------------------------------------------------------------------
def obtener_todos_usuarios():
    try:
        return [user.to_dict() for user in User.query.all()]    
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener usuarios'}), 500

# -----------------------------------------------------------------------------------------------------
def crear_usuario(name, email, password):
    try:
        # Validar email
        if not validar_email(email):
            return jsonify({'msg': 'Email inválido'}), 400
        
        # Verificar si el email ya está registrado
        usuario_existente = User.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({'msg': 'El email ya está registrado'}), 400
        
        # Validar contraseña
        if not validar_contraseña(password):
            return jsonify({'msg': 'La contraseña debe tener al menos 8 caracteres'}), 400
        
        nuevo_usuario = User(name, email, password)
    
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return nuevo_usuario.to_dict(), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear usuario'}), 500

# -----------------------------------------------------------------------------------------------------
def actualizar_usuario(user_id, name, email):
    try:
        usuario = User.query.get(user_id)
        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        # Validar formato del email
        if email and not validar_email(email):
            return {"error": "Email inválido"}, 400

        usuario.name = name if name else usuario.name
        usuario.email = email if email else usuario.email
        
        db.session.commit()
        return usuario.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        return {"error": str(e)}, 500

# -----------------------------------------------------------------------------------------------------
def eliminar_usuario(user_id):
    try:
        usuario = User.query.get(user_id)
        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        db.session.delete(usuario)
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}, 200
    except Exception as e:
        print(f"ERROR {e}")
        return {"error": str(e)}, 500

# -----------------------------------------------------------------------------------------------------
def iniciar_sesion(email, password):
    try:
        # Validar formato del email
        if not validar_email(email):
            return jsonify({"msg": "Email inválido"}), 400

        usuario = User.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            access_token = create_access_token(identity=usuario.id)
            return jsonify({
                'access_token': access_token,
                'user': {
                    "id": usuario.id,
                    "name": usuario.name,
                    "email": usuario.email
                }
            })
        return jsonify({"msg": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({"msg": "Error al intentar iniciar sesión"}), 500
