from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AddGroupForm(FlaskForm):
    group = StringField('Group', validators=[DataRequired()])
    submit = SubmitField('Add Group')
    
class RemoveGroupForm(FlaskForm):
    group = StringField('Group', validators=[DataRequired()])
    submit = SubmitField('Remove Group')    