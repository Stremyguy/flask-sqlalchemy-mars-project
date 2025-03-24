from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.users import User
from data.resources_parsers import users_parser


def abort_if_user_not_found(user_id: int) -> None:
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    
    if not user:
        abort(404, message=f"User {user_id} is not found")


class UsersResource(Resource):
    def get(self, user_id: int) -> dict:
        abort_if_user_not_found(user_id)
        
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        
        return jsonify({"user": user.to_dict(
            only=("surname", "name", "age", "city_from", 
                  "position", "speciality", "address"))})
    
    def delete(self, user_id: int) -> dict:
        abort_if_user_not_found(user_id)
        
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        
        session.delete(user)
        session.commit()
        
        return jsonify({"success": "OK"})


class UsersListResource(Resource):
    def get(self) -> dict:
        session = db_session.create_session()
        users = session.query(User).all()
        
        return jsonify({"users": [item.to_dict(
            only=("surname", "name", "age", "city_from", 
                  "position", "speciality", "address")) for item in users]})
    
    def post(self) -> dict:
        args = users_parser.parse_args()
        session = db_session.create_session()
        
        user = User(
            email=args["email"],
            surname=args["surname"],
            name=args["name"],
            city_from=args["city_from"],
            age=args["age"],
            position=args["position"],
            speciality=args["speciality"],
            address=args["address"]
        )
        
        user.set_password(args["password"])
        session.add(user)
        session.commit()
        
        return jsonify({"id": user.id})
