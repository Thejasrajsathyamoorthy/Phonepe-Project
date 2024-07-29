import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import nbformat
import requests
import json

# DataFrame creation

#SQL connection

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "phonepe_data",
                        password = "Thejas@4218")

cursor = mydb.cursor()

# Aggregated_Insurance_DF

cursor.execute("SELECT * FROM Aggregated_Insurance")
mydb.commit()
agg_ins_table = cursor.fetchall()

Aggregated_Insurance = pd.DataFrame(agg_ins_table, columns=("States", "Years", "Quarter", "Transaction_type",
                                                             "Transaction_count", "Transaction_amount"))


# Aggregated_Transaction_DF

cursor.execute("SELECT * FROM Aggregated_Transaction")
mydb.commit()
agg_trans_table = cursor.fetchall()

Aggregated_Transaction = pd.DataFrame(agg_trans_table, columns=("States", "Years", "Quarter", "Transaction_type",
                                                             "Transaction_count", "Transaction_amount"))


# Aggregated_User_DF

cursor.execute("SELECT * FROM Aggregated_User")
mydb.commit()
agg_user_table = cursor.fetchall()

Aggregated_User = pd.DataFrame(agg_user_table, columns=("States", "Years", "Quarter", "Brands",
                                                             "Transaction_count", "Percentage"))


# Map_Insurance_DF

cursor.execute("SELECT * FROM Map_Insurance")
mydb.commit()
map_ins_table = cursor.fetchall()

Map_Insurance = pd.DataFrame(map_ins_table, columns=("States", "Years", "Quarter", "Districts",
                                                             "Transaction_count", "Transaction_amount"))


# Map_Transaction_DF

cursor.execute("SELECT * FROM Map_Transaction")
mydb.commit()
map_trans_table = cursor.fetchall()

Map_Transaction = pd.DataFrame(map_trans_table, columns=("States", "Years", "Quarter", "Districts",
                                                             "Transaction_count", "Transaction_amount"))


# Map_User_DF

cursor.execute("SELECT * FROM Map_User")
mydb.commit()
map_user_table = cursor.fetchall()

Map_User = pd.DataFrame(map_user_table, columns=("States", "Years", "Quarter", "Districts",
                                                             "Registered_users", "App_opens"))


# Top_Insurance_DF

cursor.execute("SELECT * FROM Top_Insurance")
mydb.commit()
top_ins_table = cursor.fetchall()

Top_Insurance = pd.DataFrame(top_ins_table, columns=("States", "Years", "Quarter", "Pincodes",
                                                             "Transaction_count", "Transaction_amount"))


# Top_Transaction_DF

cursor.execute("SELECT * FROM Top_Transaction")
mydb.commit()
top_trans_table = cursor.fetchall()

Top_Transaction = pd.DataFrame(top_trans_table, columns=("States", "Years", "Quarter", "Pincodes",
                                                             "Transaction_count", "Transaction_amount"))


# Top_User_DF

cursor.execute("SELECT * FROM Top_User")
mydb.commit()
top_user_table = cursor.fetchall()

Top_User = pd.DataFrame(top_user_table, columns=("States", "Years", "Quarter", "Pincodes",
                                                             "Registered_users"))


# to make bar chart in streamlit


#Aggregated Analysis


def Aggregated_Insurance_count_amount_year(df, Year):

    # aicay = Aggregated_Insurance_count_amount_year
    aicay = df[df["Years"] == Year]
    aicay.reset_index(drop= True, inplace= True)

    #aicayg = Aggregated_Insurance_count_amount_year_groupby
    aicayg = aicay.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    aicayg.reset_index(inplace= True)
    

    col1, col2 = st.columns(2)
    with col1:
        agg_ins_fig_count = px.bar(aicayg, x = "States", y = "Transaction_count", title= f"{Year} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800)
        st.plotly_chart(agg_ins_fig_count)

    with col2:
        agg_ins_fig_amount = px.bar(aicayg, x = "States", y = "Transaction_amount", title= f"{Year} Transaction Amount", color_discrete_sequence= px.colors.sequential.Jet_r, height = 650, width = 800)
        st.plotly_chart(agg_ins_fig_amount)


    # to plot data in streamlit in India map

    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)
    with col1:
        agg_ins_count_fig_india = px.choropleth(aicayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (aicayg["Transaction_count"].min(), aicayg["Transaction_count"].max()),
                                            title= f"{Year} Transaction count", fitbounds= "locations", height= 650, width = 750)
        
        agg_ins_count_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_ins_count_fig_india)
    
    with col2:
        agg_ins_amount_fig_india = px.choropleth(aicayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (aicayg["Transaction_amount"].min(), aicayg["Transaction_amount"].max()),
                                            title= f"{Year} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        agg_ins_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_ins_amount_fig_india)

        return aicay



def Aggregated_Insurance_count_amount_year_quarter(df, Quarter):

    # aicayq = Aggregated_Insurance_count_amount_year_quarter
    aicay = df[df["Quarter"] == Quarter]
    aicay.reset_index(drop= True, inplace= True)

    #aicayqg = Aggregated_Insurance_count_amount_year_quarter_groupby
    aicayg = aicay.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    aicayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        agg_ins_fig_count = px.bar(aicayg, x = "States", y = "Transaction_count", title= f"{aicay['Years'].min()} Year Q-{Quarter} Transaction Count", color_discrete_sequence= px.colors.sequential.Darkmint,  height = 650, width = 800)
        st.plotly_chart(agg_ins_fig_count)


    with col2:
        agg_ins_fig_amount = px.bar(aicayg, x = "States", y = "Transaction_amount", title= f"{aicay['Years'].min()} Year Q-{Quarter} Transaction Amount", color_discrete_sequence= px.colors.sequential.Sunset_r,  height = 650, width = 800)
        st.plotly_chart(agg_ins_fig_amount)


    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)

    with col1:
        agg_ins_count_fig_india = px.choropleth(aicayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (aicayg["Transaction_count"].min(), aicayg["Transaction_count"].max()),
                                            title= f"{aicay['Years'].min()} Year Q-{Quarter} Transaction count", fitbounds= "locations", height= 650, width = 800)
        agg_ins_count_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_ins_count_fig_india)

    with col2:
        agg_ins_amount_fig_india = px.choropleth(aicayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (aicayg["Transaction_amount"].min(), aicayg["Transaction_amount"].max()),
                                            title= f"{aicay['Years'].min()} Year Q-{Quarter} Transaction Amount", fitbounds= "locations", height= 650, width = 800)
        
        agg_ins_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_ins_amount_fig_india)

    

def Aggregated_Transaction_count_amount_year(df, Year):

    #atcay = Aggregated Transaction count amount year
    atcay = df[df["Years"] == Year]
    atcay.reset_index(drop= True, inplace= True)

    #atcayg = Aggregated Transaction count amount year groupby
    atcayg = atcay.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    atcayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        agg_trans_fig_count = px.bar(atcayg, x= "States", y= "Transaction_count", title= f"{Year} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height= 650, width= 800)
        st.plotly_chart(agg_trans_fig_count)

    with col2:
        agg_trans_fig_amount = px.bar(atcayg, x= "States", y= "Transaction_amount", title= f"{Year} Transaction Amount", color_discrete_sequence=px.colors.sequential.Magenta_r, height= 650, width = 800 )
        st.plotly_chart(agg_trans_fig_amount)

    
    # to plot data in streamlit in India map
    
    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)

    with col1:
        agg_trans_count_fig_india = px.choropleth(atcayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (atcayg["Transaction_count"].min(), atcayg["Transaction_count"].max()),
                                            title= f"{Year} Transaction Count", fitbounds= "locations", height= 650, width = 750)
        
        agg_trans_count_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_trans_count_fig_india)
    
    with col2:
        agg_trans_amount_fig_india = px.choropleth(atcayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (atcayg["Transaction_amount"].min(), atcayg["Transaction_amount"].max()),
                                            title= f"{Year} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        agg_trans_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_trans_amount_fig_india)

        return atcay



def Aggregated_Transaction_Type_Year(df, State):
    atcay = df[df["States"] == State ]
    atcay.reset_index(drop= True, inplace= True)

    atcayg = atcay.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    atcayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    
    with col1:
        agg_trans_pie_count = px.pie(data_frame= atcayg, names= "Transaction_type", values= "Transaction_count",
                                width = 600, title= f"{State.upper()}  TRANSACTION COUNT", hole = 0.5, color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(agg_trans_pie_count)

    with col2:
        agg_trans_pie_amount = px.pie(data_frame= atcayg, names= "Transaction_type", values= "Transaction_amount",
                                width = 600, title= f"{State.upper()}  TRANSACTION AMOUNT", hole= 0.5, color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(agg_trans_pie_amount)



def Aggregated_Transaction_count_amount_year_quarter(df, Quarter):
    #atcay = Aggregated Transaction count amount year
    atcayq = df[df["Quarter"] == Quarter]
    atcayq.reset_index(drop= True, inplace= True)

    #atcayg = Aggregated Transaction count amount year groupby
    atcayqg = atcayq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    atcayqg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        agg_trans_fig_count = px.bar(atcayqg, x= "States", y= "Transaction_count", title= f"{atcayq['Years'].min()} Year Q-{Quarter} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height= 650, width= 800)
        st.plotly_chart(agg_trans_fig_count)

    with col2:
        agg_trans_fig_amount = px.bar(atcayqg, x= "States", y= "Transaction_amount", title= f"{atcayq['Years'].min()} Year Q-{Quarter} Transaction Amount", color_discrete_sequence=px.colors.sequential.Cividis, height= 650, width = 800 )
        st.plotly_chart(agg_trans_fig_amount)


    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)
    with col1:
        agg_trans_count_fig_india = px.choropleth(atcayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (atcayqg["Transaction_count"].min(), atcayqg["Transaction_count"].max()),
                                            title= f"{atcayq['Years'].min()} Year Q-{Quarter} Transaction Count", fitbounds= "locations", height= 650, width = 750)
        
        agg_trans_count_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_trans_count_fig_india)
    
    with col2:
        agg_trans_amount_fig_india = px.choropleth(atcayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (atcayqg["Transaction_amount"].min(), atcayqg["Transaction_amount"].max()),
                                            title= f"{atcayq['Years'].min()} Year Q-{Quarter} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        agg_trans_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(agg_trans_amount_fig_india)

        return atcayq



def Aggregated_Transaction_Type_Year_Quarter(df, State):
    atcay = df[df["States"] == State ]
    atcay.reset_index(drop= True, inplace= True)

    atcayg = atcay.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    atcayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    
    with col1:
        agg_trans_pie_count = px.pie(data_frame= atcayg, names= "Transaction_type", values= "Transaction_count",
                                width = 600, title= f"{State.upper()}  TRANSACTION COUNT", hole = 0.5, color_discrete_sequence= px.colors.sequential.Agsunset_r )
        st.plotly_chart(agg_trans_pie_count)

    with col2:
        agg_trans_pie_amount = px.pie(data_frame= atcayg, names= "Transaction_type", values= "Transaction_amount",
                                width = 600, title= f"{State.upper()}  TRANSACTION AMOUNT", hole= 0.5, color_discrete_sequence= px.colors.sequential.Bluyl )
        st.plotly_chart(agg_trans_pie_amount)



def Aggregated_User_Transaction_Year(df, Year):
    agguy = df[df["Years"] == Year]
    agguy.reset_index(drop= True, inplace= True)

    agguyg = pd.DataFrame(agguy.groupby("Brands")["Transaction_count"].sum())
    agguyg.reset_index(inplace= True)


    fig_agg_user = px.bar(agguyg, x = "Brands", y = "Transaction_count", title = f"{Year} Brands and Transaction_count",
                           color_discrete_sequence=px.colors.sequential.Rainbow, height = 650, width = 1350, hover_name= "Brands")
    st.plotly_chart(fig_agg_user)

    return agguy



def Aggregated_User_Transaction_Year_Quarter(df, Quarter):
    agguyq = df[df["Quarter"] == Quarter]
    agguyq.reset_index(drop= True, inplace= True)

    agguyqg = pd.DataFrame(agguyq.groupby("Brands")["Transaction_count"].sum())
    agguyqg.reset_index(inplace= True)


    fig_agg_user = px.bar(agguyqg, x = "Brands", y = "Transaction_count", title = f"Q-{Quarter} Brands and Transaction_count",
                           color_discrete_sequence=px.colors.sequential.algae, height = 650, width = 1350)
    st.plotly_chart(fig_agg_user)

    return agguyq



def Aggregated_User_Transaction_State(df, State):
    aggus = df[df["States"] == State]
    aggus.reset_index(drop= True, inplace= True)

    fig_agg_user_s = px.line(aggus, x = "Brands", y = "Transaction_count", hover_name= "Percentage", color_discrete_sequence = px.colors.sequential.Blackbody_r,
                            title= f" {State.upper()} - Brands, Transaction count, Percentage", width= 1350, markers= True, hover_data= "Percentage") 
    st.plotly_chart(fig_agg_user_s)


# Map Analysis


def Map_Insurance_count_amount_year(df, Year):

    # micay = Map_Insurance_count_amount_year
    micay = df[df["Years"] == Year]
    micay.reset_index(drop= True, inplace= True)

    #micayg = Map_Insurance_count_amount_year_groupby
    micayg = micay.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    micayg.reset_index(inplace= True)
    

    col1, col2 = st.columns(2)
    with col1:
        map_ins_fig_count = px.bar(micayg, x = "States", y = "Transaction_count", title= f"{Year} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800)
        st.plotly_chart(map_ins_fig_count)

    with col2:
        map_ins_fig_amount = px.bar(micayg, x = "States", y = "Transaction_amount", title= f"{Year} Transaction Amount", color_discrete_sequence= px.colors.sequential.Jet_r, height = 650, width = 800)
        st.plotly_chart(map_ins_fig_amount)


    # to plot data in streamlit in India map

    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)
    with col1:
        map_ins_count_fig_india = px.choropleth(micayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (micayg["Transaction_count"].min(), micayg["Transaction_count"].max()),
                                            title= f"{Year} Transaction count", fitbounds= "locations", height= 650, width = 750)
        
        map_ins_count_fig_india.update_geos(visible = False)
        st.plotly_chart(map_ins_count_fig_india)
    
    with col2:
        map_ins_amount_fig_india = px.choropleth(micayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (micayg["Transaction_amount"].min(), micayg["Transaction_amount"].max()),
                                            title= f"{Year} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        map_ins_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(map_ins_amount_fig_india)

        return micay
    

    
def Map_Insurance_Count_amount_year_district(df, State):
    micay = df[df["States"] == State ]
    micay.reset_index(drop= True, inplace= True)

    micayg = micay.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    micayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    
    with col1:
        map_ins_bar_count = px.bar(data_frame= micayg, x = "Transaction_count", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Count", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(map_ins_bar_count)

    with col2:
        map_ins_bar_amount = px.bar(data_frame= micayg, x = "Transaction_amount", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Amount", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(map_ins_bar_amount)




def Map_Insurance_count_amount_year_quarter(df, Quarter):

    # micayq = Map_Insurance_count_amount_year_quarter
    micayq = df[df["Quarter"] == Quarter]
    micayq.reset_index(drop= True, inplace= True)

    #micayqg = Map_Insurance_count_amount_year_quarter_groupby
    micayqg = micayq.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    micayqg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        map_ins_fig_count = px.bar(micayqg, x = "States", y = "Transaction_count", title= f"{micayq['Years'].min()} Year Q-{Quarter} Insurance Count", color_discrete_sequence= px.colors.sequential.Darkmint,  height = 650, width = 800)
        st.plotly_chart(map_ins_fig_count)


    with col2:
        map_ins_fig_amount = px.bar(micayqg, x = "States", y = "Transaction_amount", title= f"{micayq['Years'].min()} Year Q-{Quarter} Insurance Amount", color_discrete_sequence= px.colors.sequential.Sunset_r,  height = 650, width = 800)
        st.plotly_chart(map_ins_fig_amount)


    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)

    with col1:
        map_ins_count_fig_india = px.choropleth(micayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (micayqg["Transaction_count"].min(), micayqg["Transaction_count"].max()),
                                            title= f"{micayq['Years'].min()} Year Q-{Quarter} Transaction count", fitbounds= "locations", height= 650, width = 800)
        map_ins_count_fig_india.update_geos(visible = False)
        st.plotly_chart(map_ins_count_fig_india)

    with col2:
        map_ins_amount_fig_india = px.choropleth(micayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (micayqg["Transaction_amount"].min(), micayqg["Transaction_amount"].max()),
                                            title= f"{micayq['Years'].min()} Year Q-{Quarter} Transaction Amount", fitbounds= "locations", height= 650, width = 800)
        
        map_ins_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(map_ins_amount_fig_india)


        return micayq



def Map_Insurance_count_amount_year_quarter_district(df, State):
    micayq = df[df["States"] == State ]
    micayq.reset_index(drop= True, inplace= True)

    micayqg = micayq.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    micayqg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:    
        map_ins_bar_count = px.bar(data_frame= micayqg, x = "Transaction_count", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Count", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(map_ins_bar_count)

    with col2:
        map_ins_bar_amount = px.bar(data_frame= micayqg, x = "Transaction_amount", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Amount", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(map_ins_bar_amount)


    
def Map_Transaction_count_amount_year(df, Year):

    #mtcay = map transaction count amount year
    mtcay = df[df["Years"] == Year]
    mtcay.reset_index(drop= True, inplace= True)

    #mtcayg = map transaction count amount year groupby
    mtcayg = mtcay.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    mtcayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        map_trans_fig_count = px.bar(mtcayg, x= "States", y= "Transaction_count", title= f"{Year} Transaction Count",
                                color_discrete_sequence= px.colors.sequential.algae, height= 650, width= 800)
        st.plotly_chart(map_trans_fig_count)

    with col2:
        map_trans_fig_amount = px.bar(mtcayg, x= "States", y= "Transaction_amount", title= f"{Year} Transaction Amount",
                                color_discrete_sequence=px.colors.sequential.Magenta_r, height= 650, width = 800 )
        st.plotly_chart(map_trans_fig_amount)

    
    # to plot data in streamlit in India map
    
    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)

    with col1:
        map_trans_count_fig_india = px.choropleth(mtcayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (mtcayg["Transaction_count"].min(), mtcayg["Transaction_count"].max()),
                                            title= f"{Year} Transaction Count", fitbounds= "locations", height= 650, width = 750)
        
        map_trans_count_fig_india.update_geos(visible = False)
        st.plotly_chart(map_trans_count_fig_india)

    with col2:
        map_trans_amount_fig_india = px.choropleth(mtcayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (mtcayg["Transaction_amount"].min(), mtcayg["Transaction_amount"].max()),
                                            title= f"{Year} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        map_trans_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(map_trans_amount_fig_india)

        return mtcay



def Map_Transaction_Type_Year_District(df, State):
    mtcay = df[df["States"] == State ]
    mtcay.reset_index(drop= True, inplace= True)

    mtcayg = mtcay.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    mtcayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        map_trans_bar_count = px.bar(data_frame= mtcayg, x = "Transaction_count", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Count", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(map_trans_bar_count)

    with col2:
        map_trans_bar_amount = px.bar(data_frame= mtcayg, x = "Transaction_amount", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Amount", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(map_trans_bar_amount)




def Map_Transaction_count_amount_year_quarter(df, Quarter):
    #mtcay = Map transaction count amount year
    mtcayq = df[df["Quarter"] == Quarter]
    mtcayq.reset_index(drop= True, inplace= True)

    #atcayg = Aggregated transaction count amount year groupby
    mtcayqg = mtcayq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    mtcayqg.reset_index(inplace= True)

    col1,col2 = st.columns(2)

    with col1:
        map_trans_fig_count = px.bar(mtcayqg, x= "States", y= "Transaction_count", title= f"{mtcayq['Years'].min()} Year Q-{Quarter} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height= 650, width= 800)
        st.plotly_chart(map_trans_fig_count)

    with col2:
        map_trans_fig_amount = px.bar(mtcayqg, x= "States", y= "Transaction_amount", title= f"{mtcayq['Years'].min()} Year Q-{Quarter} Transaction Amount", color_discrete_sequence=px.colors.sequential.Cividis, height= 650, width = 800 )
        st.plotly_chart(map_trans_fig_amount)


    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1,col2 = st.columns(2)

    with col1:
        map_trans_count_fig_india = px.choropleth(mtcayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (mtcayqg["Transaction_count"].min(), mtcayqg["Transaction_count"].max()),
                                            title= f"{mtcayq['Years'].min()} Year Q-{Quarter} Transaction Count", fitbounds= "locations", height= 650, width = 750)
        
        map_trans_count_fig_india.update_geos(visible = False)
        st.plotly_chart(map_trans_count_fig_india)

    with col2:
        map_trans_amount_fig_india = px.choropleth(mtcayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (mtcayqg["Transaction_amount"].min(), mtcayqg["Transaction_amount"].max()),
                                            title= f"{mtcayq['Years'].min()} Year Q-{Quarter} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        map_trans_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(map_trans_amount_fig_india)

    return mtcayq



def Map_Transaction_Type_Year_Quarter_District(df, State):
    mtcay = df[df["States"] == State ]
    mtcay.reset_index(drop= True, inplace= True)

    mtcayg = mtcay.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    mtcayg.reset_index(inplace= True)

    col1,col2 = st.columns(2)

    with col1:
        map_trans_bar_count = px.bar(data_frame= mtcayg, x = "Transaction_count", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Count", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(map_trans_bar_count)

    with col2:
        map_trans_bar_amount = px.bar(data_frame= mtcayg, x = "Transaction_amount", y = "Districts", width = 600, orientation= "h",
                                title= f"{State.upper()} Districts and Transaction Amount", hover_name= "Districts", color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(map_trans_bar_amount)




def Map_Registered_Users_Year(df, Year):
    mapuy = df[df["Years"] == Year]
    mapuy.reset_index(drop= True, inplace= True)

    mapuyg = pd.DataFrame(mapuy.groupby("Districts")["Registered_users"].sum())
    mapuyg.reset_index(inplace= True)


    fig_map_user_y = px.bar(mapuyg, x = "Districts", y = "Registered_users", title = f"{Year} Districts and Registered Users", color_discrete_sequence=px.colors.sequential.Rainbow, height = 750, width = 1500, hover_name= "Districts")
    st.plotly_chart(fig_map_user_y)

    return mapuy



def Map_Registered_Users_Year_Quarter(df, Quarter):
    mapuyq = df[df["Quarter"] == Quarter]
    mapuyq.reset_index(drop= True, inplace= True)

    mapuyqg = pd.DataFrame(mapuyq.groupby("Districts")["Registered_users"].sum())
    mapuyqg.reset_index(inplace= True)


    fig_map_user_q = px.bar(mapuyqg, x = "Districts", y = "Registered_users", title = f"Q-{Quarter} Districts and Registered_users", color_discrete_sequence=px.colors.sequential.Rainbow, height = 750, width = 1500, hover_name= "Districts")
    st.plotly_chart(fig_map_user_q)

    return mapuyq



def Map_User_Transaction_State(df, State):
    mapus = df[df["States"] == State]
    mapus.reset_index(drop= True, inplace= True)

    fig_map_user_s = px.line(mapus, x = "Districts", y = "Registered_users", hover_name= "App_opens",
                            title= f" {State} - Districts, Registered_users, App_opens", width= 2000, height= 600, markers= True) 
    
    st.plotly_chart(fig_map_user_s)



def Top_Insurance_count_amount_year(df, Year):

    # ticay = Top_Insurance_count_amount_year
    ticay = df[df["Years"] == Year]
    ticay.reset_index(drop= True, inplace= True)

    #ticayg = Top_Insurance_count_amount_year_groupby
    ticayg = ticay.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    ticayg.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)

    with col1:
        fig_count = px.bar(ticayg, x = "States", y = "Transaction_count", title= f"{Year} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800)
        st.plotly_chart(fig_count)

    with col2:
        fig_amount = px.bar(ticayg, x = "States", y = "Transaction_amount", title= f"{Year} Transaction Amount", color_discrete_sequence= px.colors.sequential.Jet_r, height = 650, width = 800)
        st.plotly_chart(fig_amount)


    # to plot data in streamlit in India map

    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1,col2 = st.columns(2)

    with col1:
        top_ins_count_fig_india = px.choropleth(ticayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ticayg["Transaction_count"].min(), ticayg["Transaction_count"].max()),
                                            title= f"{Year} Transaction count", fitbounds= "locations", height= 650, width = 750)
        
        top_ins_count_fig_india.update_geos(visible = False)
        st.plotly_chart(top_ins_count_fig_india)

    with col2:
        top_ins_amount_fig_india = px.choropleth(ticayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ticayg["Transaction_amount"].min(), ticayg["Transaction_amount"].max()),
                                            title= f"{Year} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        top_ins_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(top_ins_amount_fig_india)

        return ticay



def Top_Insurance_count_amount_year_district(df, State):
    ticay = df[df["States"] == State ]
    ticay.reset_index(drop= True, inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        top_ins_bar_count = px.bar(data_frame= ticay, x = "Quarter", y = "Transaction_count", width = 600, orientation= "v",
                                title= f"{State.upper()} Pincodes and Transaction Count", hover_name= "Pincodes", color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(top_ins_bar_count)

    with col2:
        top_ins_bar_amount = px.bar(data_frame= ticay, x = "Quarter", y = "Transaction_amount", width = 600, orientation= "v",
                                title= f"{State.upper()} Pincodes and Transaction Amount", hover_name= "Pincodes", color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(top_ins_bar_amount)




def Top_Insurance_count_amount_year_quarter(df, Quarter):

    # ticayq = Top_Insurance_count_amount_year_quarter
    ticayq = df[df["Quarter"] == Quarter]
    ticayq.reset_index(drop= True, inplace= True)

    #ticayqg = Top_Insurance_count_amount_year_quarter_groupby
    ticayg = ticayq.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    ticayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_count = px.bar(ticayg, x = "States", y = "Transaction_count", title= f"{ticayq['Years'].min()} Year Q-{Quarter} Insurance Count", color_discrete_sequence= px.colors.sequential.Darkmint,  height = 650, width = 800)
        st.plotly_chart(fig_count)


    with col2:
        fig_amount = px.bar(ticayg, x = "States", y = "Transaction_amount", title= f"{ticayq['Years'].min()} Year Q-{Quarter} Insurance Amount", color_discrete_sequence= px.colors.sequential.Sunset_r,  height = 650, width = 800)
        st.plotly_chart(fig_amount)


    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    

    col1, col2 = st.columns(2)

    with col1:
        top_ins_count_fig_india = px.choropleth(ticayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ticayg["Transaction_count"].min(), ticayg["Transaction_count"].max()),
                                            title= f"{ticayq['Years'].min()} Year Q-{Quarter} Transaction count", fitbounds= "locations", height= 650, width = 800)
        top_ins_count_fig_india.update_geos(visible = False)
        st.plotly_chart(top_ins_count_fig_india)

    with col2:
        top_ins_amount_fig_india = px.choropleth(ticayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ticayg["Transaction_amount"].min(), ticayg["Transaction_amount"].max()),
                                            title= f"{ticayq['Years'].min()} Year Q-{Quarter} Transaction Amount", fitbounds= "locations", height= 650, width = 800)
        
        top_ins_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(top_ins_amount_fig_india)



def Top_Transaction_count_amount_year(df, Year):

    #ttcay = Top transaction count amount year
    ttcay = df[df["Years"] == Year]
    ttcay.reset_index(drop= True, inplace= True)

    #mtcayg = Top transaction count amount year groupby
    ttcayg = ttcay.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    ttcayg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        top_trans_fig_count = px.bar(ttcayg, x= "States", y= "Transaction_count", title= f"{Year} Transaction Count",
                                color_discrete_sequence= px.colors.sequential.algae, height= 650, width= 800)
        st.plotly_chart(top_trans_fig_count)

    with col2:
        top_trans_fig_amount = px.bar(ttcayg, x= "States", y= "Transaction_amount", title= f"{Year} Transaction Amount",
                                color_discrete_sequence=px.colors.sequential.Magenta_r, height= 650, width = 800 )
        st.plotly_chart(top_trans_fig_amount)

    
    # to plot data in streamlit in India map
    
    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)

    with col1:
        top_trans_count_fig_india = px.choropleth(ttcayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ttcayg["Transaction_count"].min(), ttcayg["Transaction_count"].max()),
                                            title= f"{Year} Transaction Count", fitbounds= "locations", height= 650, width = 750)
        
        top_trans_count_fig_india.update_geos(visible = False)
        st.plotly_chart(top_trans_count_fig_india)

    with col2:
        top_trans_amount_fig_india = px.choropleth(ttcayg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ttcayg["Transaction_amount"].min(), ttcayg["Transaction_amount"].max()),
                                            title= f"{Year} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        top_trans_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(top_trans_amount_fig_india)

        return ttcay



def Top_Transaction_Type_Year_Areas(df, State):
    ttcay = df[df["States"] == State ]
    ttcay.reset_index(drop= True, inplace= True)
    
    col1, col2 = st.columns(2)

    with col1:
        top_trans_bar_count = px.bar(data_frame= ttcay, x = "Quarter", y = "Transaction_count", width = 600, orientation= "v",
                                title= f"{State.upper()} Pincodes and Transaction Count", hover_name= "Pincodes", color_discrete_sequence= px.colors.sequential.Emrld )
        st.plotly_chart(top_trans_bar_count)

    with col2:
        top_trans_bar_amount = px.bar(data_frame= ttcay, x = "Quarter", y = "Transaction_amount", width = 600, orientation= "v",
                                title= f"{State.upper()} Pincodes and Transaction Amount", hover_name= "Pincodes", color_discrete_sequence= px.colors.sequential.Brwnyl)
        st.plotly_chart(top_trans_bar_amount)



def Top_Transaction_count_amount_year_quarter(df, Quarter):
    #ttcay = Top transaction count amount year
    ttcayq = df[df["Quarter"] == Quarter]
    ttcayq.reset_index(drop= True, inplace= True)

    #ttcayg = Top transaction count amount year groupby
    ttcayqg = ttcayq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    ttcayqg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        top_trans_fig_count = px.bar(ttcayqg, x= "States", y= "Transaction_count", title= f"{ttcayq['Years'].min()} Year Q-{Quarter} Transaction Count", color_discrete_sequence= px.colors.sequential.algae, height= 650, width= 800)
        st.plotly_chart(top_trans_fig_count)

    with col2:
        top_trans_fig_amount = px.bar(ttcayqg, x= "States", y= "Transaction_amount", title= f"{ttcayq['Years'].min()} Year Q-{Quarter} Transaction Amount", color_discrete_sequence=px.colors.sequential.Cividis, height= 650, width = 800 )
        st.plotly_chart(top_trans_fig_amount)


    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geo_response = requests.get(geo_url)
    ins_geo_data = json.loads(geo_response.content)

    state_names = []
    for feature in ins_geo_data["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    col1, col2 = st.columns(2)

    with col1:
        top_trans_count_fig_india = px.choropleth(ttcayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_count", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ttcayqg["Transaction_count"].min(), ttcayqg["Transaction_count"].max()),
                                            title= f"{ttcayq['Years'].min()} Year Q-{Quarter} Transaction Count", fitbounds= "locations", height= 650, width = 750)
        
        top_trans_count_fig_india.update_geos(visible = False)
        st.plotly_chart(top_trans_count_fig_india)

    with col2:
        top_trans_amount_fig_india = px.choropleth(ttcayqg, geojson= ins_geo_data, locations= "States", featureidkey= "properties.ST_NM", 
                                            color= "Transaction_amount", hover_name= "States", color_continuous_scale= "tropic",
                                            range_color= (ttcayqg["Transaction_amount"].min(), ttcayqg["Transaction_amount"].max()),
                                            title= f"{ttcayq['Years'].min()} Year Q-{Quarter} Transaction Amount", fitbounds= "locations", height= 650, width = 750)
        
        top_trans_amount_fig_india.update_geos(visible = False)
        st.plotly_chart(top_trans_amount_fig_india)

    return ttcayq


def Top_User_Registered_Year(df, Year):
    topuy = df[df["Years"] == Year]
    topuy.reset_index(drop= True, inplace= True)

    topuyg = pd.DataFrame(topuy.groupby(["States", "Quarter"])["Registered_users"].sum())
    topuyg.reset_index(inplace= True)


    top_user_fig_y = px.bar(topuyg, x = "States", y = "Registered_users",color = "Quarter", title = f"{Year} Pincodes and Registered Users", color_discrete_sequence=px.colors.sequential.Rainbow, height = 550, width = 1350, hover_name= "States")
    st.plotly_chart(top_user_fig_y)

    return topuy


def Top_User_Transaction_State(df, State):
    topus = df[df["States"] == State]
    topus.reset_index(drop= True, inplace= True)

    top_user_fig_s = px.bar(topus, x = "Quarter", y = "Registered_users",color= "Registered_users", title = f"{State} Quarter, Pincodes and Registered Users", color_continuous_scale = px.colors.sequential.YlOrRd_r, height = 550, width = 1450, hover_name= "Pincodes")
    st.plotly_chart(top_user_fig_s)


def Analysis_transaction_amount(table_name):
    
    Analysis_Top_10_Transaction_Amount = f'''SELECT States, sum(Transaction_amount) AS Transaction_Amount
                                            FROM {table_name}
                                            GROUP BY States
                                            ORDER BY Transaction_amount DESC
                                            LIMIT 10;'''


    cursor.execute(Analysis_Top_10_Transaction_Amount)
    Analysis_Top_10_Table = cursor.fetchall()
    mydb.commit()

    col1, col2 = st.columns(2)

    with col1:
        Analysis_Top_10_df = pd.DataFrame(Analysis_Top_10_Table, columns= ("States", "Transaction_amount"))
        Analysis_Top_10_fig_count = px.bar(Analysis_Top_10_df, x = "States", y = "Transaction_amount", title=f"{table_name} Top 10 Transaction Amount", 
                                            color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800, hover_name= "States")
        st.plotly_chart(Analysis_Top_10_fig_count)



    Analysis_Bottom_10_Transaction_Amount = f'''SELECT States, sum(Transaction_amount) AS Transaction_Amount
                                                FROM {table_name}
                                                GROUP BY States
                                                ORDER BY Transaction_amount
                                                LIMIT 10;'''

    cursor.execute(Analysis_Bottom_10_Transaction_Amount)
    Analysis_Bottom_10_Table = cursor.fetchall()
    mydb.commit()

    with col2:
        Analysis_Bottom_10_df = pd.DataFrame(Analysis_Bottom_10_Table, columns=("States", "Transaction_amount"))
        Analysis_Bottom_10_fig_count = px.bar(Analysis_Bottom_10_df, x = "States", y = "Transaction_amount", title=f"{table_name} Bottom 10 Transaction Amount", 
                                            color_discrete_sequence= px.colors.sequential.Aggrnyl_r, height = 700, width = 800, hover_name= "States")
        st.plotly_chart(Analysis_Bottom_10_fig_count)


    Analysis_Average_Transaction_Amount = f'''SELECT States, AVG(Transaction_amount) AS Transaction_Amount
                                                    FROM {table_name}
                                                    GROUP BY States
                                                    ORDER BY Transaction_amount ;'''

    cursor.execute(Analysis_Average_Transaction_Amount)
    Analysis_Average_Table = cursor.fetchall()
    mydb.commit()

    Analysis_Average_df = pd.DataFrame(Analysis_Average_Table, columns = ("States", "Transaction_amount"))
    Analysis_Average_fig_count = px.bar(Analysis_Average_df, y = "States", x = "Transaction_amount", title=f"{table_name} Average Transaction Amount", orientation = "h", 
                                        color_discrete_sequence= px.colors.sequential.Agsunset_r, height = 850, width = 1500, hover_name= "States")
    st.plotly_chart(Analysis_Average_fig_count)



def Analysis_transaction_count(table_name):
    
    Analysis_Top_10_Transaction_Count = f'''SELECT States, sum(Transaction_count) AS Transaction_Count
                                                        FROM {table_name}
                                                        GROUP BY States
                                                        ORDER BY Transaction_count DESC
                                                        LIMIT 10
                                                        ;'''


    cursor.execute(Analysis_Top_10_Transaction_Count)
    Analysis_Top_10_Table = cursor.fetchall()
    mydb.commit()

    col1, col2 = st.columns(2)

    with col1:
        Analysis_Top_10_df = pd.DataFrame(Analysis_Top_10_Table, columns= ("States", "Transaction_count"))
        Analysis_Top_10_fig_count = px.bar(Analysis_Top_10_df, x = "States", y = "Transaction_count", title=f"{table_name} Top 10 Transaction Count", 
                                            color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800, hover_name= "States")
        st.plotly_chart(Analysis_Top_10_fig_count)



    Analysis_Bottom_10_Transaction_Count = f'''SELECT States, sum(Transaction_count) AS Transaction_Count
                                                        FROM {table_name}
                                                        GROUP BY States
                                                        ORDER BY Transaction_count
                                                        LIMIT 10
                                                        ;'''

    cursor.execute(Analysis_Bottom_10_Transaction_Count)
    Analysis_Bottom_10_Table = cursor.fetchall()
    mydb.commit()

    with col2:
        Analysis_Bottom_10_df = pd.DataFrame(Analysis_Bottom_10_Table, columns=("States", "Transaction_count"))
        Analysis_Bottom_10_fig_count = px.bar(Analysis_Bottom_10_df, x = "States", y = "Transaction_count", title=f"{table_name} Bottom 10 Transaction Count", 
                                            color_discrete_sequence= px.colors.sequential.Aggrnyl_r, height = 700, width = 800, hover_name= "States")
        st.plotly_chart(Analysis_Bottom_10_fig_count)


    Analysis_Average_Transaction_Count = f'''SELECT States, avg(Transaction_count) AS Transaction_Count
                                                        FROM {table_name}
                                                        GROUP BY States
                                                        ORDER BY Transaction_count
                                                        ;'''

    cursor.execute(Analysis_Average_Transaction_Count)
    Analysis_Average_Table = cursor.fetchall()
    mydb.commit()

    Analysis_Average_df = pd.DataFrame(Analysis_Average_Table, columns = ("States", "Transaction_count"))
    Analysis_Average_fig_count = px.bar(Analysis_Average_df, y = "States", x = "Transaction_count", title=f"{table_name} Average Transaction Count", orientation = "h", 
                                        color_discrete_sequence= px.colors.sequential.Agsunset_r, height = 850, width = 1500, hover_name= "States")
    st.plotly_chart(Analysis_Average_fig_count)



def Analysis_registered_users(table_name, state):
    Analysis_Top_10_registered_users = f'''SELECT Districts, SUM(Registered_Users) AS Registered_Users
                                                    From {table_name}
                                                    WHERE States = '{state}'
                                                    GROUP BY Districts
                                                    ORDER BY  Registered_Users DESC
                                                    LIMIT 10;'''
    
    cursor.execute(Analysis_Top_10_registered_users)
    Analysis_Top_10_reg_user_table = cursor.fetchall()
    mydb.commit()

    col1, col2 = st.columns(2)

    with col1:
        Analysis_Top_10_reg_user_df = pd.DataFrame(Analysis_Top_10_reg_user_table, columns = ("Districts", "Registered_Users"))
        Analysis_Top_10_fig = px.bar(Analysis_Top_10_reg_user_df, x = "Districts", y = "Registered_Users", title="Top 10 Districts (Registered Users)",
                                        color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800)
        st.plotly_chart(Analysis_Top_10_fig)


    Analysis_Last_10_registered_users = f'''SELECT Districts, SUM(Registered_Users) AS Registered_Users
                                                    From {table_name}
                                                    Where States = '{state}'
                                                    GROUP BY Districts
                                                    ORDER BY  Registered_Users
                                                    LIMIT 10;'''
    
    cursor.execute(Analysis_Last_10_registered_users)
    Analysis_Last_10_reg_user_table = cursor.fetchall()
    mydb.commit()

    with col2:
        Analysis_Last_10_reg_user_df = pd.DataFrame(Analysis_Last_10_reg_user_table, columns = ("Districts", "Registered_Users"))
        Analysis_Last_10_fig = px.bar(Analysis_Last_10_reg_user_df, x = "Districts", y = "Registered_Users", title="Last 10 Districts (Registered Users)",
                                        color_discrete_sequence= px.colors.sequential.Aggrnyl_r, height = 650, width = 800)
        st.plotly_chart(Analysis_Last_10_fig)


    
    Analysis_Average_registered_users = f'''SELECT Districts, AVG(Registered_Users) AS Registered_Users
                                                    From {table_name}
                                                    WHERE States = '{state}'
                                                    GROUP BY Districts
                                                    ORDER BY  Registered_Users;
                                                    '''
    
    cursor.execute(Analysis_Average_registered_users)
    Analysis_Average_reg_user_table = cursor.fetchall()
    mydb.commit()

    Analysis_Average_reg_user_df = pd.DataFrame(Analysis_Average_reg_user_table, columns = ("Districts", "Registered_Users"))
    Analysis_Average_fig = px.bar(Analysis_Average_reg_user_df, x = "Registered_Users", y = "Districts", title="Average Registered Users each District", orientation="h",
                                    color_discrete_sequence= px.colors.sequential.Aggrnyl_r, height = 850, width = 1500)
    st.plotly_chart(Analysis_Average_fig)



def Analysis_App_opens(table_name, state):
    Analysis_Top_10_App_opens = f'''SELECT Districts, SUM(App_opens) AS App_opens
                                                    From {table_name}
                                                    WHERE States = '{state}'
                                                    GROUP BY Districts
                                                    ORDER BY  App_opens DESC
                                                    LIMIT 10;'''
    
    cursor.execute(Analysis_Top_10_App_opens)
    Analysis_Top_10_app_opens_table = cursor.fetchall()
    mydb.commit()

    col1,col2 = st.columns(2)

    with col1:
        Analysis_Top_10_app_opens_df = pd.DataFrame(Analysis_Top_10_app_opens_table, columns = ("Districts", "App_opens"))
        Analysis_Top_10_fig = px.bar(Analysis_Top_10_app_opens_df, x = "Districts", y = "App_opens", title="Top 10 Districts (App Opens)",
                                        color_discrete_sequence= px.colors.sequential.algae, height = 650, width = 800)
        st.plotly_chart(Analysis_Top_10_fig)


    Analysis_Last_10_App_opens = f'''SELECT Districts, SUM(App_opens) AS App_opens
                                                    From {table_name}
                                                    Where States = '{state}'
                                                    GROUP BY Districts
                                                    ORDER BY  App_opens
                                                    LIMIT 10;'''
    
    cursor.execute(Analysis_Last_10_App_opens)
    Analysis_Last_10_App_opens_table = cursor.fetchall()
    mydb.commit()

    with col2:
        Analysis_Last_10_app_opens_df = pd.DataFrame(Analysis_Last_10_App_opens_table, columns = ("Districts", "App_opens"))
        Analysis_Last_10_fig = px.bar(Analysis_Last_10_app_opens_df, x = "Districts", y = "App_opens", title="Last 10 Districts (App Opens)",
                                        color_discrete_sequence= px.colors.sequential.Aggrnyl_r, height = 650, width = 800)
        st.plotly_chart(Analysis_Last_10_fig)


    
    Analysis_Average_App_opens = f'''SELECT Districts, AVG(App_opens) AS App_opens
                                                    From {table_name}
                                                    WHERE States = '{state}'
                                                    GROUP BY Districts
                                                    ORDER BY  App_opens;
                                                    '''
    
    cursor.execute(Analysis_Average_App_opens)
    Analysis_Average_app_opens_table = cursor.fetchall()
    mydb.commit()

    Analysis_Average_app_opens_df = pd.DataFrame(Analysis_Average_app_opens_table, columns = ("Districts", "App_opens"))
    Analysis_Average_fig = px.bar(Analysis_Average_app_opens_df, x = "App_opens", y = "Districts", title="Average App Opens each District", orientation="h",
                                    color_discrete_sequence= px.colors.sequential.Aggrnyl_r, height = 750, width = 1500)
    st.plotly_chart(Analysis_Average_fig)


def Analysis_Total_transaction_amount(table_name):
    Transaction_amount = f'''SELECT  Years, SUM(Transaction_amount) AS Transaction_amount
                                            From {table_name}
                                            GROUP BY Years
                                            ORDER BY Years;'''
        
    cursor.execute(Transaction_amount)
    Total_transaction_amount_table = cursor.fetchall()
    mydb.commit()
    col1, col2 = st.columns(2)

    with col1:
        Total_transaction_amount_df = pd.DataFrame(Total_transaction_amount_table, columns= ("Years", "Transaction_amount"))
    
    def format_with_commas(x):
        return "{:,}".format(x)

    Total_transaction_amount_df['Transaction_amount'] = Total_transaction_amount_df['Transaction_amount'].apply(format_with_commas)
    
    st.table(Total_transaction_amount_df)


def Analysis_Total_transaction_count(table_name):
    Transaction_count = f'''SELECT  Years, SUM(Transaction_count) AS Transaction_count
                                            From {table_name}
                                            GROUP BY Years
                                            ORDER BY Years;'''
        
    cursor.execute(Transaction_count)
    Total_transaction_count_table = cursor.fetchall()
    mydb.commit()
    col1, col2 = st.columns(2)

    with col2:
        Total_transaction_count_df = pd.DataFrame(Total_transaction_count_table, columns= ("Years", "Transaction_count"))

    def format_with_commas(x):
        return "{:,}".format(x)

    Total_transaction_count_df['Transaction_count'] = Total_transaction_count_df['Transaction_count'].apply(format_with_commas)
    
    st.table(Total_transaction_count_df)


# Streamlit Part

st.set_page_config(layout = "wide")
st.title("Phonepe Data Visualization and Exploration")

with st.sidebar:

    select = option_menu("Main menu", ["Data Exploration", "Analysis"])

if select == "Data Exploration":
    
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method_1 = st.radio("Select the Method", ["Aggregated Insurance", "Aggregated Transaction", "Aggregated User"])


# Aggregated Insurance

        if method_1 == "Aggregated Insurance":

            col1, col2 = st.columns(2)
            
            with col1:
                Agg_Ins_Years = st.slider("Select the Aggregated Insurance Year", Aggregated_Insurance["Years"].min(),Aggregated_Insurance["Years"].max(),Aggregated_Insurance["Years"].min())
            Agg_ins_ica_y = Aggregated_Insurance_count_amount_year(Aggregated_Insurance, Agg_Ins_Years)


            col1, col2 = st.columns(2)

            with col1:
                Agg_Ins_Quarter = st.slider("Select the Aggregated Insurance Quarter", Agg_ins_ica_y["Quarter"].min(), Agg_ins_ica_y ["Quarter"].max(), Agg_ins_ica_y["Quarter"].min())
            Aggregated_Insurance_count_amount_year_quarter(Agg_ins_ica_y, Agg_Ins_Quarter)


# Aggregated Transaction

        elif method_1 == "Aggregated Transaction":

            col1, col2 = st.columns(2)

            with col1:
                Agg_Trans_Year = st.slider("Select the Aggregated Transaction Year", Aggregated_Transaction["Years"].min(), Aggregated_Transaction["Years"].max(), Aggregated_Transaction["Years"].min())
            Agg_trans_tca_y = Aggregated_Transaction_count_amount_year(Aggregated_Transaction,Agg_Trans_Year)


            col1, col2 = st.columns(2)

            with col1:
                Agg_Trans_Type_State = st.selectbox("Select the State", Agg_trans_tca_y["States"].unique())
            Aggregated_Transaction_Type_Year(Agg_trans_tca_y, Agg_Trans_Type_State)


            col1, col2 = st.columns(2)

            with col1:
                Agg_Trans_Quarter = st.slider("Select the Aggregated Transaction Quarter", Agg_trans_tca_y["Quarter"].min(), Agg_trans_tca_y ["Quarter"].max(), Agg_trans_tca_y["Quarter"].min())
            Agg_trans_tca_y_q = Aggregated_Transaction_count_amount_year_quarter(Agg_trans_tca_y, Agg_Trans_Quarter)


            col1, col2 = st.columns(2)

            with col1:
                Agg_Trans_Type_State = st.selectbox("Select the States", Agg_trans_tca_y["States"].unique())
            Aggregated_Transaction_Type_Year_Quarter(Agg_trans_tca_y_q, Agg_Trans_Type_State)


# Aggregated User

        elif method_1 == "Aggregated User":
            
            col1, col2 = st.columns(2)

            with col1:
                Agg_User_Year = st.slider("Select the Aggregated User Year", Aggregated_User["Years"].min(), Aggregated_User["Years"].max(), Aggregated_User["Years"].min())
            aggu_y = Aggregated_User_Transaction_Year(Aggregated_User, Agg_User_Year)

            col1, col2 = st.columns(2)

            with col1:
                Agg_User_Year_Quarter = st.slider("Select the Aggregated User Quarter", aggu_y["Quarter"].min(), aggu_y["Quarter"].max(), aggu_y["Quarter"].min())
            agguy_q = Aggregated_User_Transaction_Year_Quarter(aggu_y, Agg_User_Year_Quarter)

            col1, col2 = st.columns(2)

            with col1:
                Agg_User_State = st.selectbox("Select the State", agguy_q["States"].unique())
            Aggregated_User_Transaction_State(agguy_q, Agg_User_State)

    
    with tab2:
        method_2 = st.radio("Select the Method", ["Map Insurance", "Map Transaction", "Map User"])


# Map Insurance

        if method_2 == "Map Insurance":

            col1, col2 = st.columns(2)

            with col1:
                Map_Ins_Years = st.slider("Select the Map Insurance Years.", Map_Insurance["Years"].min(),Map_Insurance["Years"].max(),Map_Insurance["Years"].min())
            mica_y = Map_Insurance_count_amount_year(Map_Insurance, Map_Ins_Years)


            col1, col2 = st.columns(2)
            
            with col1:
                Map_ins_count_amount_year_district = st.selectbox("Select the Map Insurance by State", Map_Insurance["States"].unique())
            Map_Insurance_Count_amount_year_district(mica_y, Map_ins_count_amount_year_district)


            col1, col2 = st.columns(2)

            with col1:
                Map_Ins_quarter = st.slider("Select the Map Insurance Quarter", mica_y["Quarter"].min(), mica_y ["Quarter"].max(), mica_y["Quarter"].min())
            mica_y_q = Map_Insurance_count_amount_year_quarter(mica_y, Map_Ins_quarter)

            col1,col2 = st.columns(2)

            with col1:
                Map_ins_count_amount_year_quarter_district = st.selectbox("Select the Map Insurance by State ", Map_Insurance["States"].unique())
            Map_Insurance_count_amount_year_quarter_district(mica_y_q, Map_ins_count_amount_year_quarter_district)


# Map Transaction

        elif method_2 == "Map Transaction":

            col1, col2 = st.columns(2)

            with col1:
                Map_Trans_Year = st.slider("Select the Map Transaction Year", Map_Transaction["Years"].min(), Map_Transaction["Years"].max(), Map_Transaction["Years"].min())
            mtca_y = Map_Transaction_count_amount_year(Map_Transaction, Map_Trans_Year)


            col1, col2 = st.columns(2)

            with col1:
                Map_Trans_Year_State = st.selectbox("Select the State", Map_Transaction["States"].unique())
            Map_Transaction_Type_Year_District(mtca_y, Map_Trans_Year_State)


            col1, col2 = st.columns(2)

            with col1:
                Map_Trans_Quarter = st.slider("Select the Map Transaction Year ", mtca_y["Quarter"].min(), mtca_y["Quarter"].max(), mtca_y["Quarter"].min())          
            mtca_y_q = Map_Transaction_count_amount_year_quarter(mtca_y,Map_Trans_Quarter)


            col1, col2 = st.columns(2)

            with col1:
                Map_Trans_Quarter_State = st.selectbox("Select the State ", Map_Transaction["States"].unique())
            Map_Transaction_Type_Year_Quarter_District(mtca_y_q, Map_Trans_Quarter_State)


# Map User

        elif method_2 == "Map User":
            col1, col2 = st.columns(2)

            with col1:
                Map_Reg_User_Year = st.slider("Select the Map User Year", Map_User["Years"].min(), Map_User["Years"].max(), Map_User["Years"].min())
            mapu_y = Map_Registered_Users_Year(Map_User, Map_Reg_User_Year)

            col1, col2 = st.columns(2)

            with col1:
                Map_Reg_Users_Year_Quarter = st.slider("Select the Map User Quarter", Map_User["Quarter"].min(), Map_User["Quarter"].max(), Map_User["Quarter"].min())
            mapu_y_q = Map_Registered_Users_Year_Quarter(mapu_y, Map_Reg_Users_Year_Quarter)
                
            col1, col2 = st.columns(2)

            with col1:
                Map_Reg_User_Transaction_State = st.selectbox("Select the state", Map_User["States"].unique())
            Map_User_Transaction_State(mapu_y_q, Map_Reg_User_Transaction_State)


    with tab3:
        method_3 = st.radio("Select the Method", ["Top Insurance", "Top Transaction", "Top User"])

# Top Insurance
        
        if method_3 == "Top Insurance":
            col1, col2 = st.columns(2)

            with col1:
                Top_Ins_Years = st.slider("Select the Top Insurance Years", Top_Insurance["Years"].min(),Top_Insurance["Years"].max(),Top_Insurance["Years"].min())
            tica_y = Top_Insurance_count_amount_year(Top_Insurance,Top_Ins_Years)


            col1, col2 = st.columns(2)

            with col1:
                Top_Ins_Years_State = st.selectbox("Select the State ", tica_y["States"].unique())
            Top_Insurance_count_amount_year_district(tica_y, Top_Ins_Years_State)


            col1,col2 = st.columns(2)

            with col1:
                Top_Ins_Years_Quarter = st.slider("Select the Top Insurance Quarter", tica_y["Quarter"].min(), tica_y["Quarter"].max(), tica_y["Quarter"].min())
            tica_y_q = Top_Insurance_count_amount_year_quarter(tica_y, Top_Ins_Years_Quarter)

            

# Top Transaction

        elif method_3 == "Top Transaction":
            col1, col2 = st.columns(2)

            with col1:
                Top_Trans_Year = st.slider("Select the Top Transaction Year", Top_Transaction["Years"].min(), Top_Transaction["Years"].max(), Top_Transaction["Years"].min())
            ttca_y = Top_Transaction_count_amount_year(Top_Transaction,Top_Trans_Year)

            col1, col2 = st.columns(2)

            with col1:
                Top_Trans_Year_Areas = st.selectbox("Select the State,", Top_Transaction["States"].unique())
            Top_Transaction_Type_Year_Areas(ttca_y, Top_Trans_Year_Areas)

            col1, col2 = st.columns(2)

            with col1:
                Top_Trans_Year_Quarter = st.slider("Select the Top_Transaction Quarter", ttca_y["Quarter"].min(), ttca_y["Quarter"].max(), ttca_y["Quarter"].min())
            Top_Transaction_count_amount_year_quarter(ttca_y, Top_Trans_Year_Quarter)

# Top User

        elif method_3 == "Top User":
            col1, col2 = st.columns(2)

            with col1:
                top_user_registered_y = st.slider("Select the Year", Top_User["Years"].min(), Top_User["Years"].max(), Top_User["Years"].min())
            topu_y = Top_User_Registered_Year(Top_User, top_user_registered_y)


            col1, col2 = st.columns(2)

            with col1:
                top_user_registered_s = st.selectbox("Select the Top User Registered by State", topu_y["States"].unique())
            Top_User_Transaction_State(topu_y, top_user_registered_s)




        
elif select == "Analysis":
    Questions =st.selectbox("Select the Question", ["1. States with Top, Bottom, Avg Transactions Amount and Transaction Count for Aggregated Insurance",
                                                    "2. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Aggregated Transaction",
                                                    "3. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Map Insurance",
                                                    "4. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Map Transaction",
                                                    "5. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Top Insurance",
                                                    "6. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Top Transaction",
                                                    "7. States with Top, Bottom, Avg Transaction Count  for Aggregated User",
                                                    "8. States with Top, Bottom, Avg Registered Users based on Districts",
                                                    "9. States with Top, Bottom, Avg App openings based on Districts",
                                                    "10. Total 'Transaction Amount' and 'Transaction Count' each Year",
                                                    ])
    
    if Questions == "1. States with Top, Bottom, Avg Transactions Amount and Transaction Count for Aggregated Insurance":
        st.subheader("Transaction Amount")
        Analysis_transaction_amount("Aggregated_Insurance")
        st.subheader("Transaction Count")
        Analysis_transaction_count("Aggregated_Insurance")
    
    elif Questions == "2. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Aggregated Transaction":
        st.subheader("Transaction Amount")
        Analysis_transaction_amount("Aggregated_Transaction")
        st.subheader("Transaction Count")
        Analysis_transaction_count("Aggregated_Transaction")

    elif Questions == "3. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Map Insurance":
        st.subheader("Transaction Amount")
        Analysis_transaction_amount('Map_Insurance')
        st.subheader("Transaction Count")
        Analysis_transaction_count('Map_Insurance')
    
    elif Questions == "4. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Map Transaction":
        st.subheader("Transaction Amount")
        Analysis_transaction_amount("Map_Transaction")
        st.subheader("Transaction Count")
        Analysis_transaction_count("Map_Transaction")

    elif Questions == "5. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Top Insurance":
        st.subheader("Transaction Amount")
        Analysis_transaction_amount("Top_Insurance")
        st.subheader("Transaction Count")
        Analysis_transaction_count("Top_Insurance")
    
    elif Questions == "6. States with Top, Bottom, Avg Transactions Amount and Transaction Count  for Top Transaction":
        st.subheader("Transaction Amount")
        Analysis_transaction_amount("Top_Transaction")
        st.subheader("Transaction Count")
        Analysis_transaction_count("Top_Transaction")

    elif Questions == "7. States with Top, Bottom, Avg Transaction Count  for Aggregated User":
        st.subheader("Transaction Count")
        Analysis_transaction_count("Aggregated_User")

    elif Questions == "8. States with Top, Bottom, Avg Registered Users based on Districts":
        st.subheader("Registered Users")
        col1, col2 = st.columns(2)
        with col1:
            Reg_user_State = st.selectbox("Select the State", Map_User["States"].unique())
        Analysis_registered_users("Map_User", Reg_user_State)

        
        
    elif Questions == "9. States with Top, Bottom, Avg App openings based on Districts":
        st.subheader("App Opens")
        col1, col2 = st.columns(2)
        with col1:
            App_open_State = st.selectbox("Select the State", Map_User["States"].unique())
        Analysis_App_opens("Map_User", App_open_State)

    elif Questions == "10. Total 'Transaction Amount' and 'Transaction Count' each Year":
        col1, col2 = st.columns(2)
        with col1:
            Transaction_amount_table = st.selectbox("Select table",["1. Aggregated Insurance",
                             "2. Aggregated Transaction",
                             "3. Map Insurance",
                             "4. Map Transaction",
                             "5. Top Insurance",
                             "6. Top Transaction"])
        
        if Transaction_amount_table == "1. Aggregated Insurance":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Transaction Amount")
                Analysis_Total_transaction_amount("Aggregated_Insurance")
            with col2:
                st.subheader("Transaction Count")
                Analysis_Total_transaction_count("Aggregated_Insurance")

        elif Transaction_amount_table == "2. Aggregated Transaction":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Transaction Amount")
                Analysis_Total_transaction_amount("Aggregated_Transaction")
            with col2:
                st.subheader("Transaction Count")
                Analysis_Total_transaction_count("Aggregated_Transaction")

        elif Transaction_amount_table == "3. Map Insurance":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Transaction Amount")
                Analysis_Total_transaction_amount("Map_Insurance")
            with col2:
                st.subheader("Transaction Count")
                Analysis_Total_transaction_count("Map_Insurance")

        elif Transaction_amount_table == "4. Map Transaction":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Transaction Amount")
                Analysis_Total_transaction_amount("Map_Transaction")
            with col2:
                st.subheader("Transaction Count")
                Analysis_Total_transaction_count("Map_Transaction")

        elif Transaction_amount_table == "5. Top Insurance":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Transaction Amount")
                Analysis_Total_transaction_amount("Top_Insurance")
            with col2:
                st.subheader("Transaction Count")
                Analysis_Total_transaction_count("Top_Insurance")

        elif Transaction_amount_table == "6. Top Transaction":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Transaction Amount")
                Analysis_Total_transaction_amount("Top_Transaction")
            with col2:
                st.subheader("Transaction Count")
                Analysis_Total_transaction_count("Top_Transaction")

