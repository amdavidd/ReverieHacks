#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

from sfunc import run_forest, one_hot, answer, intensity, quality


# In[3]:


alzheimers = pd.read_csv('Datasets/alzheimers.csv')


# In[4]:


pd.set_option('display.max_columns', 100)


# In[5]:


print(len(alzheimers))


# In[6]:


alzheimers.columns = alzheimers.columns.str.strip().str.replace('’', '', regex=False)
alzheimers = alzheimers.rename(columns={
    'Genetic Risk Factor (APOE-ε4 allele)': 'Genetic Risk',
    'Urban vs Rural Living': 'Residence Type' 
})
print(alzheimers.columns)
print(alzheimers['Education Level'].value_counts())
alzheimers.head()


# In[7]:

#drop unnecessary columns
alzheimers.drop(['Country', 'Employment Status', 'Marital Status'], axis=1, inplace=True)


# In[8]:

#manual encoding for columns where order preservation is important
intensity = {'Low': 0, 'Medium': 1, 'High': 2}
quality = {'Poor': 0, 'Average': 1, 'Good': 2}
answer = {'No': 0, 'Yes': 1}

#one-hot encoding

print(alzheimers.columns)
alzheimers = one_hot(alzheimers, ['Residence Type'])

alzheimers['Gender'] = alzheimers['Gender'].map({'M': 0, 'F': 1})

alzheimers['Physical Activity Level'] = alzheimers['Physical Activity Level'].map(intensity)
 
alzheimers['Smoking Status'] = alzheimers['Smoking Status'].map({'Never': 0, 'Former': 1, 'Current': 2}) #Other custom encoding maps

alzheimers['Alcohol Consumption'] = alzheimers['Alcohol Consumption'].map({'Never': 0, 'Occasionally': 1, 'Regularly': 2})

alzheimers['Cholesterol Level'] = alzheimers['Cholesterol Level'].map({'Normal': 0, 'High': 1})

alzheimers['Family History of Alzheimers'] = alzheimers['Family History of Alzheimers'].map(answer)

alzheimers['Depression Level'] = alzheimers['Depression Level'].map(intensity)

alzheimers['Sleep Quality'] = alzheimers['Sleep Quality'].map(quality)

alzheimers['Dietary Habits'] = alzheimers['Dietary Habits'].map({'Healthy': 0, 'Average': 1, 'Unhealthy': 2})

alzheimers['Air Pollution Exposure'] = alzheimers['Air Pollution Exposure'].map(intensity)

alzheimers['Genetic Risk'] = alzheimers['Genetic Risk'].map(answer)

alzheimers['Social Engagement Level'] = alzheimers['Social Engagement Level'].map(intensity)

alzheimers['Income Level'] = alzheimers['Income Level'].map(intensity)

alzheimers['Stress Levels'] = alzheimers['Stress Levels'].map(intensity)

#target variables
alzheimers['Alzheimers Diagnosis'] = alzheimers['Alzheimers Diagnosis'].map(answer)
alzheimers['Diabetes'] = alzheimers['Diabetes'].map(answer)
alzheimers['Hypertension'] = alzheimers['Hypertension'].map(answer)


# In[9]:


print(alzheimers['Alzheimers Diagnosis'].value_counts(normalize=True))


# In[11]:


test_forest = run_forest(alzheimers, 'Alzheimers Diagnosis')
cleaned_alzheimers = alzheimers[['Age', 'BMI', 'Sleep Quality', 'Social Engagement Level', 'Physical Activity Level', 'Alcohol Consumption',  'Smoking Status', 'Depression Level', 'Alzheimers Diagnosis']]
alzheimers_forest = run_forest(cleaned_alzheimers, 'Alzheimers Diagnosis')

