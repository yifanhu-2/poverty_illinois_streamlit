#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:08:47 2022

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

with urlopen('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json') as response:
    zipcodes = json.load(response)

# data for display
df_race = load_data('processed_data/poverty_RACE AND HISPANIC OR LATINO ORIGIN.csv')
df_race = df_race[df_race['Stats'] == 'Estimate'].loc[df_race['Zipcode'] != 'Illinois', ~df_race.columns.isin(['Below poverty level','Stats'])] 


#######################
# choropleth map
#######################

# add filters
with st.sidebar.form(key = 'choropleth-params'):
        race_filter = st.selectbox(
            'Select a race/ethnic group of interest:',
            (df_race['RACE AND HISPANIC OR LATINO ORIGIN'].unique())
        )

        pop_thresh = st.number_input(
            "Set a population threshold in the selected group (e.g., 10000):",
            value=10000
        )

        pct_thresh = st.number_input(
            'Set a threshold on percent below poverty level (e.g., 11.6):',
            value=11.6
        )

        submit_button = st.form_submit_button('Submit')

if submit_button:
    
    st.write('Showing zipcodes where the population for *', race_filter, '* is greater than ', pop_thresh, ', while more than ', pct_thresh, '% of this population are below poverty level:' )

    # filter data for display
    dff = df_race.loc[(df_race['RACE AND HISPANIC OR LATINO ORIGIN'] == race_filter) & (df_race['Total'] >= pop_thresh) & (df_race['Percent below poverty level'] >= pct_thresh), :]
    dff = dff.rename(columns={'RACE AND HISPANIC OR LATINO ORIGIN': 'Race/ethnicity', 'Total': 'Population'})

    with st.spinner('Loading...'):
        # plot choropleth
        fig = px.choropleth(dff, 
                            geojson=zipcodes, locations='Zipcode', 
                            featureidkey='properties.ZCTA5CE10',
                            color='Percent below poverty level',
                            color_continuous_scale="Viridis",
                            range_color=(df_race['Percent below poverty level'].min(), df_race['Percent below poverty level'].max()),
                            scope="usa",
                            labels={'Percent below poverty level':'Percent below poverty level'},
                            hover_data=['Population', 'Percent below poverty level'],
                            height=500
                            )
        fig.update_geos(fitbounds="locations")
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            )
        st.plotly_chart(fig, use_container_width=True)


