import flask
from flask import jsonify

from . import db_session
from .jobs import Jobs

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
                [item.to_dict(only=("job", "leader.id", "work_size", "collaborators", "is_finished"))
                 for item in jobs]
        }
    )