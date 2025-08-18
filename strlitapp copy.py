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

def gen_pregnancy(is_female):
    user_pregnancies = 0
    if user_gender == "Female":
        user_pregnancies = st.number_input(label = "Number of times pregnant:", placeholder = "Enter your number of pregnancies here!")
    return user_pregnancies

def get_random_height_weight(age):
    if age <= 18:  # Teenagers (13-18 years)
        meanA, stdA = 150 + (age - 12) * 3, 8 
        meanW, stdW = 47 + (age - 12) * 3, 3  # Slower weight gain, puberty variation
    else:  # Adults (19+ years)
        meanA, stdA = 170, 10  # Average adult height
        meanW, stdW = 70, 10  # Average adult weight ~70kg
    height, weight = round(random.gauss(meanA, stdA), 0), round(random.gauss(meanW, stdW), 0)
    print(height, weight)
    return height, weight

def get_bmi(system, randomize, user_age):
    if system == 'Metric':
        if randomize:
            height, weight = get_random_height_weight(user_age)
            user_height = st.number_input(label = "Height(cm):", value = height, format = "%d", placeholder = "Enter your height here!")
            user_weight = st.number_input(label = "Weight(kg):", value = weight, format = "%d", placeholder = "Enter your weight here!")
        else: 
            user_height = st.number_input(label = "Height(cm):", format = "%d", placeholder = "Enter your height here!")
            user_weight = st.number_input(label = "Weight(kg):", format = "%d", placeholder = "Enter your weight here!")
            
        user_bmi = user_weight / ((user_height / 100) ** 2)
    else:
        if randomize:
            #get random height and weight, convert to imperial
            height, weight = get_random_height_weight(user_age)
            height /= 2.54
            weight *= 2.20462262185
            user_height = st.number_input(label = "Height(in):", value = height, format = "%d", placeholder = "Enter your height here!")
            user_weight = st.number_input(label = "Weight(lbs):", value = weight, format = "%d", placeholder = "Enter your weight here!")
        else:
            user_height = st.number_input(label = "Height(in):", format = "%d", placeholder = "Enter your height here!")
            user_weight = st.number_input(label = "Weight(lbs):", format = "%d", placeholder = "Enter your weight here!")
            
        user_bmi = (user_weight / 2.20462262185) / ((user_height * 2.54 / 100) ** 2)
    
    st.write('BMI: ', user_bmi)
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
    user_age = st.number_input(label = "Age:", value = random.randint(12, 100), format = "%d", placeholder = "Enter your age here!")
    user_gender = st.radio(
        "Gender (Biological)",
        ["Male", "Female", ":rainbow[gayyyy]",],
        index = int(random.randrange(1, 5) / 2)
    )
    user_pregnancies = gen_pregnancy(user_gender)

    user_bmi = get_bmi(user_system, True, user_age)

else:
    user_age = st.number_input(label = "Age:", format = "%d", placeholder = "Enter your age here!")
    user_gender = st.radio(
        "Gender (Biological)",
        ["Male", "Female", ":rainbow[gayyyy]",],
        index = None
    )    
    user_pregnancies = gen_pregnancy(user_gender)
    
    user_bmi = get_bmi(user_system, False, user_age)
    
    
st.markdown("Optional (improves accuracy, but likely requires medically tested information)")