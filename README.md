# Crop Recommendation System

An AI-powered web application that recommends the most suitable crops based on environmental conditions and soil properties.

## Features

- Input field conditions (temperature, humidity, pH, water availability, season)
- Interactive sliders for easy parameter adjustment
- Machine learning-based crop recommendations
- Confidence score for each recommendation
- Seasonal information and agricultural insights
- Responsive design for both desktop and mobile devices

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Place your `crop_prediction.csv` file in the root directory
4. Run the application: `python app.py`
5. Open your browser and navigate to `http://localhost:5000`

## How It Works

The system uses a Random Forest classifier trained on agricultural data to predict the most suitable crop based on input parameters. The model considers:

- Temperature (°C)
- Humidity (%)
- Soil pH
- Water availability (mm)
- Season (Rainy, Winter, Summer, Spring)

## File Structure
