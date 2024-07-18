from flask import Flask, jsonify, request, render_template, flash
import joblib
import pandas as pd
from forms import PredictionForm
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config['SECRET_KEY'] = "dfkhferhfiebe;lvieiiui"

@app.route('/api/nigeria/predict', methods=['POST'], strict_slashes=False)
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
            if serviced is None or newly_built is None or furnished is None or bedrooms is None or bathrooms is None or toilets is None:
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

            # encoding
            serviced = 1 if serviced.lower() == 'yes' else 0
            newly_built = 1 if newly_built.lower() == 'yes' else 0
            furnished = 1 if furnished.lower() == 'yes' else 0

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
                loaded_model = joblib.load("./nigeria_model_catboost.plk")
                logging.debug("Model loaded successfully")

                prediction = loaded_model.predict(df)[0]  # Get the first element from the prediction array
                logging.debug(f"Prediction made: {prediction}")

                
                return jsonify({
                    'success': {
                        'country': 'Nigeria',
                        'currency': 'Naira',
                        'rent': prediction,
                    }
                }), 200

            except Exception as e:
                return jsonify({
                    'error': f'an exception occurred, please try again: {e}'
                }), 400


        

@app.route('/form/predict', methods=['GET', 'POST'], strict_slashes=False)
def form_predict():
    """ method for handling prediction from form data """

     # handling form data from client side
    if request.form:
        form = PredictionForm()
        if form.validate_on_submit():
            serviced = request.form.get('serviced', None)
            newly_built = request.form.get('newly_built', None) 
            furnished = request.form.get('furnished', None) 
            bedrooms = request.form.get('bedrooms', None) 
            bathrooms = request.form.get('bathroom', None)
            toilets = request.form.get('toilets', None)
        
            # encoding inputs
            if serviced == 'Yes':
                serviced = 1
            else:
                serviced = 0
            
            if newly_built == 'Yes':
                newly_built = 1
            else:
                newly_built = 0
            if furnished == 'Yes':
                furnished = 1
            else:
                furnished = 0
        
        
        try:
            df = pd.DataFrame({'Serviced': [int(serviced)], 'Newly Built': [int(newly_built)], \
                                'Furnished': [int(furnished)], 'Bedrooms': [int(bedrooms)], 'Bathrooms': [int(bathrooms)], 'Toilets': [int(toilets)]})

            loaded_model = joblib.load('nigeria_model.joblib')
            prediction = loaded_model.predict(df)
            return render_template('success.html', prediction=prediction, currency='Naira')
        
        except Exception:
            flash('an exception occured, please try again')

        return render_template('success.html', prediction=prediction) 
        

    return render_template('Nigeria_predict.html', form=form)



@app.route('/nigeria')
def nigeria():
    form = PredictionForm()
    return render_template('Nigeria_predict.html',   form=form)

@app.route('/uk')
def uk():
    return render_template('Uk_predict.html')



if __name__ == '__main__':
    app.run(debug=True)

