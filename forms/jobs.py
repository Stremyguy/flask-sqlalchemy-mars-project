from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class JobsForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    team_leader_id = IntegerField("Team leader ID", validators=[DataRequired(), NumberRange(min=1)])
    duration =  IntegerField("Work Size", validators=[DataRequired(), NumberRange(min=0)])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    hazard_category_id = SelectMultipleField("Hazard category ID", coerce=int)
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField("Submit")
