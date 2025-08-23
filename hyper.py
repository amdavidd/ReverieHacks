#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np

from sfunc import run_forest_regressor, one_hot, answer, intensity, quality


# In[ ]:


hyper = pd.read_csv('Datasets/hypertension.csv')


# In[ ]:


pd.set_option('display.max_columns', 100)


# In[ ]:


print(len(hyper))


# In[ ]:


print(hyper.columns)
hyper.head()


# In[ ]:


print(hyper['Risk'].value_counts(normalize=True))


# In[ ]:


hyper.describe()


# In[ ]:


test_forest = run_forest_regressor(hyper, 'Risk')
cleaned_hyper = hyper[['sysBP', 'diaBP', 'BMI', 'age', 'totChol', 'glucose', 'heartRate', 'Risk']]
hyper_forest = run_forest_regressor(cleaned_hyper, 'Risk')
cleaned_hyper_small = hyper[['BMI', 'age', 'Risk']]
hyper_forest_small = run_forest_regressor(cleaned_hyper_small, 'Risk')