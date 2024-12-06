import pickle
import pandas as pd
from flask import Flask, request, render_template

# Flask app initialization
app = Flask(__name__)

# Load and initialize the model
MODEL_PATH = '../models/model.pkl'

try:
    with open(MODEL_PATH, 'rb') as file:
        diabetes_model = pickle.load(file)
    print("Model successfully loaded.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    diabetes_model = None
except Exception as e:
    print(f"An unexpected error occurred while loading the model: {e}")
    diabetes_model = None

# Mapping prediction outputs to user-friendly labels
PREDICTION_LABELS = {
    0: "Not diabetic",
    1: "Diabetic"
}

@app.route('/', methods=['GET', 'POST'])
def predict_diabetes():
    prediction_label = None  # Initialize the result variable
    
    if request.method == 'POST':
        try:
            # Collect input values from the form
            form_data = {
                'Glucose': request.form.get('glucose'),
                'Insulin': request.form.get('insulin'),
                'BMI': request.form.get('bmi'),
                'Age': request.form.get('age')
            }

            # Log received form data for debugging
            print(f"Form input data: {form_data}")

            # Validate and convert form inputs
            input_features = {key: float(value) for key, value in form_data.items() if value.strip()}
            if len(input_features) != 4:
                raise ValueError("All fields are required and must be numeric.")

            # Create a DataFrame for prediction
            input_df = pd.DataFrame([input_features])

            # Log the DataFrame for debugging
            print(f"Data prepared for prediction:\n{input_df}")

            # Ensure the model is loaded
            if diabetes_model is None:
                raise RuntimeError("The prediction model is unavailable. Please check the server setup.")

            # Make a prediction
            prediction = diabetes_model.predict(input_df)[0]
            prediction_label = PREDICTION_LABELS.get(prediction, "Unknown outcome")

        except ValueError as ve:
            # Handle invalid inputs
            print(f"Input validation error: {ve}")
            return render_template('index.html', prediction=f"Error: {ve}")
        except Exception as e:
            # Catch other unexpected errors
            print(f"Error during prediction: {e}")
            return render_template('index.html', prediction="An error occurred during processing.")

    # Render the template with the prediction result
    return render_template('index.html', prediction=prediction_label)

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
