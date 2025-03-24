from flask_restful import reqparse

users_parser = reqparse.RequestParser()
users_parser.add_argument("surname", required=True)
users_parser.add_argument("name", required=True)
users_parser.add_argument("age", required=True)
users_parser.add_argument("city_from", required=True)
users_parser.add_argument("position", required=True)
users_parser.add_argument("speciality", required=True)
users_parser.add_argument("address", required=True)
users_parser.add_argument("email", required=True)
users_parser.add_argument("password", required=True)
