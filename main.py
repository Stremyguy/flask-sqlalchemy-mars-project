from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from data.category import Category
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from forms.departments import DepartmentsForm
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
    return session.get(User, user_id)


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
        
        category = session.get(Category, form.hazard_category_id.data)
        
        if category:
            job.categories.append(category)
        
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
    
    session = db_session.create_session()
    form.hazard_category_id.choices = [[c.id, c.name] for c in session.query(Category).all()]
    
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Edit a job"
    param["form"] = form
    
    if request.method == "GET":
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          or_(Jobs.team_leader == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                          ).first()
        if jobs:
            form.title.data = jobs.job
            form.team_leader_id.data = jobs.team_leader
            form.duration.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.hazard_category_id.data = [c.id for c in jobs.categories]
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          or_(Jobs.team_leader == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                          ).first()
        if jobs:
            jobs.job = form.title.data
            jobs.team_leader = form.team_leader_id.data
            jobs.work_size = form.duration.data
            jobs.collaborators = form.collaborators.data
            jobs.categories = session.query(Category).filter(Category.id.in_(form.hazard_category_id.data)).all()
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


@app.route("/departments")
def departments() -> str:
    session = db_session.create_session()
    
    departments = session.query(Departments).all()

    param = {}
    param["title"] = "List of Departments"
    param["css_link"] = url_for("static", filename="css/style.css")
    param["departments"] = departments
    
    return render_template("departments_list.html", **param)


@app.route("/add_department", methods=["GET", "POST"])
@login_required
def add_department() -> str:
    param = {}
    form = DepartmentsForm()
    
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Add a department"
    param["form"] = form
    
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Departments()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        session.add(department)
        session.commit()
        return redirect("/departments")
    return render_template("departments.html", **param)


@app.route("/departments/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id: int) -> str:
    param = {}
    form = DepartmentsForm()
    
    param["css_link"] = url_for("static", filename="css/style.css")
    param["title"] = "Edit a department"
    param["form"] = form
    
    if request.method == "GET":
        session = db_session.create_session()
        departments = session.query(Departments).filter(Departments.id == id,
                                                        or_(Departments.chief == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                                        ).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        departments = session.query(Departments).filter(Departments.id == id,
                                                        or_(Departments.chief == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                                        ).first()
        if departments:
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data
            session.commit()
            return redirect("/departments")
        else:
            abort(404)
    return render_template("departments.html", **param)


@app.route("/delete_department/<int:id>", methods=["GET", "POST"])
@login_required
def delete_department(id: int) -> None:
    session = db_session.create_session()
    departments = session.query(Departments).filter(Departments.id == id,
                                                    or_(Departments.chief == int(current_user.get_id()), int(current_user.get_id()) == 1)
                                                    ).first()
    if departments:
        session.delete(departments)
        session.commit()
    else:
        abort(404)
    return redirect("/departments")


if __name__ == "__main__":
    main()
