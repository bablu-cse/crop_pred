from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

app = Flask(__name__)

# -------------------------------
# Load and Train Model
# -------------------------------
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, 'crop_prediction.csv'))

    # Fix column name
    df.rename(columns={'water availability': 'water_availability'}, inplace=True)

    # Normalize season
    df['season'] = df['season'].str.lower()

    season_encoder = LabelEncoder()
    label_encoder = LabelEncoder()

    df['season_encoded'] = season_encoder.fit_transform(df['season'])
    df['label_encoded'] = label_encoder.fit_transform(df['label'])

    X = df[['temperature', 'humidity', 'ph', 'water_availability', 'season_encoded']]
    y = df['label_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, 'model.pkl')
    joblib.dump(season_encoder, 'season_encoder.pkl')
    joblib.dump(label_encoder, 'label_encoder.pkl')

    return model, season_encoder, label_encoder


# Load model
if os.path.exists('model.pkl'):
    model = joblib.load('model.pkl')
    season_encoder = joblib.load('season_encoder.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
else:
    model, season_encoder, label_encoder = load_data()


# -------------------------------
# Routes
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        water = float(data['water_availability'])
        season = data['season'].lower()

        season_encoded = season_encoder.transform([season])[0]

        features = pd.DataFrame([{
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'water_availability': water,
            'season_encoded': season_encoded
        }])

        pred = model.predict(features)[0]
        confidence = np.max(model.predict_proba(features)) * 100

        crop = label_encoder.inverse_transform([pred])[0]

        return jsonify({
            'success': True,
            'crop': crop,
            'confidence': round(confidence, 2)
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'success': False, 'error': str(e)})


@app.route('/roadmap/<path:crop_name>')
def roadmap(crop_name):
    crop_name = crop_name.strip().lower()

    return render_template('roadmap.html', crop_name=crop_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)