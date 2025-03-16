from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from sqlalchemy import or_

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


def main() -> None:
    db_session.global_init("db/mars_explorer.db")
    app.run()
    

@app.route("/")
def index() -> str:
    session = db_session.create_session()
    
    actions = session.query(Jobs).all()

    param = {}
    param["css_link"] = url_for("static", filename="css/style.css")
    param["actions"] = actions
    
    return render_template("works_log.html", **param)


@app.route("/success")
def success() -> str:
    param = {}
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Success!"
    
    return render_template("success.html", **param)


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    form = RegisterForm()
    
    param = {}
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Registration"
    
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template("register.html", title="Registration",
                                   form=form,
                                   message="Passwords do not match")
        
        session = db_session.create_session()
        
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title="Registration",
                                   form=form,
                                   message="This user already exists")
        
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        
        return redirect("/login")
    return render_template("register.html", **param, form=form)


@login_manager.user_loader
def load_user(user_id: int) -> None:
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    param = {}
    form = LoginForm()
    
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Registration"
    param["form"] = form
    
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               message="Incorrect email or password",
                               form=form)
    return render_template("login.html", **param)


@app.route("/logout")
@login_required
def logout() -> None:
    logout_user()
    return redirect("/")


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job() -> str:
    param = {}
    form = JobsForm()
    
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Add a job"
    param["form"] = form
    
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.team_leader_id.data
        job.work_size = form.duration.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        session.add(job)
        session.commit()
        return redirect("/")
    return render_template("jobs.html", **param)


@app.route("/jobs/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id: int) -> str:
    param = {}
    form = JobsForm()
    
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Edit a job"
    param["form"] = form
    
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          or_(Jobs.team_leader == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                          ).first()
        if jobs:
            form.title.data = jobs.job
            form.team_leader_id.data = jobs.team_leader
            form.duration.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          or_(Jobs.team_leader == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                          ).first()
        if jobs:
            jobs.job = form.title.data
            jobs.team_leader = form.team_leader_id.data
            jobs.work_size = form.duration.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            session.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("jobs.html", **param)


@app.route("/delete_job/<int:id>", methods=["GET", "POST"])
@login_required
def delete_job(id: int) -> None:
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id,
                                          or_(Jobs.team_leader == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                          ).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect("/")


if __name__ == "__main__":
    main()
