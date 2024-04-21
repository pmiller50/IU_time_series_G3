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

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX, dbc_css])

# dash.Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.H1(children='Indiana University Spring 2024 Group 3 Time series project', style={'textAlign':'center'}), width="auto")),
        dbc.Row(dbc.Col(html.P(
                [
                    "Plot average salaries in the United States by education level attained. Data provided by the ",
                    html.A("US Census Bureau", href = "https://www.census.gov/data/tables/time-series/demo/educational-attainment/cps-historical-time-series.html"),
                    ".",
                    html.Br(), 
                    "Please choose a model to use for forecasting."
                ]
                ), width="auto")),
                

        dbc.Row(dbc.Col(dcc.Dropdown(["Naive", "ARIMA", "SARIMAX", "LSTM"], "Naive", id='model_selection'))),

        dbc.Row(
            [
                dbc.Col(   [ dcc.Graph(id='salaries_graph',
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
                                    labelStyle={"display": "inline","align-items": "center", "margin-right": "10px"},  
                                    value=[12],
                                    className="dbc"
                                )  ] , width=8),                                                      


                dbc.Col( [ html.Br(), 
                          html.P('Choose how many years to forecast'),
                          
                          dcc.Slider(0, 10, 1,
                            value=5,
                            id='forecast_year_slider',
                            className="dbc"
                                )
                                
                        ]),
            ]
        ),
    ],
    className="dbc"
    
    
    
 )

@callback(
    Output('salaries_graph', 'figure'),
    Input('checklist', 'value'),
    Input('forecast_year_slider', 'value'),
    Input('model_selection', 'value')
)
def update_graph(edu_checklist,forecast_year_slider, model_selection):

    print (f'edu_checklist {edu_checklist}')
    print (f'forecast_year_slider {forecast_year_slider}')
    print (f'model_selection {model_selection}')

    fig = px.line(df, x='year', y=df.columns[edu_checklist])



    
    fig.update_layout(showlegend=True, 
                xaxis_title="Year",
                yaxis_title="Average salary",
                legend_title="Education level",
                plot_bgcolor="aliceblue")
    

    return fig

if __name__ == '__main__':
    app.run(debug=True)
