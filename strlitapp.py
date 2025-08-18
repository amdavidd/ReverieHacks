#from alzheimers import alzheimers_forest
#from diabetes import diabetes_forest
#from heart import heart_forest
#from hyper import hyper_forest
#from lung import lung_forest

import streamlit as st 
import random

def validate_data():
    pass
def write_dataframe():
    pass

def gen_random_data():
    pass

def gen_pregnancy(user_gender):
    user_pregnancies = 0
    if user_gender == "Female":
        user_pregnancies = int(st.number_input(label = "Number of times pregnant:", min_value = 0, max_value = 10, step = 1, format = "%d", placeholder = "Enter your number of pregnancies here!"))
    return user_pregnancies

def get_bmi(system, user_age):
    if system == 'Metric':
        user_height = st.number_input(
            label="Height (cm):",
            min_value=0.0,
            format="%.1f",  # Use float format to allow decimal input
            placeholder="Enter your height here!"
        )
        user_weight = st.number_input(
            label="Weight (kg):",
            min_value=0.0,
            format="%.1f",  # Use float format
            placeholder="Enter your weight here!"
        )
        user_bmi = user_weight / ((user_height / 100) ** 2) if user_height > 0 else 0
    else:  # Imperial
        user_height = st.number_input(
            label="Height (in):",
            min_value=0.0,
            format="%.1f",  # Use float format
            placeholder="Enter your height here!"
        )
        user_weight = st.number_input(
            label="Weight (lbs):",
            min_value=0.0,
            format="%.1f",  # Use float format
            placeholder="Enter your weight here!"
        )
        user_bmi = (user_weight / 2.20462262185) / ((user_height * 2.54 / 100) ** 2) if user_height > 0 else 0
    
    st.write(f'BMI: {user_bmi:.1f}')  # Display BMI with one decimal place
    return user_bmi

st.set_page_config(
    page_title="Chronic Illnesses Prediction",
    page_icon="",
    layout="wide"
)

st.title("Chronic Illnesses Prediction")

st.subheader("Fill out the brief form below to get a risk assessment! ")

st.subheader("Or, generate a random entry:")

use_random = st.button("Random")

user_system = st.radio(
    "Measuring System",
    ["Metric", "Imperial"],
    captions = ["cm, kg", "in, lb"],
    index = 0
    )

if use_random:
    gen_random_data()
else:
    user_age = int(st.number_input(label = "Age:", min_value = 0, max_value = 120, step = 1, format = "%d", placeholder = "Enter your age here!"))
    user_gender = st.radio(
        "Gender (Biological)",
        ["Male", "Female", ":rainbow[gayyyy]",],
        index = None
    )    
    user_pregnancies = gen_pregnancy(user_gender)
    
    user_bmi = get_bmi(user_system, user_age)
    
    
st.markdown("Optional (improves accuracy, but likely requires medically tested information)")