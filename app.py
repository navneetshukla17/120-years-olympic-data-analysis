import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


# datasets
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
# st.sidebar.image('/home/tusharshukla/ML/7. EDA/olympic-analysis-project/olympic games design in_6517310.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    
    selected_years = st.sidebar.selectbox('Select Years', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    
    medal_tally = helper.fetch_medal_tally(df,selected_years,selected_country)
    
    if selected_years=='OverAll' and selected_country=='OverAll':
        st.title('OverAll Taly')
    if selected_years!='OverAll' and selected_country=='OverAll':
        st.title('Medal Tally in '+str(selected_years)+" Olympics")
    if selected_years=='OverAll' and selected_country!='OverAll':
        st.title('OverAll Performance of '+selected_country)
    if selected_years!='OverAll' and selected_country!='OverAll':
        st.title('OverAll Performance of '+selected_country+' In '+str(selected_years)+' Olympics') 
    
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athlete = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hots')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athlete)

nations_over_time = helper.data_over_time(df,'region')
st.title('Participating Nations Over The Years')
fig = px.line(nations_over_time, x='Year', y='count')
st.plotly_chart(fig)

events_over_time = helper.data_over_time(df,'Event')
st.title('Events Over The Years')
fig = px.line(events_over_time, x='Year', y='count')
st.plotly_chart(fig)

athletes_over_time = helper.data_over_time(df,'Name')
st.title('Athletes Over The Years')
fig = px.line(athletes_over_time, x='Year', y='count')
st.plotly_chart(fig)

st.title('No. Of Events Over time(Every Sport)')
fig, ax = plt.subplots(figsize=(20,20))
x = df.drop_duplicates(['Year','Sport','Event'])
sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
st.pyplot(fig)

st.title('Most Successfull Athletes')

sport_list = df['Sport'].unique().tolist()
sport_list.sort()
sport_list.insert(0,'OverAll')

selected_sport = st.selectbox('Select a Sport',sport_list)

x = helper.most_successful(df,selected_sport)
st.table(x)

if user_menu=='Country-wise Analysis':
    
    st.sidebar.title('Country Wise Analysis')
    
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0,'OverAll')
    
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country + ' Medal Tally Over The Years')
    st.plotly_chart(fig)
    
    if selected_country=='OverAll':
        st.text('Select a country a see the Results....')
    else:
        
        st.title(selected_country + ' excels in the following sports')
        pt = helper.country_event_heatmap(df,selected_country)
        fig, ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)
    
    if selected_country=='OverAll':
        st.header('Select a country a see the Results....')
    else:
        st.title('Top 10 athletes of '+selected_country)
        top_10_df = helper.most_successful_countrywise(df,selected_country)
        st.table(top_10_df)

if user_menu=='Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Athlete's Age")
    st.plotly_chart(fig)

famous_sports = df[df['Medal']=='Gold']['Sport']
famous_sports.drop_duplicates()
athlete_df = df.drop_duplicates(subset=['Name','region'])

# x = []
# name = []
# for sport in famous_sports:
#     temp_df = athlete_df[athlete_df['Sport']==sport]
#     x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
#     name.append(sport)

# fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
# fig.update_layout(autosize=False,width=1000,height=600)
# st.title('Distribution of Age ')
# st.plotly_chart(fig)
