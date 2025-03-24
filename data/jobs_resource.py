from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.jobs import Jobs
from data.category import Category
from data.resources_parsers import jobs_parser


def abort_if_jobs_not_found(job_id: int) -> None:
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    
    if not job:
        abort(404, message=f"Job {job_id} is not found")
    

class JobsResource(Resource):
    def get(self, job_id: int) -> dict:
        abort_if_jobs_not_found(job_id)
        
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        
        return jsonify({"job": job.to_dict(
            only=("job", "leader.id", "work_size", "collaborators", "is_finished"))})

    def delete(self, job_id: int) -> dict:
        abort_if_jobs_not_found(job_id)
                
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        
        session.delete(job)
        session.commit()
        
        return jsonify({"success": "OK"})


class JobsListResource(Resource):
    def get(self) -> dict:
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        
        return jsonify({"jobs": [item.to_dict(
            only=("job", "leader.id", "work_size",
                  "collaborators", "is_finished")) for item in jobs]})
    
    def post(self) -> dict:
        args = jobs_parser.parse_args()
        session = db_session.create_session()
        
        job = Jobs(
            job=args["job"],
            team_leader=args["team_leader_id"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            is_finished=args["is_finished"]
        )
        
        categories = session.query(Category).filter(Category.id.in_(args["categories"])).all()
        job.categories = categories
        
        session.add(job)
        session.commit()
        
        return jsonify({"id": job.id})
