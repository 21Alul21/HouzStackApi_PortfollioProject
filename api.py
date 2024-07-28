from flask import Flask, jsonify, request, render_template, flash
import joblib
import pandas as pd
import numpy as np
from forms import PredictionForm, UkPredictionForm
import logging
import os
import pickle
from dotenv import load_dotenv


load_dotenv()


# Setup logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/api/v1/nigeria/predict', methods=['POST'], strict_slashes=False)
def predict_nigeria():
    """ view that handles prediction of house rent in Nigeria """

    if request.method == 'POST':
        # handling json data from client side
        if request.get_json():
            # receiving json inputs
            serviced = request.json.get('serviced', None)
            newly_built = request.json.get('newly_built', None)
            furnished = request.json.get('furnished', None)
            bedrooms = request.json.get('bedrooms', None)
            bathrooms = request.json.get('bathrooms', None)
            toilets = request.json.get('toilets', None)

            # validating values
            if serviced is None or newly_built is None or furnished is \
                None or bedrooms is None or bathrooms is None or toilets is None:
                return jsonify({
                    'error': 'all input fields must be entered'
                }), 422

            try:
                bedrooms = int(bedrooms)
                bathrooms = int(bathrooms)
                toilets = int(toilets)
            except ValueError:
                return jsonify({
                    'error': {
                        'fields': ['bedrooms', 'bathrooms', 'toilets'],
                        'message': 'fields must be numbers'
                    }
                }), 422

            # encoding inputs
            if serviced.lower() == 'yes':
                serviced = 1
            else:
                serviced = 0
            
            if newly_built.lower() == 'yes':
                newly_built = 1
            else:
                newly_built = 0
            if furnished.lower() == 'yes':
                furnished = 1
            else:
                furnished = 0

            try:
                df = pd.DataFrame({
                    'Serviced': [serviced],
                    'Newly Built': [newly_built],
                    'Furnished': [furnished],
                    'Bedrooms': [bedrooms],
                    'Bathrooms': [bathrooms],
                    'Toilets': [toilets]
                })

                 # loading the model
                logging.debug("Loading model")
                loaded_model = joblib.load('nigerira.plk')
                logging.debug("Model loaded successfully")
                print(type(loaded_model))
                
                prediction = loaded_model.predict(df)[0]  # Get the first element from the prediction array
                logging.debug(f"Prediction made: {prediction}")

                # formatting the prediction value to be comma seperated
                prediction = f"{prediction:,}"

                
                return jsonify(
                    {'success': {
                        'country': 'Nigeria',
                        'currency': 'Naira',
                        'duration': 'yearly',
                        'rent': int(prediction)
                        }
                    }), 200

            except Exception as e:
                return jsonify({
                    'error': f'an exception occurred, please try again: {e}'
                }), 400

@app.route('/api/vi/uk/predict', methods=['POST'], strict_slashes=False)
def predict_uk():
    """ api view for handling logic for uk rent prediction """

    if request.method == 'POST':
        if request.get_json():

            # receiving input
            room = int(request.json.get('bedrooms'))
            if not room:
                return jsonify({'validation error': 'room field cannot be blank'}), 422
            
            try:
                df = pd.DataFrame({'Number of Rooms': [room]})

                # getting the path of the model
                script_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(script_dir, 'model_uk.plk')
                with open(file_path, 'rb') as m:
                    loaded_model = pickle.load(m)
                #loaded_model = joblib.load('model_uk.plk')
                prediction = loaded_model.predict(df)[0]

                # formatting the prediction value to be comma seperated
                prediction = f"{prediction:,}"
                

                return jsonify(
                    {
                      'success': {
                          'country': 'England',
                          'currency': 'Pounds',
                          'duration': 'monthly',
                          'rent': int(prediction)
                      }
                    
                    }
                ), 200
            
            except Exception as e:
                return jsonify(
                    {
                        'error': f'an exception occured, try again: str{e}'
                    }
                ), 400
            


# views for handling form data from the frontend

@app.route('/form/v1/nigeria/predict', methods=['GET', 'POST'], strict_slashes=False)
def nigeria_form_predict():
    """ method for handling prediction from form data """

    form = PredictionForm()

    # handling form data from client side
    if request.method == 'POST':
        if form.validate_on_submit():

            # collecting validated form data
            serviced = request.form.get('serviced', None)
            newly_built = request.form.get('newly_built', None) 
            furnished = request.form.get('furnished', None) 
            bedrooms = request.form.get('bedrooms', None) 
            bathrooms = request.form.get('bathrooms', None)
            toilets = request.form.get('toilets', None)

           
            # encoding inputs
            if serviced.lower() == 'yes':
                serviced = 1
            else:
                serviced = 0
            
            if newly_built.lower() == 'yes':
                newly_built = 1
            else:
                newly_built = 0
            if furnished.lower() == 'yes':
                furnished = 1
            else:
                furnished = 0

        logging.debug('creating a dataframe') #############
        
        try:
            df = pd.DataFrame({
                    'Serviced': [serviced],
                    'Newly Built': [newly_built],
                    'Furnished': [furnished],
                    'Bedrooms': [int(bedrooms)],
                    'Bathrooms': [int(bathrooms)],
                    'Toilets': [int(toilets)]
                })

           

            
            logging.debug('dataframe created') ############

            loaded_model = joblib.load('nigerira.plk')

            logging.debug('model loaded successfully') ############

            prediction = int(loaded_model.predict(df)[0])
            # formatting the prediction value to be comma seperated
            prediction = f"{prediction:,}"

            logging.debug('model predicted successfully') ############
            currency = 'Naira'
            country = 'Nigeria'

            flash("prediction was successful")
            logging.debug(f'prediction is {prediction}')

            
            return render_template('success.html', prediction=prediction, country=country, currency=currency)
        
        except Exception:
            flash(f'an exception occured, please try again')
    return render_template('Nigeria_predict.html', form=form)


@app.route('/form/v1/england/predict', methods=['POST', 'GET'], strict_slashes=False)
def england_form_predict():
    form = UkPredictionForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            bedroom = request.form.get('bedrooms')
            try:
                df = pd.DataFrame({'Number of Rooms': [int(bedroom)]})
                # getting the path of the model
                script_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(script_dir, 'model_uk.plk')
                with open(file_path, 'rb') as m:
                    loaded_model = pickle.load(m)
                #loaded_model = joblib.load('model_uk.plk')
                prediction = int(loaded_model.predict(df)[0])

                # formatting the prediction value to be comma seperated
                prediction = f"{prediction:,}"

                
               

                flash("prediction was successful")
                return render_template('success.html', prediction=prediction, currency='British Pounds', country='England')
            except Exception as  e:
                flash(f'an exception occured, please try again: {e}')

    return render_template('Uk_predict.html', form=form)
    


@app.route("/success", strict_slashes=False)
def success():
    """ successful reprediction page, for displaying result """

    return render_template('sucess.html')

@app.route("/landing", strict_slashes=False)
def landing():
    """ landing page """

    return render_template('landing.html')

@app.route("/nigeria", strict_slashes=False)
def nigeria():
    """ Nigeria prediction form page """
    form =  PredictionForm()

    return render_template('Nigeria_predict.html', form=form)

@app.route("/uk", strict_slashes=False)
def uk():
    """ England prediction form page"""
    form = UkPredictionForm()

    return render_template('Uk_predict.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)

