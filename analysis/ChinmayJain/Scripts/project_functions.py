import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from multipledispatch import dispatch 

def load_and_process(path):

    # Method Chain 1 (Load data and deal with missing data)

    df1 = (
        pd.DataFrame(
            pd.read_csv(path)
        )
        .dropna(axis=0)
        #.shape()
    )
    # Method Chain 2 (Create new columns, drop others, and do processing)

    df2 = (
        df1
        .drop(
            columns = ['wins', 'draws', 'loses','scored', 'missed','npxG', 'xG_diff', 'xGA_diff', 'npxGA', 'npxGD', 'xpts', 'xpts_diff']
        )
        .rename(
            columns={'Unnamed: 0': 'League', 'Unnamed: 1':'Year'}
        )
        .set_index(
            'League'
        )
        .drop(
            'RFPL'
        )
        .reset_index()
    )

    # Make sure to return the latest dataframe

    return df2

#This is a function has takes the league and position as parameters and filters the dataframe by those parameters and calculates the average.
#creates a dataframe of the given league and only has teams of a certain position
#Returns the average of each metric as a list
@dispatch(str, int, str)
def data_filter(league, pos, path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["League"]==league]
        )
    df3 = df2[df2['position']==pos]
    #We get the average of all the metrics in our dataframe
    av = {'League':league+"_topTeam", 'pts': df3['pts'].mean(), 'xG':df3['xG'].mean(), 'xGA':df3['xGA'].mean(), 'ppda_coef':df3['ppda_coef'].mean(), 'oppda_coef':df3['oppda_coef'].mean(), 'deep':df3['deep'].mean(), 'deep_allowed':df3['deep_allowed'].mean()}
    return av

#This is a function has takes the position as a parameter and filters the dataframe by the position.
#Returns a dataframe that only has teams of a certain position from all leagues and all years
@dispatch(int,str)
def data_filter(pos, path):
    df1 = load_and_process(path)
    df2 = df1[df1['position']==pos]
    
    return df2

#This is a function has takes the league as a parameter and filters the dataframe by the league.
#Returns a dataframe of the given league for all years and all positions are included
@dispatch(str, str)
def data_filter(league,path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["League"]==league]
        )
    #dropping the extra columns that we don't need
    df2 = df2.drop(
        columns = ['Year', 'position', 'team', 'matches']
    )
    #getting the average for each metric in our dataframe
    av = {'League':league, 'pts': df2['pts'].mean(), 'xG':df2['xG'].mean(), 'xGA':df2['xGA'].mean(), 'ppda_coef':df2['ppda_coef'].mean(), 'oppda_coef':df2['oppda_coef'].mean(), 'deep':df2['deep'].mean(), 'deep_allowed':df2['deep_allowed'].mean()}
    
    return av

def weighted_av_league(path):
    #we are creating a dataframe has the average values of each metric for each league
    #find the average values for each league and append them to new dataframe
    df_av = pd.DataFrame(data_filter("La_liga", path), index=[0])
    df_av = df_av.append(data_filter("EPL", path), ignore_index=True)
    df_av = df_av.append(data_filter("Bundesliga", path), ignore_index=True)
    df_av = df_av.append(data_filter("Serie_A", path), ignore_index=True)
    df_av = df_av.append(data_filter("Ligue_1", path), ignore_index=True)
    
    #We are calculating an Offensive and Defensive Weighted Average and adding these values as a new column
    #Offensive Metrics: xG, ppda_coef, deep
    #Defensive Metrics: xGA, oppda_coef, deep_allowed
    df_av['Offensive W_Average'] = 0.45*df_av['xG'] + 0.25*df_av['ppda_coef'] + 0.3*df_av['deep']
    df_av['Defensive W_Average'] = 0.4*df_av['xGA'] + 0.3*df_av['oppda_coef'] + 0.3*df_av['deep_allowed']
    
    return df_av

def weighted_av_top(path):
    #we are creating that has the average values of each metric for the winners of each league
    #find the average values for the winners of each league and add them into a new dataframe
    df_top = pd.DataFrame(data_filter("La_liga",1, path), index=[0])
    df_top = df_top.append(data_filter("EPL",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Bundesliga",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Serie_A",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Ligue_1",1, path), ignore_index=True)
    
    #We are calculating an Offensive and Defensive Weighted Average and adding these values as a new column
    #Offensive Metrics: xG, ppda_coef, deep
    #Defensive Metrics: xGA, oppda_coef, deep_allowed
    df_top['Offensive W_Average'] = 0.45*df_top['xG'] + 0.25*df_top['ppda_coef'] + 0.3*df_top['deep']
    df_top['Defensive W_Average'] = 0.4*df_top['xGA'] + 0.3*df_top['oppda_coef'] + 0.3*df_top['deep_allowed']
    
    return df_top

def weighted_av(path):
    #we are creating a dataframe has the average values of each metric for each league
    #find the average values for each league and append them to new dataframe
    df_av = pd.DataFrame(data_filter("La_liga", path), index=[0])
    df_av = df_av.append(data_filter("EPL", path), ignore_index=True)
    df_av = df_av.append(data_filter("Bundesliga", path), ignore_index=True)
    df_av = df_av.append(data_filter("Serie_A", path), ignore_index=True)
    df_av = df_av.append(data_filter("Ligue_1", path), ignore_index=True)
    
    #We are calculating an Offensive and Defensive Weighted Average and adding these values as a new column
    #Offensive Metrics: xG, ppda_coef, deep
    #Defensive Metrics: xGA, oppda_coef, deep_allowed
    df_av['Offensive W_Average'] = 0.45*df_av['xG'] + 0.25*df_av['ppda_coef'] + 0.3*df_av['deep']
    df_av['Defensive W_Average'] = 0.4*df_av['xGA'] + 0.3*df_av['oppda_coef'] + 0.3*df_av['deep_allowed']
    
    #drop the rest of the columns that we don't need, just keep the weighted averages
    df_av = df_av.drop(columns = ['pts', 'xG', 'xGA', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed'])
    
    #we are creating that has the average values of each metric for the winners of each league
    #find the average values for the winners of each league and add them into a new dataframe
    df_top = pd.DataFrame(data_filter("La_liga",1, path), index=[0])
    df_top = df_top.append(data_filter("EPL",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Bundesliga",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Serie_A",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Ligue_1",1, path), ignore_index=True)
    
    #We are calculating an Offensive and Defensive Weighted Average and adding these values as a new column
    #Offensive Metrics: xG, ppda_coef, deep
    #Defensive Metrics: xGA, oppda_coef, deep_allowed
    df_top['Offensive W_Average'] = 0.45*df_top['xG'] + 0.25*df_top['ppda_coef'] + 0.3*df_top['deep']
    df_top['Defensive W_Average'] = 0.4*df_top['xGA'] + 0.3*df_top['oppda_coef'] + 0.3*df_top['deep_allowed']
    
    #drop the rest of the columns that we don't need, just keep the weighted averages
    df_top = df_top.drop(columns = ['pts', 'xG', 'xGA', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed'])
    
    #joing the two dataframes into a new dataframe
    df=pd.concat([df_top,df_av])
    
    #sort the joined dataframe so that each league and league winners are beside each other
    df = df.sort_values(by=['League'], ignore_index=True)
    
    return df
    
    


    