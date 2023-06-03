from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class BookForm(FlaskForm):
    schoolID = StringField(label = "SchoolID", validators = [DataRequired(message = "SchoolID is a required field.")])

    userID = StringField(label = "UserID", validators = [DataRequired(message = "UserID is a required field.")])

    bookID = StringField(label = "BookID", validators = [DataRequired(message = "BookID is a required field.")])

    submit = SubmitField("Create")