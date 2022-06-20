#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 18:39:47 2022

@author: yifan
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from urllib.request import urlopen
import json

st.set_page_config(layout="wide")

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

# data for display
df_age = load_data('processed_data/demo_age.csv')
df_gender = load_data('processed_data/demo_gender.csv')
df_race = load_data('processed_data/demo_race.csv')

df_zip = pd.read_csv(
    '/Users/yifan/Documents/Github/yifanhu-2/poverty_illinois_streamlit/raw_data/uszips.csv',
    usecols=["zip", 'city', 'state_id', 'county_name']
)
df_zip = df_zip[df_zip['state_id'] == 'IL']


#######################
# pie charts
#######################

# add filters
zipcode_input = st.sidebar.number_input('Enter a zipcode of interest (e.g., 61820):', value=61820)

# add location
city = df_zip[df_zip['zip'] == zipcode_input]['city'].values[0]
county = df_zip[df_zip['zip'] == zipcode_input]['county_name'].values[0]
f'This area (zipcode: {zipcode_input}) is located in {city}, {county} County.'

# add charts
dff_age = df_age[df_age['Zipcode'] == zipcode_input]
dff_gender = df_gender[df_gender['Zipcode'] == zipcode_input]
dff_race = df_race[df_race['Zipcode'] == zipcode_input]

with st.spinner('Loading...'):
    fig_age = px.pie(dff_age, values='Estimate', names='Age group', title=f'Age ({zipcode_input})')
    fig_age.update_traces(textposition='inside')
    fig_age.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        legend_x=0,
        legend_y=1,
        )
    st.plotly_chart(fig_age, use_container_width=True)

with st.spinner('Loading...'):
    fig_gender = px.pie(dff_gender, values='Estimate', names='Gender', title=f'Gender ({zipcode_input})')
    fig_gender.update_traces(textposition='inside')
    fig_gender.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        legend_x=0,
        legend_y=1,
        )
    st.plotly_chart(fig_gender, use_container_width=True)

with st.spinner('Loading...'):
    fig_race = px.pie(dff_race, values='Estimate', names='Race group', title=f'Race/ethnicity ({zipcode_input})')
    fig_race.update_traces(textposition='inside')
    fig_race.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        legend_x=0,
        legend_y=0,
        legend=dict(orientation='h')
        )
    st.plotly_chart(fig_race, use_container_width=True)