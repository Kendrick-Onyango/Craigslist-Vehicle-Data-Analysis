#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns


# In[2]:


df = pd.read_csv('D:/Python Things/LUX_Academy/craigslist_vehicles.csv')
df.head()


# Columns in the dataframe

# In[3]:


df.columns


# Convert 'posting_date' to datetime data type

# In[4]:


df['posting_date'] = pd.to_datetime(df['posting_date'],  utc=True)


# Preview rows from dataframe

# In[5]:


df.head()


# ### Check how many NaN Values Exist

# In[6]:


df.isnull().sum()


# ### Handle Missing values by filling numeric with mean and categorical with mode

# In[7]:


def handle_missing_values(df):
    numerical_columns = ['year', 'odometer']
    df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].mean())
    
    categorical_columns = ['manufacturer', 'model', 'condition', 'cylinders', 'fuel', 'title_status',
                           'transmission', 'drive', 'size', 'type', 'paint_color', 'posting_date']
    df[categorical_columns] = df[categorical_columns].apply(lambda x: x.fillna(x.mode().iloc[0]))
    return df
df = handle_missing_values(df)


# Aggregate data based on 'posting_date','region,' and 'type' of vehicle, to be able to do further analysis lik temporal patterns, seasonal trends, and demand-supply dynamics.

# In[8]:


def convert_to_tz_aware(posting_date):
    if not posting_date.tzinfo:
        return posting_date.replace(tzinfo=pytz.utc)
    else:
        return posting_date
df['posting_date'] = df['posting_date'].apply(convert_to_tz_aware)
df_agg = df.groupby(['region', 'type', 'posting_date']).size().reset_index(name='count')
df_agg = df_agg.sort_values(by='posting_date')
print(df_agg.head())


# In[9]:


df.info()


# In total, we have 426,880 rows and 28 columns. We’ll start our exploration by seeing how many cities there are in the dataset and how much data we have on each city. A quick way to visualize this is using a histogram which we’ll create using the matplotlib library

# In[10]:


fig, ax = plt.subplots(1,1,figsize=(18,5))
# plot histogram
fig = ax.hist(df['state'],rwidth=0.7,bins=30)
# set title and labels
fig = ax.set_title('Craigslist Used Vehicles (State)')
fig = ax.set_xlabel('State')
fig = ax.set_ylabel('Vehicle Counts')


# Time series frequency graph.

# In[11]:


df_freq = df_agg.groupby(pd.Grouper(key='posting_date', freq='D')).sum().reset_index()

fig_freq = go.Figure(data=go.Bar(
    x=df_freq['posting_date'],
    y=df_freq['count'],
    marker_color='royalblue',
    opacity=0.8
))

fig_freq.update_layout(
    title='Time Frequency Graph: Number of Vehicle Listings per Day',
    xaxis_title='Posting Date',
    yaxis_title='Number of Vehicle Listings',
    xaxis_tickangle=-45,
)
fig_freq.show()


# Interactive time series chart.

# In[12]:


fig = px.line(df_agg, x='posting_date', y='count', color='region', line_group='type',
              title='Number of Available Vehicles Over Time by Region and Vehicle Type',
              labels={'count': 'Number of Vehicles'})
fig.update_layout(
    xaxis_title='Posting Date',
    yaxis_title='Number of Vehicles',
    hovermode='x',
    showlegend=True,
)
fig.show()

