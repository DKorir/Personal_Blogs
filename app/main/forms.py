from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import InputRequired
#update profileform
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')
#quotes form
class QuoteForm(FlaskForm):
    my_quotes = TextAreaField('Enter Quote', validators=[InputRequired()])
    submit = SubmitField('Submit')
#commentform
class CommentForm(FlaskForm):
    comments = TextAreaField('leave your comment below', validators=[InputRequired()])
    submit = SubmitField('Submit')