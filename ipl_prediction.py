# -*- coding: utf-8 -*-
"""ipl_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LdXfIFMn8EDV6Qh2gkaz_3N8Xsh5r3WC
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import cufflinks as cf
cf.go_offline()
import plotly.graph_objects as go
import plotly.express as px

balls = pd.read_csv('/content/IPL_Ball_by_Ball_2008_2022.csv')
balls.shape

matches = pd.read_csv('/content/IPL_Matches_2008_2022.csv')
matches.shape

balls.head()

x=balls['batsman_run']
y=balls['total_run']
plt.scatter(x,y)

balls.info()

balls.describe()

matches.head()

matches.info()

matches['City'].value_counts().plot()

total_score = balls.groupby(['ID', 'innings']).sum()['total_run'].reset_index()

total_score.head()

total_score = total_score[total_score['innings']==1]

total_score.head()

sns.countplot(matches['Season'])
plt.xticks(rotation=90, fontsize=10)
plt.yticks(rotation=45,fontsize=10)
plt.xlabel('Season', fontsize=10)
plt.ylabel('Count', fontsize=10)
plt.title('Total matches played in each season', fontsize = 10, fontweight = "bold")

ax = plt.axes()
ax.set(facecolor = "pink")
sns.countplot(x='Season', hue='TossDecision', data=matches,palette="magma",saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(rotation=45,fontsize=15)
plt.xlabel('\n Season',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.title('Toss decision across seasons',fontsize=12,fontweight="bold")
plt.show()

matches['WonBy'].value_counts()

match_per_season = matches.groupby(['Season'])['ID'].count().reset_index().rename(columns={'ID':'matches'})
match_per_season

season_data=matches[['ID','Season']].merge(balls, left_on = 'ID', right_on = 'ID', how = 'left').drop('ID', axis = 1)
season_data.head()

matches.Venue[matches.WonBy!='runs'].mode()

matches.Venue[matches.WonBy!='wickets'].mode()

matches.WinningTeam[matches.WonBy!='wickets'].mode()

toss = matches['TossWinner'] == matches['WinningTeam']
plt.figure(figsize=(10,5))
sns.countplot(toss)
plt.show()

player = (balls['batter']=='SK Raina')
df_raina=balls[player]
df_raina.head()

def count(df_raina,runs):
    return len(df_raina[df_raina['batsman_run']==runs])*runs

print("Runs scored from 1's :",count(df_raina,1))
print("Runs scored from 2's :",count(df_raina,2))
print("Runs scored from 3's :",count(df_raina,3))
print("Runs scored from 4's :",count(df_raina,4))
print("Runs scored from 6's :",count(df_raina,6))

runs = balls.groupby(['batter'])['batsman_run'].sum().reset_index()
runs.columns = ['Batsman' , 'runs']
y = runs.sort_values(by='runs',ascending = False).head(10).reset_index().drop('index',axis=1)
print(y)

ax = plt.axes()
ax.set(facecolor = "grey")
sns.barplot(x=y['Batsman'],y=y['runs'],palette='rocket',saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('\n Player',fontsize=15)
plt.ylabel('Total Runs',fontsize=15)
plt.title('Top 10 run scorers in IPL',fontsize=15,fontweight="bold")

ax = plt.axes()
ax.set(facecolor = "black")
matches.Player_of_Match.value_counts()[:10].plot(kind='bar')
plt.xlabel('Players')
plt.ylabel("Count")
plt.title("Highest MOM award winners",fontsize=15,fontweight="bold")

temp = pd.DataFrame({"WinningTeam":matches["WinningTeam"]})
count_wins = temp.value_counts()
labels = [X[0] for X in count_wins.keys()]
bar , ax = plt.subplots(figsize =(14,15))
ax = plt.pie(x = count_wins, autopct = "%.1f%%" ,labels = labels)
plt.title("Most Wins in IPL",fontsize = 17,fontweight="bold")
plt.show()

plt.figure(figsize=(7,7))
plt.hist(df_raina['batsman_run'])
plt.show()

"""total_score['target'] = total_score['total_run'] + 1"""

total_score['target'] = total_score['total_run'] + 1

match_df = matches.merge(total_score[['ID','target']], on='ID')

match_df.head()

match_df['Team1'].unique()

teams = [
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad', 
    'Delhi Capitals', 
    'Chennai Super Kings',
    'Gujarat Titans', 
    'Lucknow Super Giants', 
    'Kolkata Knight Riders',
    'Punjab Kings', 
    'Mumbai Indians'
]

match_df['Team1'] = match_df['Team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['Team2'] = match_df['Team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')

match_df['Team1'] = match_df['Team1'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['Team2'] = match_df['Team2'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')


match_df['Team1'] = match_df['Team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['Team2'] = match_df['Team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

match_df = match_df[match_df['Team1'].isin(teams)]
match_df = match_df[match_df['Team2'].isin(teams)]
match_df = match_df[match_df['WinningTeam'].isin(teams)]

match_df.shape

match_df.columns

match_df['method'].unique()

match_df['method'].value_counts()

match_df = match_df[match_df['method'].isna()]

match_df.shape

match_df.columns

match_df = match_df[['ID','City','Team1','Team2','WinningTeam','target']].dropna()

match_df.head()

match_df.isna().sum()

balls.columns

balls['BattingTeam'] = balls['BattingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

balls = balls[balls['BattingTeam'].isin(teams)]

balls_df = match_df.merge(balls, on='ID')

balls_df.head()

balls_df['BattingTeam'].value_counts()

balls_df.columns

balls_df = balls_df[balls_df['innings']==2]

balls_df.shape

balls_df.head()

balls_df.columns

balls_df['current_score'] = balls_df.groupby('ID')['total_run'].cumsum()

balls_df

balls_df['runs_left'] = np.where(balls_df['target']-balls_df['current_score']>=0, balls_df['target']-balls_df['current_score'], 0)

balls_df

balls_df['balls_left'] = np.where(120 - balls_df['overs']*6 - balls_df['ballnumber']>=0,120 - balls_df['overs']*6 - balls_df['ballnumber'], 0)

balls_df['wickets_left'] = 10 - balls_df.groupby('ID')['isWicketDelivery'].cumsum()

balls_df.columns

balls_df['current_run_rate'] = (balls_df['current_score']*6)/(120-balls_df['balls_left'])

balls_df['required_run_rate'] = np.where(balls_df['balls_left']>0, balls_df['runs_left']*6/balls_df['balls_left'], 0)

balls_df.columns

def result(row):
    return 1 if row['BattingTeam'] == row['WinningTeam'] else 0

balls_df['result'] = balls_df.apply(result, axis=1)

balls_df.head()

balls_df.columns

index1 = balls_df[balls_df['Team2']==balls_df['BattingTeam']]['Team1'].index
index2 = balls_df[balls_df['Team1']==balls_df['BattingTeam']]['Team2'].index

balls_df.loc[index1, 'BowlingTeam'] = balls_df.loc[index1, 'Team1']
balls_df.loc[index2, 'BowlingTeam'] = balls_df.loc[index2, 'Team2']

balls_df.head()

final_df = balls_df[['BattingTeam', 'BowlingTeam','City','runs_left','balls_left','wickets_left','current_run_rate','required_run_rate','target','result']]

final_df.head()

fig = plt.hist(final_df[final_df['runs_left']>0]['runs_left'], bins=30,)

plt.hist(final_df['wickets_left'].value_counts())

fig = plt.hist(final_df['target'], bins=30)

final_df.describe()

final_df.isna().sum()

final_df.shape

final_df.sample(final_df.shape[0])

final_df.sample()

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

trf = ColumnTransformer([
    ('trf', OneHotEncoder(sparse=False,drop='first'),['BattingTeam','BowlingTeam','City'])
],
remainder = 'passthrough')

from sklearn.model_selection import train_test_split

X = final_df.drop('result', axis=1)
y = final_df['result']
X.shape, y.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

pipe = Pipeline(steps=[
    ('step1',trf),
    ('step2',LogisticRegression())
])

pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy_score(y_pred, y_test)

pipe.predict_proba(X_test)

teams

final_df['City'].unique()

toss=match_df['target'].value_counts()
ax = plt.axes()
ax.set(facecolor = "grey")
sns.set(rc={'figure.figsize':(15,10)},style='darkgrid')
ax.set_title('No. of tosses won by each team',fontsize=15,fontweight="bold")
sns.barplot(y=toss.index, x=toss, orient='h',palette="icefire",saturation=1)
plt.xlabel('# of tosses won')
plt.ylabel('Teams')
plt.show()

toss=final_df['result'].value_counts()
ax = plt.axes()
ax.set(facecolor = "grey")
sns.set(rc={'figure.figsize':(15,10)},style='darkgrid')
ax.set_title('Result ',fontsize=15,fontweight="bold")
sns.barplot(y=toss.index, x=toss, orient='h',palette="icefire",saturation=1)
plt.xlabel('won')
plt.ylabel('Teams')
plt.show()

toss =matches['TossWinner'] == matches['WinningTeam']
plt.figure(figsize=(10,5))
sns.countplot(toss)
plt.show()

season=matches.groupby(['Season'])['Margin'].sum().reset_index()
p=season.set_index('Season')
ax = plt.axes()
ax.set(facecolor = "grey")
sns.lineplot(data=p,palette="magma") 
plt.title('Total runs in each season',fontsize=12,fontweight="bold")
plt.show()

import pickle
pickle.dump(pipe, open('pipe.pkl','wb'))

X_train

y_train

