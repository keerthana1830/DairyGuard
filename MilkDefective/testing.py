import serial
import joblib
import pandas as pd
import warnings
#from tensorflow.keras.models import load_model
warnings.filterwarnings('ignore')
# Load the model
model =joblib.load('ABCmodel.h5')

# Setup Serial Communication
serial_port = 'COM9'  # Update with your Arduino port
baud_rate = 9600
ser = serial.Serial(serial_port,baud_rate)

# Load the scaler
scaler = joblib.load('scaler.h5')

def predict_milk_freshness(data):
    # Convert data to the appropriate format
    features = pd.DataFrame([data], columns=['Absorbance', 'Reflectance', 'Fluoroscence'])
    
    # Preprocess features (apply the same scaling used during training)
    features_scaled = scaler.transform(features)

    # Predict using the loaded model
    prediction = model.predict(features_scaled)
    return 'Spoiled' if prediction[0] == 1 else 'Fresh'

while True:
    if ser.in_waiting > 0:
        # Read a line from the serial monitor
        line = ser.readline().decode('utf-8').strip()
        
        # Convert the line into a list of float numbers
        data = list(map(float, line.split(',')))
        print(data)
        # Ensure the data has 3 features (Absorbance, Reflectance, Fluorescence)
        if len(data) == 3:
            # Predict milk freshness
            result = predict_milk_freshness(data)
            
            # Print the prediction result
            print(f"Milk Quality: {result}")