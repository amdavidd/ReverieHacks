#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd 
import numpy as np

from sfunc import run_forest, one_hot, answer, intensity, quality


# In[10]:


import pandas as pd 
import numpy as np

from sfunc import run_forest, one_hot, answer, intensity, quality


# In[11]:


diabetes = pd.read_csv('Datasets/diabetes.csv')


# In[12]:


pd.set_option('display.max_columns', 100)


# In[13]:


print(len(diabetes))


# In[14]:


print(diabetes.columns)
diabetes.head()


# In[15]:


print(diabetes['Outcome'].value_counts(normalize=True))


# In[16]:


diabetes.describe()


# In[17]:


test_forest = run_forest(diabetes, 'Outcome')
cleaned_diabetes = diabetes[['Glucose', 'BMI', 'Age', 'BloodPressure', 'Pregnancies', 'Insulin', 'Outcome']]
diabetes_forest = run_forest(cleaned_diabetes, 'Outcome')

