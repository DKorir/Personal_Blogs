from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,FileField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed
#update profileform
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    picture=FileField('Upload picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Submit')
#quotes form
class QuoteForm(FlaskForm):
    my_quotes = TextAreaField('Enter Quote', validators=[InputRequired()])
    submit = SubmitField('Submit')
#commentform
class CommentForm(FlaskForm):
    username=StringField('username', validators=[InputRequired()])
    comments = TextAreaField('leave your comment below', validators=[InputRequired()])
    submit = SubmitField('Submit')