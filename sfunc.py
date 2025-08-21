from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from alzheimers.py import alzheimers_forest
from diabetes.py import diabetes_forest
from heart.py import heart_forest
from hyper.py import hyper_forest
from lung.py import lung_forest
from stroke.py import stroke_forest

import pandas as pd

def run_forest(df, target_column):
    forest = RandomForestClassifier(n_estimators=100, random_state=3)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 3)

    forest.fit(X_train, y_train)
    
    importance = pd.Series(forest.feature_importances_, index=df.drop(target_column, axis=1).columns)
    print(importance.sort_values(ascending=False))
    
    
    accuracy = forest.score(X_test, y_test)
    prob = forest.predict_proba(X_test)
    print(accuracy)

    scores = cross_val_score(forest, X, y, cv=5, scoring='accuracy')
    print(f"CV Accuracy: {scores.mean()} (+/- {scores.std()})")
    print()
    print(prob[:10])
    
    return forest


#scale data
def scale_data(df, target_column):
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame")
    
    # Separate features and target
    features = df.drop(columns=[target_column])
    target = df[target_column]

    s = StandardScaler()
    
    #transform data
    scaled_data = s.fit_transform(features)
    scaled_df = pd.DataFrame(data = scaled_data, columns = features.columns)
    
    #add target column
    scaled_df[target_column] = target.values
    return scaled_df

intensity = {'Low': 0, 'Medium': 1, 'High': 2}
quality = {'Poor': 0, 'Average': 1, 'Good': 2}
answer = {'No': 0, 'Yes': 1}

def one_hot(df, target_columns):
    missing_cols = [col for col in target_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns {missing_cols} not found in DataFrame")
    df = pd.get_dummies(df, columns=target_columns, prefix=None, prefix_sep=' ', drop_first=False, dtype=int)
    return df

def parse_data(data, has_medical_info):
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
    
        return run_models(alzheimers_df, diabetes_df, heart_df, hyper_df, lung_df, stroke_df)

def run_models(alzheimers_df, diabetes_df, heart_df, hyper_df, lung_df, stroke_df):
    alzheimers_result = alzheimers_forest.predict_proba(alzheimers_df)
    diabetes_result = diabetes_forest.predict_proba(diabetes_df)
    heart_result = heart_forest.predict_proba(heart_df)
    hyper_result = hyper_forest.predict_proba(hyper_df)
    lung_result = lung_forest.predict_proba(lung_df)
    stroke_result = stroke_forest.predict_proba(stroke_df)
    results = [alzheimers_result, diabetes_result, heart_result, hyper_result, lung_result, stroke_result]
    print(results)
    return results