'''
To run:

pip install dash
pip install dash_bootstrap_components

then run:
python dash_app.py

'''

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('data/salary_clean.csv')

print(df.info())

# stylesheet with the .dbc class from dash-bootstrap-templates library
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])


app.layout = html.Div([
    html.H1(children='Indiana University Spring 2024 Group 3 Time series project', style={'textAlign':'center'}),
    html.P(
    [
        "Plot average salaries in the United States by education level attained. Data provided by the ",
        html.A("US Census Bureau", href = "https://www.census.gov/data/tables/time-series/demo/educational-attainment/cps-historical-time-series.html"),
        ".\n Please choose a model to use for forecasting."
    ]),
    dcc.Dropdown(["Naive", "ARIMA", "SARIMAX", "LSTM"], "Naive"),
    dcc.Graph(id='salaries_graph',
          config={'displayModeBar': False},
          figure=px.line(df,
                         x='year',
                         y='adv_salary',
                         template='plotly_dark').update_layout(
                                   {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                    ),
    dcc.Checklist(
            id="checklist",
            options=[
                {"label": "Advanced degree", "value": 12},
                {"label": "Bachelors degree", "value": 10},
                {"label": "Some college", "value": 8},
                {"label": "High school", "value": 6},
            ],
            labelStyle={"display": "inline"},  
            value=[12],
        ),                                  
])

@callback(
    Output('salaries_graph', 'figure'),
    Input('checklist', 'value')
)
def update_graph(value):

    print (value)

    fig = px.line(df, x='year', y=df.columns[value])

    
    fig.update_layout(showlegend=True, 
                xaxis_title="Year",
                yaxis_title="Average salary",
                legend_title="Education level",
                plot_bgcolor="aliceblue")
    

    return fig

if __name__ == '__main__':
    app.run(debug=True)
