import pandas as pd
from multipledispatch import dispatch
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_process(path):

    # Method Chain 1 (Load data and deal with missing data)
    df1 = (
        pd.read_csv(path
        )#reads data file from the given path
        .dropna(axis=0
        )#drop na values
    )

    # Method Chain 2 (Create new columns, drop others, and do processing)
    df2 = (
          df1
    .assign(pts_per_game = lambda df: df['pts']/df['matches']
    )#adds a new column by calculating the points per game
    .drop(columns=['xGA_diff','npxG','npxGD','npxGA','wins','draws','loses','xpts_diff','xG_diff','deep','deep_allowed']
    )#drops 'xGA_diff','npxG','npxGD','npxGA','wins','draws','loses','xpts_diff','xG_diff','deep','deep_allowed' columns
    .rename(columns={'Unnamed: 0' :'league','Unnamed: 1':'year','missed':'conceded','ppda_coef':'pressure','oppda_coef':'oppo_pressure'}
    )#renames few columns to increase readability
    .set_index('league'
    )#setting index to league to drop 'RFPL' league
    .drop('RFPL'
    )#drops 'RFL'
    .reset_index(
    )#resets index to numbers
    )

    #function returns the latest dataframe
    return df2

def all_cases(path):
    
    leagues=['EPL','Serie_A','Ligue_1','La_liga']
    df1=[]
    k=0
    
    for l in leagues:
        for i in range(2014,2020):
            df=df1
            if(k == 0):
                df1= filter_data_set(l,i,path)
                k=k+1
            else:
                df1= filter_data_set(l,i,path)
                df1=pd.concat([df,df1])
            
    #df1.to_csv (r'../data/processed/processed_all_cases.csv', index = False, header=True)
    
    return df1


#method to plot 3d pie charts
def plot_pie(values, labels):
    
    #adds the explode effect to the 3d pie chart
    explode = (0, 0.1, 0)
    
    #add colors
    colors = ['#ff9999','#99ff99', '#B7C3F3', '#DD7596']
    
    #set up the pie chart by using the passed parameters of values and labels
    fig1, ax1 = plt.subplots()
    ax1.pie(values, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',shadow=True, startangle=30)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    
    #print the 3d pie chart
    plt.tight_layout()
    

#method to find out team's effect on opponent
def weighted_avg_attack(league,year,path):   
    
    #method call to show only those teams from a specific year and league that have higher xG than the winning team
    df= filter_data_set(league,year,path)

    #according to corelation matrix, weight of pressure, xG, scored is 0.24, 0.37, 0.39 respectively
    #calculates the weighted attacking average
    avg= ((df['pressure'])*0.24 + (df['xG'])*0.37 + (df['scored'])*0.39)
    
    #creates a new dataframe along with the required teams
    team= df['team']
    position= df['position']
    l = df['league']
    y = df['year']
    data = list(zip(team, position, avg,l,y))
    df1= pd.DataFrame(data,columns=['team','position','avg','league','year'])
    
    return df1
    
#method to find out opponent's effect on team    
def weighted_avg_def(league, year, path):
    
    #colors2 = ['#99ff99']
    
    #method call to show only those teams from a specific year and league that have higher xG than the winning team
    df= filter_data_set(league,year,path)
    
    #according to corelation matrix, weight of oppo_pressure, xGA, conceded is 0.28, 0.34, 0.38 respectively
    avg=((df['oppo_pressure'])*0.28 + (df['xGA'])*0.34 + (df['conceded'])*0.38)
    
    #creates a new dataframe along with the required teams
    team= df['team']
    position= df['position']
    l = df['league']
    y = df['year']
    data=list(zip(team, position, avg,l,y))
    df3=pd.DataFrame(data,columns=['team','position','avg','league','year'])
    
    return df3
    
#method to find out team's net effect
def weighted_avg_net(league, year, path):
    
    #method call to show only those teams from a specific year and league that have higher xG than the winning team
    df= filter_data_set(league,year,path)
    
    #plotting for the net average (team's effect - opponent's effect)
    #creates a new dataframe along with the required teams
    team= df['team']
    position= df['position']
    l = df['league']
    y = df['year']
    
    df1= weighted_avg_attack(league,year,path)
    df3= weighted_avg_def(league,year,path)
          
    a=df1['avg']
    b=df3['avg']
    
    net=a-b
    
    data=list(zip(team, position, net,l,y))
    df3=pd.DataFrame(data,columns=['team','position','net','league','year'])
    
    return df3

#method to concatenate the weighted team's effect into a single dataframe
def all_avg_attack(path):
    
    leagues=['EPL','Serie_A','Ligue_1','La_liga']
    df1=[]
    k=0
    
    for l in leagues:
        for i in range(2014,2020):
            df=df1
            if(k == 0):
                df1= weighted_avg_attack(l,i,path)
                k=k+1
            else:
                df1= weighted_avg_attack(l,i,path)
                df1=pd.concat([df,df1])

    #df1.to_csv (r'../data/processed/processed_avg_attack.csv', index = False, header=True)
    
    return df1


#method to concatenate the weighted opponent's effect into a single dataframe
def all_avg_def(path):
    
    leagues=['EPL','Serie_A','Ligue_1','La_liga']
    df1=[]
    k=0
    
    for l in leagues:
        for i in range(2014,2020):
            df=df1
            if(k == 0):
                df1= weighted_avg_def(l,i,path)
                k=k+1
            else:
                df1= weighted_avg_def(l,i,path)
                df1=pd.concat([df,df1])
            
    #df1.to_csv (r'../data/processed/processed_avg_def.csv', index = False, header=True)
    
    return df1


#method to concatenate the weighted net effect of team into a single dataframe
def all_avg_net(path):
    
    leagues=['EPL','Serie_A','Ligue_1','La_liga']
    df1=[]
    k=0
    
    for l in leagues:
        for i in range(2014,2020):
            df=df1
            if(k == 0):
                df1= weighted_avg_net(l,i,path)
                k=k+1
            else:
                df1= weighted_avg_net(l,i,path)
                df1=pd.concat([df,df1])
            
    #df1.to_csv (r'../data/processed/processed_avg_net.csv', index = False, header=True)
    
    return df1


#method to plot the pie chart using the values
def pie_def(parameters,oppo_effect_weights):
    
    data=list(zip(parameters,oppo_effect_weights))
    df1=pd.DataFrame(data,columns=['parameter','weight'])
    
    #display(df1)
    return df1

#method to plot the pie chart using the values
def pie_attack(parameters,team_effect_weights):
    
    data=list(zip(parameters,team_effect_weights))
    df1=pd.DataFrame(data,columns=['parameter','weight'])
    
    #display(df1)
    return df1


#method to drop columns and keep those variables that are involved in the team's effect on opponent calculation
def team_effect_parameters(df):
    df=df.drop(columns=['pts','year','matches','league','pts_per_game','conceded','oppo_pressure','xpts','xGA'])
    return df


#method to drop columns and keep those variables that are involved in the opponent's effect on team calculation
def opponent_effect_parameters(df):
    df= df.drop(columns=['pts','year','matches','league','pts_per_game','xG','xpts','scored','pressure'])
    return df


#method to show only those teams from a specific year and league that have higher xG than the winning team
def filter_data_set(league, year, path):
    
    #clean and format the data before working on it
    df= load_and_process(path)
    
    #conditions to extract the data from a specific league and year
    df1=df[df['year']==year]
    df2=df1[df1['league']==league]
    df3=df2[df2['position']==1]
    
    #makes a new list with all the xG values so that xG values can be compared
    xG=[]
    a= (float)(df3['xG'])
    xG.append(a)
    for i in range(0,19):
        xG.append(a)
    
    #returns only those teams in the year and league that have xG greater than the winning team
    df4=df2[df2['xG'].values >= xG]
        
    return df4

#method to plot bar graphs
def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True, chart_value=None):
    
    #list contains the positions of all the teams from the data that is passed
    list=[]
    
    #x_pos contains the names of all teams in the order to label the axis of the plot properly
    if chart_value <=2:
        data=data
    else:
        data=data.data
    
    #data= data.data
    x_pos= data['team']
    for i in range(0,len(data['position'])):
        list.append(i)
    s= pd.Series(list)
    
    #condition to drop the required parameters according to the requirements of the graph
    if chart_value == 1:
        data= team_effect_parameters(data)
        plt.title('Team\'s effect on opponent (xG, scored, pressure)')
    elif chart_value == 2:
        data= opponent_effect_parameters(data)
        plt.title('Opponent\'s effect on team (xGA, conceded, oppo_pressure)')
    else:
        data=data
        
        
    if chart_value <=2:
        data= data.drop(columns=['team','position'])
    else:
        data= data.drop(columns=['team','position','league','year'])
    #data= data.drop(columns=['team','position','league','year'])
    
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())
    
    plt.xticks(s,x_pos)
    
    #adds proper label to the plot in order to increase readability
    plt.xlabel('Teams')
    plt.ylabel('Values')
    
    plt.rcParams['figure.figsize']= (10,6)
    plt.rcParams['font.family'] = 'serif'
    
    sns.despine()

    #Citation: https://stackoverflow.com/questions/14270391/python-matplotlib-multiple-bars/14270539

    
#method to extract data for a specific league and year
@dispatch(str,int, str)
def data_filter(league,year, path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["league"]==league]
        )
    df3 = df2[df2["year"]==year]
    
    return df3


#method to extract data for a specific league only
@dispatch(str,str)
def data_filter(league, path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["league"]==league]
        )
    
    return df2

#method to extract data of teams that have the same position as the passed parameter
@dispatch(int,str)
def data_filter(pos, path):
    df1 = load_and_process(path)
    df2 = df1[df1['position']==pos]
    
    return df2
