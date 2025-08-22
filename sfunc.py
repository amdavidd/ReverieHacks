from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler



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

def one_hot(df, target_columns, sep='_'):
    missing_cols = [col for col in target_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns {missing_cols} not found in DataFrame")
    df = pd.get_dummies(df, columns=target_columns, prefix=None, prefix_sep=sep, drop_first=False, dtype=int)
    return df