# -*- coding: utf-8 -*-
"""StreamLit.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z0NmQedL93p60Eo5rTnS4bCqun0Yy86I
"""
import streamlit as st
import joblib
from PIL import Image
import pandas as pd
from datetime import datetime
import pickle
import tensorflow as tf
import requests


# Define the URL of the .pkl file on GitHub
github_url = 'https://github.com/udaybhaskar717/Solar-Power-Forecasting-APP/raw/main/stack_reg_1.pkl'

# Retrieve the file contents using requests
response = requests.get(github_url)
file_contents = response.content

# Load the model object from the file contents using pickle
model = pickle.loads(file_contents)

# define a function to make predictions
def predict_solar_power(df):
    # make predictions using the loaded model
    predictions = model.predict(df)
    return predictions

# create a function to get user inputs
def get_user_inputs():
    st.header("Enter the weather data:")
    date = st.date_input("Date", datetime.now().date())
    Ambient_temp = st.number_input("Ambient Temperature (°C)", value=25.0, key="ambient_temp")
    Module_temp = st.number_input("Module Temperature (°C)", value=25.0, key="module_temp")
    Irradiance = st.number_input("Irradiance (W/m^2)", value=1000.0, key="irradiance")
    # wind_speed = st.number_input("Wind Speed (m/s)", value=3.0, key="wind_speed")
    # pressure = st.number_input("Pressure (hPa)", value=1013.0, key="pressure")

    # create a DataFrame with the user inputs
    user_inputs = pd.DataFrame({
        'AMBIENT_TEMPERATURE': [Ambient_temp],
        'MODULE_TEMPERATURE': [Module_temp],
        'IRRADIATION': [Irradiance]
        # 'Wind Speed': [wind_speed],
        # 'Pressure': [pressure]
    })

    # add a new column with the date
    user_inputs['Date'] = pd.to_datetime(date)
    user_inputs.set_index('Date', inplace=True)

    return user_inputs

# create the app
def main():
    st.title("GIL Solar Power Forecasting Tool for Gandikota PV plant")
    # Set header image
    # load image from URL
    url = "https://raw.githubusercontent.com/udaybhaskar717/Solar-Power-Forecasting-APP/main/GIL_Image.png"
    image = Image.open(requests.get(url, stream=True).raw)
# Create a container for the image
    img_container = st.container()
#   # Add the image to the container
    with img_container:
        st.image(image, use_column_width=True)
        st.markdown(
           ''' <style>
            .stApp {
                display: flex;
                flex-direction: column;
            }
            .stApp > div:first-child {
                margin-top: -30px;
                margin-right: 10px;
                align-self: flex-end;
            }
            </style>'''
          ,
            unsafe_allow_html=True
        )

#     st.write("Developed by")
#     st.write("# G R Uday Kumar Reddy (213170007)")
#     st.write("Under the Guidance of")
#     st.write("# Prof. Zakir Hussain Rather")
    user_inputs = get_user_inputs()

    # make predictions
    predictions = predict_solar_power(user_inputs)
    
    if st.button("Forecast"):
        st.subheader("Predicted solar power output:")
        st.write(f"{predictions[0]:.2f} kW")
    st.markdown("---")
    # add author's information
    st.markdown("<br><br><br>", unsafe_allow_html=True) # to add some space
    st.markdown("<p style='font-size:20px;'>Developed by</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:24px; font-weight:bold;'>G R Uday Kumar Reddy (213170007)</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px;'>Under the Guidance of</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:24px; font-weight:bold;'>Prof. Zakir Hussain Rather</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
