import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

# Reading The Dataset and Doing any Transformations Required by The Figures

data = pd.read_csv('https://gist.githubusercontent.com/ThiagoFPMR/' +
                             'fea32b8082a54889ba7470ac63252299/raw/' +
                             'aea145700257ffa89d924073189a0e3804bd987c/' +
                             'covid_worldwide.csv')

def drop_outliers (country):
  if country in ['Brazil', 'United States', 'India', 'China']:
    return None
  else:
    return country

data2 = data.copy()
data2.country = data2.country.apply(drop_outliers)
data2 = data2[data2.country.notnull()]

data3 = data2.groupby(by='income_group').sum().reset_index()

# Defining the figures that will be used for the Dash app

fig1 = px.scatter(data2,
                 x='expected_years_of_school',
                 y=data2.total_cases/data2.population,
                 size='population',
                 color='income_group',
                 hover_name='country',
                 template='plotly_white',
                 labels={'expected_years_of_school':'Expected Years of School',
                         'y': 'Percentage Infected'},
                 title='Total Cases VS Education Level')
fig1.update_layout()

fig2 = px.bar(data3,
                 x='income_group',
                 y='total_cases',
                 color='income_group',
                 template='plotly_white',
                 labels={'country':'Country',
                         'total_cases': 'Total Tests'},
                 title='Total Cases By Income Group')
fig2.update_layout()

fig3 = px.bar(data2, 
              x='country', 
              y='total_cases', 
              color='income_group',
              template='plotly_white',
              labels={'income_group':'Income Group',
                      'total_cases': 'Total Cases'},
              title='Total Cases per Country')
fig3.update_layout()

# Defining App Layout 

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[      
      html.Div([ 
          html.H1('Studying The Pandemic Worldwide'),
              dcc.Graph(
                  id='covid-vs-edu',
                  figure = fig1
              ),    
          html.Div(
              dcc.Graph(
                  id='covid-vs-income',
                  figure = fig2
              )
      , style = {'width': '50%', 'display': 'inline-block'}),
          html.Div( 
              dcc.Graph(
                  id='covid-vs-income2',
                  figure = fig3
              )
      , style = {'width': '50%', 'display': 'inline-block'})
      ])
])



if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)