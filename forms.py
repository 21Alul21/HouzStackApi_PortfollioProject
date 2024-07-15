from flask_wtforms import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PredictionForm(FlaskForm):
    """ class for the prediction form """

    serviced = SelectField('serviced', validators=[DataRequired()])
    newly_built = SelectField('newly built', validators=[DataRequired()]) 
    furnished = SelectField('furnished', validators=[DataRequired()])
    bedrooms = StringField('number of bedrooms', validators=[DataRequired()])
    bathrooms = StringField('number of bathrooms', validators=[DataRequired()])
    toilets = StringField('nuber of toilets', validators=[DataRequired()])
    