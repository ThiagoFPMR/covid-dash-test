import dash
from dash.dependencies import Output, Input
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
                         'total_cases': 'Total Cases'},
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
      html.H1('Studying The Pandemic Worldwide', style={'textAlign':'center'}),
      html.Div([
          html.Div([ 
              html.Label('Population'),
              dcc.Slider(
                  id='population-slider',
                  min=data.population.min(),
                  max=data.population.max(),
                  marks={
                    72037 : '72K',
                    80000000 : '80M',
                    150000000 : '150M',
                    300000000 : '300M',
                    700000000 : '700M',
                    1000000000 : '1B',
                    1439323776 : '1.4B' 
                  },
                  value=data.population.min(),
                  step=100000000,
                  updatemode='drag'
              )
          ]),
          html.Div([
              html.Label('Interest Variable'),
              dcc.Dropdown(
                  id='interest-variable',
                  options=[{'label':'Total Cases', 'value':'total_cases'},
                           {'label': 'Total Tests', 'value':'total_tests'},
                           {'label': 'Total Deaths', 'value':'total_deaths'},
                           {'label': 'Total Recovered', 'value':'total_recovered'}],
                  value='total_cases' 
              )
          ])
      ], style = {'width':'90%','margin':'auto'}),      
      html.Div([ 
              dcc.Graph(
                  id='covid-vs-edu',
              ),    
          html.Div(
              dcc.Graph(
                  id='covid-vs-income',
              )
      , style = {'width': '50%', 'display': 'inline-block'}),
          html.Div( 
              dcc.Graph(
                  id='covid-vs-income2',
              )
      , style = {'width': '50%', 'display': 'inline-block'})
      ], style = {'width':'90%','margin':'auto'})
])

def scatter_y_label (var):
  if var == 'total_cases':
    return 'Percentage Infected'
  elif var == 'total_tests':
    return 'Percentage Tested'
  elif var == 'total_deaths':
    return 'Percentage Dead'
  elif var == 'total_recovered':
    return 'Percentage Recovered'

# Variable VS Education Level Scatter Plot

@app.callback(Output('covid-vs-edu', 'figure'),
              [Input('population-slider', 'value'),
               Input('interest-variable', 'value')])             
def update_scatter(selected_pop, interest_var):
  sorted = data[data.population <= selected_pop]
  fig = px.scatter(sorted,
                  x='expected_years_of_school',
                  y=sorted[interest_var]/sorted.population,
                  size='population',
                  color='income_group',
                  hover_name='country',
                  template='plotly_white',
                  labels={'expected_years_of_school':'Expected Years of School',
                          'y': scatter_y_label(interest_var),
                          'income_group':'Income Group'},
                  title='Total Cases VS Education Level')
  fig.update_layout(transition_duration=500)
  return fig

# Variable Per Income Group Bar Chart

@app.callback(Output('covid-vs-income', 'figure'),
              [Input('population-slider', 'value'),
               Input('interest-variable', 'value')])             
def update_income_bar(selected_pop, interest_var):
  sorted = data[data.population <= selected_pop].groupby(by='income_group').sum().reset_index()
  fig = px.bar(sorted,
                  x='income_group',
                  y=interest_var,
                  color='income_group',
                  template='plotly_white',
                  labels={'income_group':'Income Group',
                          'total_cases':'Total Cases',
                          'total_tests':'Total Tests',
                          'total_deaths':'Total Deaths',
                          'total_recovered':'Total Recovered'},
                  title='Total Cases By Income Group')
  fig.update_layout()
  return fig

# Variable Per Country Bar Chart

@app.callback(Output('covid-vs-income2', 'figure'),
              [Input('population-slider', 'value'),
               Input('interest-variable', 'value')])             
def update_country_bar(selected_pop, interest_var):
  sorted = data[data.population <= selected_pop]
  fig = px.bar(sorted, 
                x='country', 
                y=interest_var, 
                color='income_group',
                template='plotly_white',
                labels={'country':'Country',
                        'income_group':'Income Group',
                        'total_cases':'Total Cases',
                        'total_tests':'Total Tests',
                        'total_deaths':'Total Deaths',
                        'total_recovered':'Total Recovered'},
                title='Total Cases per Country')
  fig.update_layout()
  return fig

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)