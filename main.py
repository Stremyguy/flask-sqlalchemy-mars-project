from flask import Flask, render_template, url_for, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm

app = Flask(__name__)
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


if __name__ == "__main__":
    main()
