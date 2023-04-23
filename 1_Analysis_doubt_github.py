import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import plotly.express as px


# from: https://youtu.be/lWxN-n6L7Zc
# StreamlitAPIException: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script.


st.set_page_config(page_title="Election Party Candidate Analysis",
                    layout='wide',
                    initial_sidebar_state="expanded")


############################## GET DATA ##############################
# @st.cache
# @st.cache_data
def get_data():
    df = pl.scan_parquet('Elections_Data_Compiled.parquet')
    
    return df

df = get_data()
############################## DATA DONE ##############################





############################## CREATING HEADER ##############################

header_left,header_mid,header_right = st.columns([1,6,1],gap = "large")

with header_mid:
    # https://docs.streamlit.io/library/get-started/create-an-app
    st.title("Party Criminal Records Analysis")

############################## HEADER DONE ##############################





############################## FIRST FILTER STATE ##############################

with st.sidebar:
    State_List = df.lazy().select(pl.col('State')).unique().collect().to_series().to_list()

    # State_Selected = st.selectbox(label="Select State",
    #                               options = State_List)

    State_Selected = st.multiselect(label="Select State",
                                    options = State_List,
                                    default = ["Uttar Pradesh"], # Delhi West Bengal  
                                    # default = State_List[-1],
                                    max_selections=1
                                       )
    
############################## FIRST FILTER STATE DONE ##############################





############################## SECOND FILTER YEAR ##############################

    Year_List = df.lazy().filter(pl.col('State').is_in(State_Selected)).select(
                                                pl.col('Year')).unique().collect().to_series().sort().to_list()

    Year_Selected = st.multiselect(label="Select Election Year",
                                     options=Year_List,
                                     default=Year_List[-1])
    
############################## SECOND FILTER YEAR DONE ##############################
    




############################## FILTERED DATA ##############################

df_selected = df.lazy().filter(pl.col('State').is_in(State_Selected) &
                    (pl.col('Year').is_in(Year_Selected))
                    ).collect()
    
############################## FILTERED DATA DONE ##############################    





############################## FIRST PLOT ##############################

fig_party_crime_sum = px.bar(df_selected.groupby(['Party']
                            ).agg(pl.col('Criminal_Case').sum()
                            ).sort(by='Criminal_Case',descending=True
                            ).head(18).to_pandas(),
                            orientation='h',
                            x='Criminal_Case',y='Party', color="Party",
                            labels={
                                    "Criminal_Case": "Total Criminal Cases",
                                    "Party": "Election Parties"
                                },
                        
                        title=f'<b>{State_Selected} - Top 18 Election Parties with Total Criminal Records in {Year_Selected} Elections</b>')

# fig_party_crime_sum.update_yaxes(autorange="reversed")
fig_party_crime_sum.update_layout(title_font_size=26, height = 600, 
                                    showlegend=False
                                    )
fig_party_crime_sum.add_annotation(
                                    showarrow=False,
                                    text='Data Source: https://myneta.info/',
                                    xanchor='right',
                                    x=2,
                                    xshift=675,
                                    yanchor='bottom',
                                    y=0.01 #,
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=22,
                                    #     color="#0000FF"
                                )

st.plotly_chart(fig_party_crime_sum,use_container_width=True)

############################## FIRST PLOT DONE ##############################