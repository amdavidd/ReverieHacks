#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np
from sfunc import run_forest, one_hot, answer, intensity, quality


# In[3]:


lung = pd.read_csv('Datasets/lung_cancer.csv')


# In[4]:

lung = lung.sample(n=100000, random_state=3)
print(len(lung))


# In[5]:


pd.set_option('display.max_columns', 100)


# In[6]:


lung.columns = lung.columns.str.strip().str.replace('_', ' ', regex=False)
print(lung.columns)
lung.head()


# In[7]:


lung.drop(['Country'], axis=1, inplace=True)


# In[8]:


lung.drop(columns = ['Stage at Diagnosis', 'Cancer Type', 'Mutation Type', 'Clinical Trial Access', 'Mortality Risk', 'Mutation Type', 'Language Barrier', 
                  'Mortality Risk', '5 Year Survival Probability', 'Delay in Diagnosis' 
                  ], axis = 1, inplace = True)
print(lung.columns)


# In[9]:


lung = one_hot(lung, ['Rural or Urban'], ' ')

lung['Gender'] = lung['Gender'].map({'Male': 0, 'Female': 1})

lung['Smoking Status'] = lung['Smoking Status'].map({'Non-Smoker': 0, 'Former Smoker': 1, 'Smoker': 2})

lung['Second Hand Smoke'] = lung['Second Hand Smoke'].map(answer)

lung['Air Pollution Exposure'] = lung['Air Pollution Exposure'].map(intensity)

lung['Occupation Exposure'] = lung['Occupation Exposure'].map(answer)

lung['Socioeconomic Status'] = lung['Socioeconomic Status'].map({'Low' : 0, 'Middle': 1, 'High': 2})

lung['Healthcare Access'] = lung['Healthcare Access'].map({'Poor': 0, 'Limited': 1, 'Good': 2})

lung['Insurance Coverage'] = lung['Insurance Coverage'].map(answer)

lung['Screening Availability'] = lung['Screening Availability'].map(answer)

lung['Treatment Access'] = lung['Treatment Access'].map({'Partial': 0, 'Full' : 1})

lung['Indoor Smoke Exposure'] = lung['Indoor Smoke Exposure'].map(answer)

lung['Family History'] = lung['Family History'].map(answer)

lung['Tobacco Marketing Exposure'] = lung['Tobacco Marketing Exposure'].map(answer)
#target variable
lung['Final Prediction'] = lung['Final Prediction'].map(answer)

print(lung.head())


# In[ ]:


print(lung['Final Prediction'].value_counts(normalize=True))


# In[ ]:


lung.describe()


# In[10]:


print(lung.corr()['Final Prediction'].sort_values(key = lambda x: x.abs(), ascending = False))


# In[12]:


test_forest = run_forest(lung, 'Final Prediction')
cleaned_lung = lung[['Age', 'Air Pollution Exposure', 'Healthcare Access', 'Smoking Status', 'Final Prediction']]
lung_forest = run_forest(cleaned_lung, 'Final Prediction')