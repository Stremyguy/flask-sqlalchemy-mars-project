import flask
from flask import jsonify, make_response, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    "users_api",
    __name__,
    template_folder="templates"
)

@blueprint.route("/api/users")
def get_users() -> dict:
    session = db_session.create_session()
    users = session.query(User).all()
    
    return jsonify(
        {
            "users":
                [item.to_dict(only=("surname", "name", "age", "position", "speciality",
                                    "address"))
                 for item in users]
        }
    )


@blueprint.route("/api/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id: int) -> dict:
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    
    return jsonify(
        {
            "user": user.to_dict(only=(
                "surname", "name", "age", 
                "position", "speciality", "address"))
        }
    )


@blueprint.route("/api/users", methods=["POST"])
def create_user() -> dict:
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position",
                  "speciality", "address", "email", "password"]):
        return make_response(jsonify({"error": "Bad request"}), 400)
    
    session = db_session.create_session()
    
    user = User(
        email=request.json["email"],
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json["position"],
        speciality=request.json["speciality"],
        address=request.json["address"]
    )
    
    user.set_password(request.json["password"])
    session.add(user)
    session.commit()
    
    return jsonify({"id": user.id})


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id: int) -> dict:
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    
    if not user:
        return make_response(jsonify({"error": "Not found"}))
    
    data = request.json
    
    if "surname" in data:
        user.surname = data["surname"]
    if "name" in data:
        user.name = data["name"]
    if "age" in data:
        user.age = data["age"]
    if "position" in data:
        user.position = data["position"]
    if "speciality" in data:
        user.speciality = data["speciality"]
    if "address" in data:
        user.address = data["address"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.set_password(data["password"])
        
    session.commit()
    
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> dict:
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    
    session.delete(user)
    session.commit()
    
    return jsonify({"success": "OK"})
