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
    df = pd.read_csv(path, index_col=0)
    return df

with urlopen('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json') as response:
    zipcodes = json.load(response)

# data for display
df_race = load_data('processed_data/poverty_RACE AND HISPANIC OR LATINO ORIGIN.csv')
df_race = df_race[df_race['Stats'] == 'Estimate'].loc[df_race['Zipcode'] != 'Illinois', ~df_race.columns.isin(['Below poverty level','Stats'])] 

df_pop = load_data('processed_data/poverty_POPULATION.csv')
df_pop = df_pop[df_pop['Stats'] == 'Estimate'].loc[df_pop['Zipcode'] != 'Illinois', ~df_pop.columns.isin(['Below poverty level','Stats'])]

#######################
# choropleth map
#######################

# add filters
with st.sidebar.form(key = 'choropleth-params'):
        
        pop_thresh = st.number_input(
            "Set a population threshold (e.g., 10000) for the entire zipcode area:",
            value=10000
        )

        pct_thresh = st.number_input(
            'Set a threshold on percent below poverty level (e.g., 11.6) for the entire zipcode area:',
            value=11.6
        )

        race_filter = st.selectbox(
            'Select a race/ethnic group of interest:',
            (df_race['RACE AND HISPANIC OR LATINO ORIGIN'].unique())
        )
       
        submit_button = st.form_submit_button('Submit')

if submit_button:
    
    st.write('Showing zipcodes with a total population greater than ', pop_thresh, ', and a poverty level greater than ', pct_thresh, '%.' )
    st.write('Hover over the map to view poverty statistics for the race/ethnic group of interest: ', race_filter, '.')

    # filter data for display
    dff_pop = df_pop.loc[(df_pop['Total'] >= pop_thresh) & (df_pop['Percent below poverty level'] >= pct_thresh), :]
    dff_pop = dff_pop.rename(columns={
        'Total': 'Total population',
        'Percent below poverty level': 'Total % below poverty level'
    })

    dff_race = df_race.loc[(df_race['Zipcode'].isin(dff_pop['Zipcode'])) & (df_race['RACE AND HISPANIC OR LATINO ORIGIN'] == race_filter), :]
    dff_race = dff_race.rename(columns={
        'Total': f'Population for {race_filter} ', 
        'Percent below poverty level': f'% Poverty for {race_filter}'}).drop('RACE AND HISPANIC OR LATINO ORIGIN', axis=1)

    dff_pop = dff_pop.merge(dff_race, how='left', on='Zipcode')

    with st.spinner('Loading...'):
        # plot choropleth
        fig = px.choropleth(dff_pop, 
                            geojson=zipcodes, locations='Zipcode', 
                            featureidkey='properties.ZCTA5CE10',
                            color='Total % below poverty level',
                            color_continuous_scale="Viridis",
                            range_color=(dff_pop['Total % below poverty level'].min(), dff_pop['Total % below poverty level'].max()),
                            scope="usa",
                            # hover_data=dff_pop.loc[:, dff_pop.columns != 'Zipcode'].columns.values.tolist(),
                            hover_data=dff_pop.columns.values.tolist(),
                            height=500
                            )
        fig.update_geos(fitbounds="locations")
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            )
        st.plotly_chart(fig, use_container_width=True)


