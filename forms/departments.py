from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class DepartmentsForm(FlaskForm):
    title = StringField("Department Title", validators=[DataRequired()])
    chief = IntegerField("Chief ID", validators=[DataRequired(), NumberRange(min=1)])
    members = StringField("Members", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
