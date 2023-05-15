#%% Paqueterias
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.offline as pyo
#%% Read Covid-19 dataset from github
df =  pd.read_csv('https://raw.githubusercontent.com/shinokada/covid-19-stats/master/data/daily-new-confirmed-cases-of-covid-19-tests-per-case.csv')
print(df.head())
print(df.shape)
# %% prepare data
# setting shorter names of the columns
df.columns = ['Countries', 'Code','Date','Avg Daily Confirmed',
              'Days to first 30 Cases']

## Excluding Data aggregated at world, continent and other groups

excludes = ['World', 'Africa', 'North America', 'South America', 'Asia', 'Europe', 'European Union', 'High income','Low income',
            'Lower middle income','Oceania','Upper middle income', 'World excl. China',
            'World excl. China and South Korea','World excl. China, South Korea, Japan and Singapore','International',
            'Asia excl. China']
df = df[~df['Countries'].isin(excludes)]

## Converting column from string to date
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
print(df.head())

# %% When did Covid-19 started
## We can look at the dates when the total confirmed cases initially 
## reached 30 per day across countries

## Create a scatter plot, having the x-axis representing the date on which 
## the frist 30 cases were touched and the y-axis repreenting the average daily 
## confirmed cases in that day

# to get the date on which 30 caseswere reached for the first time

date_df = df[df['Days to first 30 Cases']==0]

## Creating scatter plot with plotly

fig = px.scatter(date_df,x='Date',y='Avg Daily Confirmed',hover_name='Countries',
                 color = 'Countries')

fig.update_layout({
    'plot_bgcolor':'rgba(0,0,0,0)',
    'paper_bgcolor':'rgba(0,0,0,0)',
    'title': 'Date of crossing first 30 Cases'
})

fig.show()

# %% How it spread over time

## Create a line chart where each line represents a country 
## it shows how the average daily confirmed cases varied over time

fig = px.line(df, x='Date',y='Avg Daily Confirmed',color = 'Countries')

fig.update_layout({
    'plot_bgcolor':'rgba(0,0,0,0)',
    'paper_bgcolor':'rgba(0,0,0,0)',
    'title': 'Count of Avg. Confirmed Cases'
})

fig.show()
# %% Countries with the Most Number of Cases
## Top 10 countries with the most Number of Cases

## Creates a bar chart with countries on the X-axis and total confirmed
## cases in the Y-axis

total_confirmed = df.groupby(['Countries'])['Avg Daily Confirmed'].sum().reset_index()
total_confirmed.columns = ['Countries','Total Confirmed Cases']
top_confirmed = total_confirmed.sort_values(by = ['Total Confirmed Cases'],ascending=False)[:10]

fig = px.bar(top_confirmed,x='Countries', y = 'Total Confirmed Cases')

fig.update_layout({
    'plot_bgcolor':'rgba(0,0,0,0)',
    'paper_bgcolor':'rgba(0,0,0,0)',
    'title': 'Countries with the most number of Confirmed Cases'
})

fig.show()
# %% Animation. How it spread in countries with the most cases

## 1.- Dataset preparation
## 2.- Setting the layout of the graph 
## 3.- Adding trace/ line for each country
## 4.- Adding animation frames

## Preparing the data

includes = ['United States','Russia', 'India','Brazil','United Kingdom']
includes = ['United States']
df_mar_may = df[(df['Date']>'2020-03-01') & (df['Date'] <'2020-06-14')]
df_mar_may.columns = ['Countries','Code','Date','confirmed','days_since_confirmed']
df_us=df_mar_may[df_mar_may['Countries'].isin(includes)]

includes = ['India']
df_ind=df_mar_may[df_mar_may['Countries'].isin(includes)]

includes = ['Brazil']
df_brazil=df_mar_may[df_mar_may['Countries'].isin(includes)]

includes = ['Russia']
df_rus=df_mar_may[df_mar_may['Countries'].isin(includes)]

includes = ['United Kingdom']
df_uk=df_mar_may[df_mar_may['Countries'].isin(includes)]

## 2. setting the layout
fig = go.Figure(
       layout=go.Layout(
        xaxis=dict(range=[-5, 100], autorange=False),
        yaxis=dict(range=[7, 31950], autorange=False),
        title="Confirmed Covid Cases (2nd March'20 - 13th June'20)",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                         args = [None] )])]
)
) #2

fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'xaxis_title': 'Days since confirmed cases first reached 30 per day',
'yaxis_title': "Daily confirmed cases (7-day average)" })

# 3. Add traces - one line for each country
init = 1

fig.add_trace(
    go.Scatter(x=df_us.days_since_confirmed[:init],
               y=df_us.confirmed[:init],
               name="US",
               visible=True,
               line=dict(color="#33CFA5", )))


fig.add_trace(
    go.Scatter(x=df_ind.days_since_confirmed[:init],
               y=df_ind.confirmed[:init],
               name="India",
               visible=True,
               line=dict(color="#bf00ff"),))

fig.add_trace(
    go.Scatter(x=df_brazil.days_since_confirmed[:init],
               y=df_brazil.confirmed[:init],
               name="Brazil",
               visible=True,
               line=dict(color="#33C7FF"),
              ))

fig.add_trace(
    go.Scatter(x=df_rus.days_since_confirmed[:init],
               y=df_rus.confirmed[:init],
               name="Russia",
               visible=True,
               line=dict(color="#FF5733"),
              ))

fig.add_trace(
    go.Scatter(x=df_uk.days_since_confirmed[:init],
               y=df_uk.confirmed[:init],
               name="United Kingdom",
               visible=True,
               line=dict(color="#6E6E6E"),
              ))

# 4. Animation
fig.update(frames=[
    go.Frame(
        data=[
            go.Scatter(x=df_us.days_since_confirmed[:k], y=df_us.confirmed[:k]),
            go.Scatter(x=df_ind.days_since_confirmed[:k], y=df_ind.confirmed[:k]),
         go.Scatter(x=df_brazil.days_since_confirmed[:k], y=df_brazil.confirmed[:k]),
            go.Scatter(x=df_rus.days_since_confirmed[:k], y=df_rus.confirmed[:k]),
            go.Scatter(x=df_uk.days_since_confirmed[:k], y=df_uk.confirmed[:k]),
        ]
        
    )
    for k in range(init, len(df_us)+1)])

# Extra Formatting
fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=10)
fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=1)
fig.update_layout(yaxis_tickformat=',')
fig.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")


fig.show()
