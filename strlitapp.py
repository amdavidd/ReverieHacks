import streamlit as st 
import pandas as pd
import plotly.express as px

from appfunc import parse_data, run_models

# Custom CSS to increase font size of widget labels
st.markdown("""
    <style>
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
    .main { background-color: #f5f7fa; padding: 20px; border-radius: 10px; }
    .stDataFrame { border: 2px solid #4a90e2; border-radius: 8px; }
    .high-risk { background-color: #ff4d4d; color: white; font-weight: bold; }
    .low-risk { background-color: #4caf50; color: white; }
    h1, h2, h3 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'omit_medical' not in st.session_state:
    st.session_state.omit_medical = True
if 'results_df' not in st.session_state:
    st.session_state.results_df = None  
    
def validate_data(data, has_medical_info):
    acceptable_range = [
        (0, 120), #age
        ['Male', 'Female'], #gender
        (0, 20), #pregnancies
        (5, 100), #BMI
        ['< 100 minutes', '100 - 200 minutes', '> 200 minutes'], #Exercise
        (60, 230), #Max Heart Rate
        ['Poor', 'Average', 'Excellent'], #Air Quality
        ['Never', 'Formerly', 'Currently'], #Smoking
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
    st.write(data)
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

def gen_pregnancy(gender):
    pregnancies = 0
    if gender == "Female":
        pregnancies = int(st.number_input(label = "Number of times pregnant:", step = 1, format = "%d", placeholder = "Enter your number of pregnancies here!"))
    return pregnancies

def get_bmi(system, age):
    if system == 'Metric':
        height = st.number_input(
            label="Height (cm):",
            min_value=0,
            value=170,
            max_value=250,
            format="%d",  # Use integer format
            placeholder="Enter your height here!"
        )
        weight = st.number_input(
            label="Weight (kg):",
            min_value=0,
            value=70,
            max_value=500,
            format="%d",  # Use integer format
            placeholder="Enter your weight here!"
        )
        bmi = weight / ((height / 100) ** 2) if height > 0 else 0
    else:  # Imperial
        height = st.number_input(
            label="Height (in):",
            min_value=0,
            value=67,
            max_value=100,
            format="%d",  # Use integer format
            placeholder="Enter your height here!"
        )
        weight = st.number_input(
            label="Weight (lbs):",
            min_value=0,
            value=150,
            max_value=1000,
            format="%d",  # Use integer format
            placeholder="Enter your weight here!"
        )
        bmi = (weight / 2.20462262185) / ((height * 2.54 / 100) ** 2) if height > 0 else 0
    bmi = float(f"{bmi:.1f}")
    st.write(f'BMI: {bmi}')  # Display BMI with one decimal place
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
    average_sleep_time = (sleep_time[0] + sleep_time[1]) / 2
    total_score = 0
    if 7 <= average_sleep_time <= 9:
        total_score += 2
    elif 6 <= average_sleep_time < 7 or 9 < average_sleep_time <= 10:
        total_score += 1
    else:
        total_score += 0    
    
    rested_category_map = {
        'Almost never (0-1 time(s))': 0,
        'Rarely (1-2 time(s))': 0,
        'Sometimes (3-4 times)': 1,
        'Often (5-6 times)': 2,
        'Always (6-7 times)': 2,
    }
    
    total_score += rested_category_map[rested]
    
    if total_score >= 3:
        sleep_rank = "Good"
    elif total_score == 2:
        sleep_rank = "Fair"
    else:
        sleep_rank = "Poor"
    return sleep_rank
    
st.set_page_config(
    page_title="Chronic Illnesses Prediction",
    page_icon="",
    layout="wide"
)

st.title("Chronic Illnesses Prediction")

st.subheader("Fill out the brief form below to get a risk assessment! ")

st.link_button("See project documentation", "https://www.google.com")

user_system = st.radio(
    "Measuring System",
    ["Metric", "Imperial"],
    captions = ["cm, kg", "in, lb"],
    index = 0
    )

user_age = st.number_input(label = "Age:", min_value = 0, max_value = 120, value = 45, step = 1, format = "%d", placeholder = "Enter your age here!")
if user_age is not None:
    user_age = int(user_age)

user_gender = st.radio(
    "Gender (Biological)",
    ["Male", "Female"],
    index = 0
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
    options=['Almost never (0-1 time(s))',
    'Rarely (1-2 time(s))',
    'Sometimes (3-4 times)',
    'Often (5-6 times)',
    'Always (6-7 times)'],
    help="Select a point to rate your sleep quality."
)

user_sleep_quality = get_total_sleep_quality(user_sleep_time, user_rested)

user_depression = st.radio(
    "Have you been medically diagnosed with depression?",
    ["Yes", "No", "No, but I commonly experience symptoms"],
    index = 1
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

# Handle "Toggle optional fields" button
if st.button("Toggle optional fields"):
    st.session_state.omit_medical = not st.session_state.omit_medical

if not st.session_state.omit_medical:
    user_blood_pressure = st.text_input("Blood Pressure in mmHg (Systolic/Diastolic)",
                                        value = "120/80",  
                                        placeholder="Enter your blood pressure...")
    user_blood_pressure_list = user_blood_pressure.split('/')
    user_systolic_blood_pressure = int(user_blood_pressure_list[0].strip())
    user_diastolic_blood_pressure = int(user_blood_pressure_list[1].strip())

    user_heart_rate = st.number_input("Current Heart Rate (bpm)",
                                        value = 72, 
                                        placeholder = "Enter your heart rate...")

    user_insulin = st.number_input("Insulin: 2-Hour serum insulin (mu U/ml)", 
                                        value = 79.8, 
                                        placeholder = "Enter your insulin level...")

    user_glucose = st.number_input("Plasma glucose concentration a 2 hours in an oral glucose tolerance test",
                                        value = 121, 
                                        placeholder = "Enter your glucose level...")

    user_cholesterol = st.number_input("Total serum cholesterol (mg/dl)",
                                        value = 180, 
                                        placeholder = "Enter your cholesterol level...")

    user_st_slope = st.selectbox("ST segment slope observed during exercise stress test", 
                                        ("Flat", "Up", "Down"),
                                        index=0,
                                        placeholder="Select ST segment slope...")
    if st.button("Submit with medical data"):
        data = [user_age, user_gender, user_pregnancies, user_bmi, user_exercise, user_max_heart_rate, 
        user_air_quality, user_smoking, user_drinks, user_sleep_quality, 
        user_depression, user_chest_pain, user_healthcare_access, 
        user_systolic_blood_pressure, user_diastolic_blood_pressure, user_heart_rate, user_insulin, 
        user_glucose, user_cholesterol, user_st_slope]
        if validate_data(data, True):
            st.success("Data submitted successfully!")
            results = parse_data(data, True)
            results_df = run_models(results, True)
            st.session_state.results_df = results_df
else:
    st.write("Optional fields omitted.")

    #submit button without medical data
    if st.button("Submit without medical data"):
        data = [user_age, user_gender, user_pregnancies, user_bmi, user_exercise, user_max_heart_rate, 
            user_air_quality, user_smoking, user_drinks, user_sleep_quality, 
            user_depression, user_chest_pain, user_healthcare_access]
        if validate_data(data, False):
            st.success("Data submitted successfully!")
            results = parse_data(data, False)
            results_df = run_models(results, False)
            st.session_state.results_df = results_df            

def highlight_risk(val):
    if isinstance(val, (int, float)):
        if val < 0.3:
            return 'background-color: #4caf50; color: white'
        elif val < 0.65:
            return 'background-color: #ffcc00; color: black'
        else:
            return 'background-color: #ff4d4d; color: white'
    return ''

if st.session_state.results_df is not None:
    results_df = st.session_state.results_df
    # Display styled DataFrame
    st.subheader("Risk Probabilities")
    st.dataframe(
        results_df.style.format("{:.3f}").applymap(highlight_risk, subset=results_df.columns),
        use_container_width=True
    )

    #Display Bar chart
    st.subheader("Risk Distribution")
    fig = px.bar(
        x=results_df.columns,
        y=results_df.iloc[0],
        color=results_df.iloc[0],
        color_continuous_scale=px.colors.sequential.Plasma,
        opacity=0.8
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="#1e1e1e",  
        paper_bgcolor="#1e1e1e", 
        font_color="#ffffff", 
        title_font_color="#ffffff", 
        xaxis_gridcolor="rgba(255, 255, 255, 0.2)",  
        yaxis_gridcolor="rgba(255, 255, 255, 0.2)", 
        xaxis_title_font_color="#ffffff",
        yaxis_title_font_color="#ffffff"
    )
    fig.update_traces(
        marker_line_color="#ffffff", 
        marker_line_width=1.5  
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretation**: 
    - Values > 0.65 (red): higher risks --- consult a healthcare professional.
    - Values > 0.35 (yellow): moderate risks --- consider lifestyle changes.
    - Values ≤ 0.5 (green): lower risks --- maintain healthy habits.
    """)

    # Download results
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="health_risk_results.csv",
        mime="text/csv"
    )
else:
    pass