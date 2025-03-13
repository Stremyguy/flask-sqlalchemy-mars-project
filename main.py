from flask import Flask, render_template, url_for
from data import db_session
from data.users import User
from data.jobs import Jobs

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


if __name__ == "__main__":
    main()
