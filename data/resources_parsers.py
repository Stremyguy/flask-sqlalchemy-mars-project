from flask_restful import reqparse

# Users parser
users_parser = reqparse.RequestParser()
users_parser.add_argument("surname", required=True)
users_parser.add_argument("name", required=True)
users_parser.add_argument("age", required=True, type=int)
users_parser.add_argument("city_from", required=True)
users_parser.add_argument("position", required=True)
users_parser.add_argument("speciality", required=True)
users_parser.add_argument("address", required=True)
users_parser.add_argument("email", required=True)
users_parser.add_argument("password", required=True)

# Jobs parser
jobs_parser = reqparse.RequestParser()
jobs_parser.add_argument("job", required=True)
jobs_parser.add_argument("team_leader_id", required=True, type=int)
jobs_parser.add_argument("work_size", required=True, type=int)
jobs_parser.add_argument("collaborators", required=True)
jobs_parser.add_argument("categories", required=True, action="append")
jobs_parser.add_argument("is_finished", required=True, type=bool)
