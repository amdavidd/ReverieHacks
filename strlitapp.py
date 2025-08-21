#from alzheimers import alzheimers_forest
#from diabetes import diabetes_forest
#from heart import heart_forest
#from hyper import hyper_forest
#from lung import lung_forest

import streamlit as st 
import pandas as pd

from sfunc import run_models, one_hot


# Custom CSS to increase font size of widget labels
st.markdown("""
    <style>
    /* select all input labels */
    div[data-testid="stSlider"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectSlider"] label {
        font-size: 24px !important; /* Increase font size */
        font-weight: bold;
    }
    div[class*="stSlider"] {
        font-size: 16px !important; /* Adjust font size for slider content */
    }
    </style>
""", unsafe_allow_html=True)


def validate_data(data, has_medical_info):
    acceptable_range = [
        (0, 120), #age
        ['Male', 'Female'], #gender
        (0, 20), #pregnancies
        (5, 100), #BMI
        ['< 100 minutes', '100 - 200 minutes', '> 200 minutes'], #Exercise
        (60, 230), #Max Heart Rate
        ['Poor', 'Average', 'Excellent'], #Air Quality
        ['Never', 'Former', 'Current'], #Smoking
        ['Never', 'Occasionally', 'Regularly'], #Drinks
        ['Poor', 'Fair', 'Good'], #Sleep Quality
        ["Yes", "No", "No, but I commonly experience symptoms"], #Depression
        ["No chest pain or discomfort", 
         "Sharp, stabbing, or burning chest discomfort (during rest)", 
         "Unusual chest pressure or mild pain (during activity or rest)", 
         "Heavy or tight chest pain (during activity)"], #Chest Pain
        ['Poor', 'Limited', 'Good'], #Healthcare Access
        (90, 180), #Blood Pressure (sys)
        (0, 200), #Blood Pressure (dia)
        (60, 100), #Heart Rate 
        (0, 1000), #Insulin
        (30, 350), #Glucose
        (0, 1000), #Cholesterol
        ['Up', 'Flat', 'Down'] #ST Slope
    ]
    for i in range(len(data)):
        if data[i] is None:
            st.warning("Please fill in all required fields.")
            return False
        if isinstance(acceptable_range[i], list):
            if data[i] not in acceptable_range[i]:
                st.warning(f"\"{data[i]}\" is not within the valid options: {acceptable_range[i]}.")
                return False
        elif isinstance(acceptable_range[i], tuple):
            if not (acceptable_range[i][0] <= data[i] <= acceptable_range[i][1]):
                st.warning(f"\"{data[i]}\" is not within the valid range: {acceptable_range[i]}.")
                return False
    return True

def write_dataframe(data, has_medical_info):
    if validate_data(data, has_medical_info):
        df = pd.DataFrame(data, columns=["Age", "Gender", "Pregnancies", "BMI", "Exercise Level", "Max Heart Rate",
                                         "Air Quality", "Smokes", "Drinks", "Sleep Quality", "Depression", "Chest Pain", 
                                         "Healthcare Access", 
                                         "Blood Pressure (sys)", "Blood Pressure (dia)", "Heart Rate", 
                                         "Insulin", "Glucose", "Cholesterol", "ST Slope"])
        
        alzheimers_df = df[['Age', 'BMI', 'Sleep Quality', 'Air Quality', 'Exercise Level', 'Drinks',  'Smoking', 'Depression']]
        alzheimers_df['Sleep Quality'] = alzheimers_df['Sleep Quality'].map({'Poor': 0, 'Average': 1, 'Good': 2})
        alzheimers_df['Air Quality'] = alzheimers_df['Air Quality'].map({'Excellent': 0, 'Average': 1, 'Poor': 2})
        alzheimers_df['Exercise Level'] = alzheimers_df['Exercise Level'].map({'< 100 minutes': 0, '100 - 200 minutes': 1, '> 200 minutes': 2})
        alzheimers_df['Drinks'] = alzheimers_df['Drinks'].map({'Never': 0, 'Occasionally': 1, 'Regularly': 2})
        alzheimers_df['Smokes'] = alzheimers_df['Smokes'].map({'Never': 0, 'Former': 1, 'Current': 2})
        alzheimers_df['Depression'] = alzheimers_df['Depression'].map({'No': 0, 'No, but I commonly experience symptoms': 1, 'Yes': 2})
        
        #rename columns
        alzheimers_df.columns = ['Age', 'BMI', 'Sleep Quality', 'Air Pollution Exposure', 'Physical Activity Level', 'Alcohol Consumption',  'Smoking Status', 'Depression Level']
        
        #preview dataset
        print(alzheimers_df.head())

        diabetes_df = df[['Glucose', 'BMI', 'Age', 'Blood Pressure (dia)', 'Pregnancies', 'Insulin']]
        diabetes_df.columns = ['Glucose', 'BMI', 'Age', 'BloodPressure', 'Pregnancies', 'Insulin']
        print(diabetes_df.head())
        
        heart_df = df[['ST Slope', 'Cholesterol', 'Max Heart Rate', 'Age', 'Blood Pressure (dia)', 'Gender', 'Chest Pain']]
        heart_df['ST Slope'] = heart_df['ST Slope'].map({'Up': 2, 'Flat': 1, 'Down': 0})
        heart_df['Gender'] = heart_df['Gender'].map({'Male': 0, 'Female': 1})
        heart_df['Chest Pain'] = heart_df['Chest Pain'].map({'No chest pain or discomfort': 'ASY', 
                                                             'Sharp, stabbing, or burning chest discomfort (during rest)': 'NAP', 
                                                             'Unusual chest pressure or mild pain (during activity or rest)': 'ATA', 
                                                             'Heavy or tight chest pain (during activity)': 'TA'})
        heart_df = one_hot(heart_df, ['Chest Pain'])
        heart_df.columns = ['ST_Slope', 'Cholesterol', 'MaxHR', 'Age', 'RestingBP', 'Sex', 'ChestPainType_ASY', 'ChestPainType_NAP', 'ChestPainType_TA',  'ChestPainType_ATA']
        print(heart_df.head())

        hyper_df = df[['Blood Pressure (sys)', 'Blood Pressure (dia)', 'BMI', 'Age', 'Cholesterol', 'Glucose', 'Heart Rate']]
        hyper_df.columns = ['sysBP', 'diaBP', 'BMI', 'age', 'totChol', 'glucose', 'heartRate']
        print(hyper_df.head())
        
        lung_df = df[['Age', 'Air Quality', 'Healthcare Access', 'Smokes']]
        lung_df['Air Quality'] = lung_df['Air Quality'].map({'Excellent': 0, 'Average': 1, 'Poor': 2})
        lung_df['Healthcare Access'] = lung_df['Healthcare Access'].map({'Poor': 0, 'Limited': 1, 'Good': 2})
        lung_df['Smokes'] = lung_df['Smokes'].map({'Never': 0, 'Former': 1, 'Current': 2})
        lung_df.columns = ['Age', 'Air Pollution Exposure', 'Healthcare Access', 'Smoking Status']
        print(lung_df.head())

        stroke_df = df[['Glucose', 'BMI', 'Age', 'Smokes', 'Gender']]
        stroke_df['Smokes'] = stroke_df['Smokes'].map({'Never': 1, 'Former': 2, 'Current': 3})
        stroke_df['Gender'] = stroke_df['Gender'].map({'Male': 0, 'Female': 1})
        stroke_df.columns = ['avg_glucose_level', 'bmi', 'age', 'smoking_status', 'gender', ]
        print(stroke_df.head())
    
        run_models(alzheimers_df, diabetes_df, heart_df, hyper_df, lung_df, stroke_df)
        return df

def gen_random_data():
    pass

def gen_pregnancy(gender):
    pregnancies = 0
    if gender == "Female":
        pregnancies = int(st.number_input(label = "Number of times pregnant:", min_value = 0, max_value = 10, step = 1, format = "%d", placeholder = "Enter your number of pregnancies here!"))
    return pregnancies

def get_bmi(system, age):
    if system == 'Metric':
        height = st.number_input(
            label="Height (cm):",
            min_value=0.0,
            format="%.1f",  # Use float format to allow decimal input
            placeholder="Enter your height here!"
        )
        weight = st.number_input(
            label="Weight (kg):",
            min_value=0.0,
            format="%.1f",  # Use float format
            placeholder="Enter your weight here!"
        )
        bmi = weight / ((height / 100) ** 2) if height > 0 else 0
    else:  # Imperial
        height = st.number_input(
            label="Height (in):",
            min_value=0.0,
            format="%.1f",  # Use float format
            placeholder="Enter your height here!"
        )
        weight = st.number_input(
            label="Weight (lbs):",
            min_value=0.0,
            format="%.1f",  # Use float format
            placeholder="Enter your weight here!"
        )
        bmi = (weight / 2.20462262185) / ((height * 2.54 / 100) ** 2) if height > 0 else 0
    
    st.write(f'BMI: {bmi:.1f}')  # Display BMI with one decimal place
    return bmi

def get_max_heart_rate(age, gender, exercise):
    max_heart_rate = 0
    if gender == 'Female':
        max_heart_rate = 206 - (0.88 * (age if age is not None else 30)) #standard max hr equation for women
    else:
        max_heart_rate = 220 - (age if age is not None else 30) #standard max hr equation for men

    #adjust to athletes
    fitness_adjustments = {
        '< 100 minutes': 0,
        '100 - 200 minutes': -3,
        '> 200 minutes': -6
    }
    max_heart_rate += fitness_adjustments.get(exercise, 0)
    st.write(f"Max Heart Rate: {max_heart_rate}")
    return max_heart_rate

def get_total_sleep_quality(sleep_time, rested):
    sleep_quality = 0
    

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
    user_age = st.number_input(label = "Age:", min_value = 0, max_value = 120, step = 1, format = "%d", value = None, placeholder = "Enter your age here!")
    if user_age is not None:
        user_age = int(user_age)
    
    user_gender = st.radio(
        "Gender (Biological)",
        ["Male", "Female", ":rainbow[gayyyy]",],
        index = None
    )    
    user_pregnancies = gen_pregnancy(user_gender)
    
    user_bmi = get_bmi(user_system, user_age)
    
    user_exercise = st.select_slider(
        "How much exercise do you get every week?",
        value='100 - 200 minutes',
        options=[
            '< 100 minutes',
            '100 - 200 minutes',
            '> 200 minutes',
        ],
        help="Select a point to rate your exercise quantity."
    )

    user_max_heart_rate = get_max_heart_rate(user_age, user_gender, user_exercise)

    user_air_quality = st.selectbox(
        "How would you rate the air quality in your area?",
        ("Poor", "Average", "Excellent"),
        index=0,
        placeholder="Select air quality...",
    )
        
    user_smoking = st.selectbox(
        "Have you ever been a smoker / lived with a smoker?",
        ("Never", "Formerly", "Currently"),
        index=0,
        placeholder="Select smoking status...",
    )
    
    user_drinks = st.selectbox(
        "How often do you drink alcohol?",
        ("Never", "Occasionally", "Regularly"),
        index=0,
        placeholder="Select alcohol status...",
    )
    
    user_sleep_time = st.slider("How many hours of sleep do you get per night?", 3, 12, (7, 8))
    
    user_rested = st.select_slider(
        "How often would you say you feel well-rested every week?",     
        value="Sometimes (3-4 times)",
        options = ['Almost never (0-1 time(s))',
        'Rarely (1-2 time(s)',
        'Sometimes (3-4 times)',
        'Often (5-6 times)',
        'Always (6-7 times)'],
        help="Select a point to rate your sleep quality."
    )

    user_sleep_quality = get_total_sleep_quality(user_sleep_time, user_rested)

    user_depression = st.radio(
        "Have you been medically diagnosed with depression?",
        ["Yes", "No", "No, but I commonly experience symptoms"],
        index = None
    )
    
    user_chest_pain = st.selectbox(
        "Which of these best explain your chest pain symptoms (if any)?",
        ("No chest pain or discomfort", 
         "Sharp, stabbing, or burning chest discomfort (during rest)", 
         "Unusual chest pressure or mild pain (during activity or rest)", 
         "Heavy or tight chest pain (during activity)"),
        index=0,
        placeholder="Select chest pain type...",
        help="Choose what matches your chest discomfort, or 'No chest pain' if unsure."
    )

    user_healthcare_access = st.selectbox(
        "How would you rate the quality of the healthcare available to you?",
        ('Poor', 'Limited', 'Good'),
        index=0,
        placeholder="Select healthcare access...",
    )

    st.write()
    st.write()
    st.subheader("The additional fields below likely require medically tested information and are thus optional. However, completing them will improve the accuracy.")    
    st.write()
    st.write()

    if not st.button("Omit optional fields"):
        user_blood_pressure = st.text_input("Blood Pressure in mmHg (Systolic/Diastolic)",
                                            value = "120 / 80",  
                                            placeholder="Enter your blood pressure...")
        
        user_blood_pressure = st.text_input("Blood Pressure in mmHg (Systolic/Diastolic)",
                                            value = "120 / 80",  
                                            placeholder="Enter your blood pressure...")

        user_heart_rate = st.text_input("Current Heart Rate (bpm)", 
                                            value = 72, 
                                            placeholder = "Enter your heart rate...")

        user_insulin = st.text_input("Insulin: 2-Hour serum insulin (mu U/ml)", 
                                            value = 79.8, 
                                            placeholder = "Enter your insulin level...")
    
        user_glucose = st.text_input("Plasma glucose concentration a 2 hours in an oral glucose tolerance test",
                                            value = 121, 
                                            placeholder = "Enter your glucose level...")
    
        user_cholesterol = st.text_input("Total serum cholesterol (mg/dl)",
                                            value = 180, 
                                            placeholder = "Enter your cholesterol level...")
    
        user_st_slope = st.selectbox("ST segment slope observed during exercise stress test", 
                                            ("Flat", "Up", "Down"),
                                            index=0,
                                            placeholder="Select ST segment slope...")
        if st.button("Submit"):
            data = [user_age, user_gender, user_pregnancies, user_bmi, user_exercise, user_max_heart_rate, 
            user_air_quality, user_smoking, user_drinks, user_sleep_time, user_sleep_quality, 
            user_depression, user_chest_pain, user_healthcare_access, 
            user_blood_pressure, user_heart_rate, user_insulin, user_glucose, user_cholesterol, 
            user_st_slope]
            write_dataframe(data, True)
            
    #submit button without medical data
    if st.button("Submit"):
        data = [user_age, user_gender, user_pregnancies, user_bmi, user_exercise, user_max_heart_rate, 
            user_air_quality, user_smoking, user_drinks, user_sleep_quality, 
            user_depression, user_chest_pain, user_healthcare_access]
        write_dataframe(data, False)
