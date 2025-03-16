from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class JobsForm(FlaskForm):
    title = StringField("Title of activity", validators=[DataRequired()])
    team_leader_id = IntegerField("Team leader ID", validators=[DataRequired(), NumberRange(min=1)])
    duration =  IntegerField("Duration", validators=[DataRequired(), NumberRange(min=0)])
    collaborators = StringField("List of collaborators", validators=[DataRequired()])
    is_finished = BooleanField("Is finished")
    submit = SubmitField("Submit")
