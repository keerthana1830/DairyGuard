import streamlit as st
import serial
import joblib
import pandas as pd
import numpy as np

# Load the model and scaler
model = joblib.load('ABCmodel.h5')
scaler = joblib.load('scaler.h5')

# Set up Streamlit interface
st.title("Milk Freshness Prediction")
st.write("This app predicts whether the milk is 'Fresh' or 'Spoiled' based on sensor data from Arduino or manual input.")

# Sidebar for mode selection
st.sidebar.header("Select Mode")
mode = st.sidebar.radio("Mode", options=["Real-Time Data", "Manual Input"])

# Sidebar for Arduino configuration (only shown if Real-Time Data is selected)
if mode == "Real-Time Data":
    st.sidebar.header("Arduino Configuration")
    serial_port = st.sidebar.text_input("Serial Port", value="COM9")
    baud_rate = st.sidebar.number_input("Baud Rate", value=9600)

# Function to read data from Arduino
def read_arduino_data(serial_port, baud_rate):
    try:
        ser = serial.Serial(serial_port, baud_rate)
        line = ser.readline().decode('utf-8').strip()
        data = list(map(float, line.split(',')))
        ser.close()
        return data
    except Exception as e:
        st.error(f"Error reading from Arduino: {e}")
        return None

# Function to predict milk freshness
def predict_milk_freshness(data):
    features = np.array(data).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    return 'Spoiled' if prediction[0] == 1 else 'Fresh'
    #return 'Spoiled' if prediction[0] == 1 else 'Fresh'

# Main loop for prediction
if st.button("Start Prediction"):
    if mode == "Real-Time Data":
        while True:
            data = read_arduino_data(serial_port, baud_rate)
            if data and len(data) == 3:
                st.write(f"Received Data: {data}")
                result = predict_milk_freshness(data)
                st.write(f"Milk Quality: {result}")
            else:
                st.warning("Waiting for valid data from Arduino...")
    elif mode == "Manual Input":
        absorbance = st.number_input("Absorbance", value=-0.7)
        reflectance = st.number_input("Reflectance", value=1.98)
        fluoroscence = st.number_input("Fluoroscence", value=4.46)
        
        data = [absorbance, reflectance, fluoroscence]
        result = predict_milk_freshness(data)
        st.write(f"Milk Quality: {result}")

# Streamlit footer
st.write("Ensure your Arduino is connected and configured correctly when using Real-Time Data mode.")
