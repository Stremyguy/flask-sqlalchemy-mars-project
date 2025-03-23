import flask
from flask import jsonify, make_response, request

from . import db_session
from .jobs import Jobs
from .category import Category

blueprint = flask.Blueprint(
    "jobs_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/jobs")
def get_jobs() -> dict:
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    
    return jsonify(
        {
            "jobs":
                [item.to_dict(only=(
                    "job", "leader.id", "work_size", "collaborators", "is_finished"))
                 for item in jobs]
        }
    )


@blueprint.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_one_job(job_id: int) -> dict:
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    
    if not jobs:
        return make_response(jsonify({"error": "Not found"}), 404)    
    return jsonify(
        {
            "jobs": jobs.to_dict(only=(
                "job", "leader.id", "work_size", "collaborators", "is_finished"))
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])
def create_job() -> dict:
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(key in request.json for key in
                 ["job", "team_leader_id", "work_size", "collaborators", "categories", "is_finished"]):
        return make_response(jsonify({"error": "Bad request"}), 400)
    
    session = db_session.create_session()

    job = Jobs(
        job=request.json["job"],
        team_leader=request.json["team_leader_id"],
        work_size=request.json["work_size"],
        collaborators=request.json["collaborators"],
        is_finished=request.json["is_finished"]
    )
    
    categories = session.query(Category).filter(Category.id.in_(request.json["categories"])).all()
    job.categories = categories
    
    session.add(job)
    session.commit()
    
    return jsonify({"id": job.id})


@blueprint.route("/api/jobs/<int:job_id>", methods=["PUT"])
def edit_job(job_id: int) -> dict:
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    
    if not job:
        return make_response(jsonify({"error": "Not found"}))
    
    data = request.json
    
    if "job" in data:
        job.job = data["job"]
    if "team_leader_id" in data:
        job.team_leader = data["team_leader_id"]
    if "work_size" in data:
        job.work_size = data["work_size"]
    if "collaborators" in data:
        job.collaborators = data["collaborators"]
    if "categories" in data:
        job.categories = session.query(Category).filter(Category.id.in_(data["categories"])).all()
    if "is_finished" in data:
        job.is_finished = data["is_finished"]
        
    session.commit()
    
    return jsonify({"success": "OK"})


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id: int) -> dict:
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    
    if not job:
        return make_response(jsonify({"error": "Not found"}), 404)
    
    session.delete(job)
    session.commit()
    
    return jsonify({"success": "OK"})