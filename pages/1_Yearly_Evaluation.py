import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Yearly Overview",
)

st.header("Yearly Overview")

### --------------------------------------- Data Preparation ------------------------------------------------- ###

df_wcoverall = pd.read_csv('./data/wcoverall.csv')

# column 1
fig1, ax1 = plt.subplots()
ax1.bar(df_wcoverall['Year'], df_wcoverall['QualifiedTeams'], width=2, align='center')

# column 2
fig2, ax2 = plt.subplots()
ax2.bar(df_wcoverall['Year'], df_wcoverall['MatchesPlayed'], width=2, align='center')



### --------------------------------------- Page Design ------------------------------------------------- ###

## Sidebar Design

def user_input_features():

    # dropdown: years
    # year = st.sidebar.selectbox("World Cup Years",
    #                             df_wcoverall['Year'],
    #                             index=0)

    year = st.sidebar.multiselect("World Cup Years",
                                   df_wcoverall['Year'],
                                  )

    data = { 'year': year }

    input_features = pd.DataFrame(data)
    print(input_features.head(10))
    return input_features

df_input_features = user_input_features()

## Main Page Layout
tab1, tab2 = st.tabs(['Bar Charts', 'Tabular Data'])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.caption('Teams Qualified each Year')
        st.pyplot(fig1)
    with col2:
        st.caption('Matches Played each Year')
        st.pyplot(fig2)

with tab2:
    df_table = df_wcoverall
    if len(df_input_features['year']) != 0:
        df_table = df_table[df_table['Year'].isin(df_input_features['year'])]
    st.table(df_table )


