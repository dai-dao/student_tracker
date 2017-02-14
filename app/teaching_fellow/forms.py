from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

class StudentForm(FlaskForm):
    """
    Form for admin to add or edit students
    """
    name = StringField('Student Name', validators=[DataRequired()])
    forum = StringField('Forum', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_description = StringField('Event Description', validators=[DataRequired()])
    event_date = DateTimeField('Event Date', validators=[DataRequired()], default=datetime.now())
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    is_attended = BooleanField('Attended', validators=[DataRequired()])
    TF_comment = TextAreaField('TF Comment', validators=[DataRequired()], render_kw={"rows": 25, "cols": 11})
    submit = SubmitField('Submit')

