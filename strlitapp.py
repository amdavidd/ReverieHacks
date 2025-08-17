from alzheimers import alzheimers_forest
from diabetes import diabetes_forest
from heart import heart_forest
from hyper import hyper_forest
from lung import lung_forest

import streamlit as st 

st.set_page_config(
    page_title="Chronic Illnesses Prediction",
    page_icon="",
    layout="wide"
)

st.title("Chronic Illnesses Prediction")