import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Countries' Performance",
)

st.header("Countries' Performance")

### --------------------------------------- Data Preparation ------------------------------------------------- ###

df_wcmatches = pd.read_csv('./data/wcmatches.csv')
df_wcoverall = pd.read_csv('./data/wcoverall.csv')


### --------------------------------------- Page Design ------------------------------------------------- ###

def user_input_features():

    # dropdown: countries
    df_countries = df_wcmatches['Home Team Name'].drop_duplicates()
    df_countries = df_countries.append(df_wcmatches['Away Team Name'].drop_duplicates())
    countries = st.sidebar.multiselect("Participating Countries",
                                   df_countries.drop_duplicates().sort_values(ascending=True),
                                  )

    data = { 'country': countries }

    input_features = pd.DataFrame(data)
    print(input_features.head(10))
    return input_features

df_input_features = user_input_features()

## Main Page Layout
tab1, tab2 = st.tabs(['Count of Cup Wins', 'Goals Scored'])

with tab1:
    df_rank = df_wcoverall.groupby('Winner').size().sort_values(ascending=False)
    df_rank = pd.DataFrame(df_rank, columns=['WC Wins'])
    st.dataframe(df_rank)

with tab2:
    df_goals_home = df_wcmatches.groupby('Home Team Name')['Home Team Goals'].sum().sort_values(ascending=False).reset_index()
    df_goals_away = df_wcmatches.groupby('Away Team Name')['Away Team Goals'].sum().sort_values(ascending=False).reset_index()

    df_goals_home.columns = ['Country', 'Goals']
    df_goals_away.columns = ['Country', 'Goals']
    df_goals = pd.concat([ df_goals_home, df_goals_away ])
    df_goals.sort_values(by='Country', ascending=True)

    df_goals = df_goals.groupby(by='Country')['Goals'].sum().sort_values(ascending=False).reset_index()

    # df_goals_merge = pd.merge(df_goals_home,df_goals_away,how='left',on='Country',sort=False,validate='1:1')
    # df_goals['Home Goals'] = df_goals_merge['Goals_x'].astype(str).astype(int)
    # df_goals['Away Goals'] = df_goals_merge['Goals_y']

    if len(df_input_features['country']) != 0:
        df_goals = df_goals[df_goals['Country'].isin(df_input_features['country'])]

    st.table(df_goals)



