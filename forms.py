from flask_wtf import   FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class PredictionForm(FlaskForm):
    """ class for the prediction form """

    serviced = SelectField('serviced', validators=[DataRequired(message='this field is required')], choices=[('Yes'), ('No')])
    newly_built = SelectField('newly built', validators=[DataRequired(message='this field is required')], choices=[('Yes'), ('No')]) 
    furnished = SelectField('furnished', validators=[DataRequired(message='this field is required')], choices=[('Yes'), ('No')])
    bedrooms = IntegerField('number of bedrooms', validators=[DataRequired(message='this field is required')])
    bathrooms = IntegerField('number of bathrooms', validators=[DataRequired(message='this field is required')])
    toilets = IntegerField('number of toilets', validators=[DataRequired(message='this field is required'), \
                           NumberRange(min=0, message='please enter a valid number')])
                                                           
    

class UkPredictionForm(FlaskForm):
    """ class for handling Uk prediction form """

    bedrooms = IntegerField('Number of bedrooms', validators=[DataRequired(message='this field is required'), NumberRange(min=0, message='please enter a valid number')])
