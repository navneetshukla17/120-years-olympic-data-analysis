import numpy as np


def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year=='OverAll' and country=='OverAll':
        temp_df=medal_df
    if year=='OverAll' and country!='OverAll':
        flag = 1
        temp_df=medal_df[medal_df['region']==country]
    if year!='OverAll' and country=='OverAll':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='OverAll' and country!='OverAll':
        temp_df=medal_df[(medal_df['Year']==int(year))&(medal_df['region']==country)]
    
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    
    return x
    
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'OverAll')
    
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'OverAll')
    
    return years, country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport!='OverAll':
        temp_df = temp_df[temp_df['Sport']==sport]
    x = temp_df[['Name','Sport','region']].value_counts().reset_index().head(15)
    x=x.rename(columns={'count':'Medals','region':'Region'})
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby(by=['Year']).count()['Medal'].reset_index()
    
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    
    new_df = temp_df[temp_df['region']==country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region']==country]
    x = temp_df[['Name','Sport']].value_counts().reset_index().head(15)
    x=x.rename(columns={'count':'Medals','region':'Region'})
    return x