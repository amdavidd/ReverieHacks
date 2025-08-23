#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np

from sfunc import run_forest_regressor, one_hot, answer, intensity, quality


# In[28]:


stroke = pd.read_csv('Datasets/stroke.csv')


# In[29]:


pd.set_option('display.max_columns', 100)


# In[30]:


print(len(stroke))
stroke = stroke[:1000]

# In[31]:


stroke.columns = stroke.columns.str.strip()
print(stroke.columns)
stroke.head()


# In[33]:


#drop unnecessary columns
stroke.drop(['id'], axis=1, inplace=True)


# In[35]:


stroke = one_hot(stroke, ['Residence_type', 'work_type'])

stroke['gender'] = stroke['gender'].map({'Male': 0, 'Female': 1})
stroke['ever_married'] = stroke['ever_married'].map({'Yes': 0, 'No': 1})
stroke['smoking_status'] = stroke['smoking_status'].map({'Unknown': 0, 'never smoked': 1, 'formerly smoked': 2, 'smokes': 3})


# In[ ]:


print(stroke['stroke'].value_counts(normalize=True))


# In[ ]:


stroke.describe()


# In[36]:


print(stroke.corr()['stroke'].sort_values(key = lambda x: x.abs(), ascending = False))


# In[39]:


test_forest = run_forest_regressor(stroke, 'stroke')
stroke_cleaned = stroke[['avg_glucose_level', 'bmi', 'age', 'smoking_status', 'gender', 'stroke']]
stroke_forest = run_forest_regressor(stroke_cleaned, 'stroke')
stroke_cleaned_small = stroke[['bmi', 'age', 'smoking_status', 'gender', 'stroke']]
stroke_forest_small = run_forest_regressor(stroke_cleaned_small, 'stroke')
