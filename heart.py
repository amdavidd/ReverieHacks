#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd 
import numpy as np

from sfunc import run_forest, one_hot, answer, intensity, quality


# In[ ]:


heart = pd.read_csv('Datasets/heart_disease.csv')


# In[ ]:


pd.set_option('display.max_columns', 100)


# In[ ]:


print(len(heart))


# In[ ]:


heart.columns = heart.columns.str.strip()
print(heart.columns)
heart.head()


# In[ ]:


heart['Sex'] = heart['Sex'].map({'M': 0, 'F': 1})
heart['ExerciseAngina'] = heart['ExerciseAngina'].map({'N': 0, 'Y': 1})
heart['ST_Slope'] = heart['ST_Slope'].map({'Up': 2, 'Flat': 1, 'Down': 0})
#one-hot encoding
heart = one_hot(heart, ['ChestPainType', 'RestingECG'])
print(heart)


# In[ ]:


print(heart['HeartDisease'].value_counts(normalize=True))


# In[ ]:


heart.describe()


# In[ ]:


print(heart.corr()['HeartDisease'].sort_values(key = lambda x: x.abs(), ascending = False))


# In[ ]:


test_forest = run_forest(heart, 'HeartDisease')
heart_cleaned = heart[['ST_Slope', 'Cholesterol', 'MaxHR', 'Age', 'RestingBP', 'Sex', 'ChestPainType_ASY', 'ChestPainType_NAP', 'ChestPainType_TA',  'ChestPainType_ATA', 'HeartDisease']]
heart_forest = run_forest(heart_cleaned, 'HeartDisease')
heart_cleaned_small = heart[['MaxHR', 'Age', 'Sex', 'ChestPainType_ASY', 'ChestPainType_NAP', 'ChestPainType_TA',  'ChestPainType_ATA', 'HeartDisease']]
heart_forest_small = run_forest(heart_cleaned_small, 'HeartDisease')
