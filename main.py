from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm

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
        
        return redirect("/success")
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


@app.route("/addjob", methods=["GET", "POST"])
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


if __name__ == "__main__":
    main()
