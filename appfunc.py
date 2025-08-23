from alzheimers import alzheimers_forest
from diabetes import diabetes_forest, diabetes_forest_small
from heart import heart_forest, heart_forest_small
from hyper import hyper_forest, hyper_forest_small
from lung import lung_forest
from stroke import stroke_forest, stroke_forest_small

import pandas as pd
def parse_data(data, has_medical_info):
    data = [data]
    if has_medical_info:
        df = pd.DataFrame(data, columns=["Age", "Gender", "Pregnancies", "BMI", "Exercise Level", "Max Heart Rate",
                                         "Air Quality", "Smokes", "Drinks", "Sleep Quality", "Depression", "Chest Pain", 
                                         "Healthcare Access", 
                                         "Blood Pressure (sys)", "Blood Pressure (dia)", "Heart Rate", 
                                         "Insulin", "Glucose", "Cholesterol", "ST Slope"])
        
        alzheimers_df = df[['Age', 'BMI', 'Sleep Quality', 'Air Quality', 'Exercise Level', 'Drinks',  'Smokes', 'Depression']]
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
        
        chest_pain_categories = {'No chest pain or discomfort': 'ASY', 
                                'Sharp, stabbing, or burning chest discomfort (during rest)': 'NAP', 
                                'Unusual chest pressure or mild pain (during activity or rest)': 'ATA', 
                                'Heavy or tight chest pain (during activity)': 'TA'}
        #manually replicate one-hot encoding
        for category, column_name in chest_pain_categories.items():
            heart_df[column_name] = 0

        for category, column_name in chest_pain_categories.items():
            heart_df[column_name] = (heart_df['Chest Pain'] == category).astype(int)

        # Drop the original Chest Pain column
        heart_df = heart_df.drop(columns=['Chest Pain'])
        
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

        return [alzheimers_df, diabetes_df, heart_df, hyper_df, lung_df, stroke_df]
    else:
        df = pd.DataFrame(data, columns=["Age", "Gender", "Pregnancies", "BMI", "Exercise Level", "Max Heart Rate",
                                         "Air Quality", "Smokes", "Drinks", "Sleep Quality", "Depression", "Chest Pain", 
                                         "Healthcare Access"])
        alzheimers_df = df[['Age', 'BMI', 'Sleep Quality', 'Air Quality', 'Exercise Level', 'Drinks',  'Smokes', 'Depression']]
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

        diabetes_df = df[['BMI', 'Age', 'Pregnancies']]
        diabetes_df.columns = ['BMI', 'Age', 'Pregnancies']
        print(diabetes_df.head())
        
        heart_df = df[['Max Heart Rate', 'Age', 'Gender', 'Chest Pain']]
        heart_df['Gender'] = heart_df['Gender'].map({'Male': 0, 'Female': 1})
        
        chest_pain_categories = {'No chest pain or discomfort': 'ASY', 
                                'Sharp, stabbing, or burning chest discomfort (during rest)': 'NAP', 
                                'Unusual chest pressure or mild pain (during activity or rest)': 'ATA', 
                                'Heavy or tight chest pain (during activity)': 'TA'}
        #manually replicate one-hot encoding
        for category, column_name in chest_pain_categories.items():
            heart_df[column_name] = 0

        for category, column_name in chest_pain_categories.items():
            heart_df[column_name] = (heart_df['Chest Pain'] == category).astype(int)

        # Drop the original Chest Pain column
        heart_df = heart_df.drop(columns=['Chest Pain'])
        heart_df.columns = ['MaxHR', 'Age', 'Sex', 'ChestPainType_ASY', 'ChestPainType_NAP', 'ChestPainType_TA',  'ChestPainType_ATA']

        hyper_df = df[['BMI', 'Age']]
        hyper_df.columns = ['BMI', 'age']
        print(hyper_df.head())
        
        lung_df = df[['Age', 'Air Quality', 'Healthcare Access', 'Smokes']]
        lung_df['Air Quality'] = lung_df['Air Quality'].map({'Excellent': 0, 'Average': 1, 'Poor': 2})
        lung_df['Healthcare Access'] = lung_df['Healthcare Access'].map({'Poor': 0, 'Limited': 1, 'Good': 2})
        lung_df['Smokes'] = lung_df['Smokes'].map({'Never': 0, 'Former': 1, 'Current': 2})
        lung_df.columns = ['Age', 'Air Pollution Exposure', 'Healthcare Access', 'Smoking Status']
        print(lung_df.head())

        stroke_df = df[['BMI', 'Age', 'Smokes', 'Gender']]
        stroke_df['Smokes'] = stroke_df['Smokes'].map({'Never': 1, 'Former': 2, 'Current': 3})
        stroke_df['Gender'] = stroke_df['Gender'].map({'Male': 0, 'Female': 1})
        stroke_df.columns = ['bmi', 'age', 'smoking_status', 'gender']
        print(stroke_df.head())
        return [alzheimers_df, diabetes_df, heart_df, hyper_df, lung_df, stroke_df] 

def run_models(dataframes, has_medical_info):
    if has_medical_info:
        alzheimers_result = alzheimers_forest.predict_proba(dataframes[0])
        diabetes_result = diabetes_forest.predict_proba(dataframes[1])
        heart_result = heart_forest.predict_proba(dataframes[2])
        hyper_result = hyper_forest.predict(dataframes[3])
        lung_result = lung_forest.predict_proba(dataframes[4])
        stroke_result = stroke_forest.predict(dataframes[5])
        results = [alzheimers_result, diabetes_result, heart_result, hyper_result, lung_result, stroke_result]
    else:
        alzheimers_result = alzheimers_forest.predict_proba(dataframes[0])
        diabetes_result = diabetes_forest_small.predict_proba(dataframes[1])
        heart_result = heart_forest_small.predict_proba(dataframes[2])
        hyper_result = hyper_forest_small.predict(dataframes[3])
        lung_result = lung_forest.predict_proba(dataframes[4])
        stroke_result = stroke_forest_small.predict(dataframes[5])
        results = [alzheimers_result, diabetes_result, heart_result, hyper_result, lung_result, stroke_result]

    dataframe = pd.DataFrame({
        "Alzheimers": results[0][0][1],
        "Diabetes": results[1][0][1],
        "Heart Disease": results[2][0][1],
        "Hypertension": results[3][0],
        "Lung Disease": results[4][0][1],
        "Stroke": results[5][0]
    }, index=[0])
    return dataframe
