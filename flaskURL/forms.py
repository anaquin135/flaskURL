from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class formURL(FlaskForm):
    site = StringField('Site URL', validators=[DataRequired()])
    keyword = StringField('Label Keyword', validators=[Length(max=35)])
    submit = SubmitField('Submit')