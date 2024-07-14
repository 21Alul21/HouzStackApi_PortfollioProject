from flask import Flask, jsonify, request, render_template, flash
import joblib
import pandas as pd 


app = Flask(__name__)

@app.route('/api/nigeria/predict', methods=['POST'], strict_slashes=False)
def predict_nigeria():
    """ view that handles prediction of house rent in Nigeria """

    if request.form:
        # receiving form inputs
        serviced = request.form.get('serviced', None)
        newly_built = request.form.get('newly_built', None) 
        furnished = request.form.get('furnished', None) 
        bedrooms = request.form.get('bedrooms', None) 
        bathrooms = request.form.get('bathroom', None)
        toilets = request.form.get('toilets', None)
      
        # validating input fields
        if not serviced or not newly_built or not furnished or not bedrooms or not bathrooms or not toilets:
            error = 'errors, all input fields must be entered'
            return render_template('predict_nigeria.html', error)
        
        if serviced == 'yes':
            serviced = 1
        else:
            serviced = 0
        
        if newly_built == 'yes':
            newly_built = 1
        else:
            newly_built = 0
        if furnished == 'yes':
            furnished = 1
        else:
            furnished = 0
        
        
        try:
            df = pd.DataFrame({'Serviced': [int(serviced)], 'Newly Built': [int(newly_built)], \
                                'Furnished': [int(furnished)], 'Bedrooms': [int(bedrooms)], 'Bathrooms': [int(bathrooms)], 'Toilets': [int(toilets)]})

            loaded_model = joblib.load('nigeria_model.joblib')
            prediction = loaded_model.predict(df)
            return render_template('success_nigeria.html', prediction, currency='Naira')
        
        except Exception:
            flash('an exception occured, please try again')




    elif request.get_json():
        # receiving json inputs
        serviced = request.json.get('serviced', None)
        newly_built = request.json.get('newly_built', None) 
        furnished = request.json.get('furnished', None) 
        bedrooms = request.json.get('bedrooms', None) 
        bathrooms = request.json.get('bathroom', None)
        toilets = request.json.get('toilets', None)
        if not serviced or not newly_built or not furnished or not bedrooms or not bathrooms or not toilets:
            return jsonify({
                'error': 'all input fields must be entered'
            }), 422
    
        if serviced == 'yes':
            serviced = 1
        else:
            serviced = 0
        
        if newly_built == 'yes':
            newly_built = 1
        else:
            newly_built = 0
        if furnished == 'yes':
            furnished = 1
        else:
            furnished = 0
        
        
        try:
            df = pd.DataFrame({'Serviced': [int(serviced)], 'Newly Built': [int(newly_built)], \
                                'Furnished': [int(furnished)], 'Bedrooms': [int(bedrooms)], 'Bathrooms': [int(bathrooms)], 'Toilets': [int(toilets)]})
            loaded_model = joblib.load('nigeria_model.joblib')
            prediction = loaded_model.predict(df)
            if prediction:
                return jsonify({
                    'success': {
                        'country': 'Nigeria',
                        'currency': 'Naira',
                        'rent': prediction,
                    }

                }), 200
            
        except Exception:
            return jsonify({
                'error': 'an exception occured, please try again'
            }), 400
            

if __name__ == '__main__':
    app.run(debug=True)