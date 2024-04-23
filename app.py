'''
Indiana University Time Series Analysis Group Project

# Group G3

*   Paul Miller
*   Dhyey Joshi
*   Jui Ambikar

To run:

pip install dash
pip install dash_bootstrap_components

then run:
python app.py

'''

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pickle
from os.path import join

# from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('data/salary_clean.csv')

# sort the dataframe by year so the most recent is last
df.sort_values(by='year', inplace=True)

# Define names of target columns
target_columns = ['high_school_salary', 'some_college_salary', 'bachelors_salary', 'adv_salary']

# Load pickled models to a dictionary
# This code isn't used at the moment. We load the models dynamically every time which is not efficient.
# arima_models = {}

# for edu_column in target_columns:

#     with open(join("models", f"{edu_column}_ARIMA.pkl"), "rb") as f:
#         arima_models[edu_column] = pickle.load(f)

from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()

# print(f'THIS_FOLDER: {THIS_FOLDER}')
# my_file = THIS_FOLDER / "myfile.txt"

    
def naive_forecast(series, steps):
    '''
    Naive model
    '''
    return np.array([series.iloc[-1]] * steps)
    

# stylesheet with the .dbc class from dash-bootstrap-templates library
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX, dbc_css])

server = app.server

app.title = "Salaries by education level"


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
                

        dbc.Row(dbc.Col(dcc.Dropdown(["Naive", "ARIMA", "SARIMAX"], "Naive", id='model_selection'))),

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
                                        )
                           ]
                       )       ,                                     


                dbc.Col( [ html.Br(), 
                          html.P('Choose how many years to forecast'),
                          
                          dcc.Slider(0, 10, 1,
                            value=5,
                            id='forecast_year_slider',
                            className="dbc"
                                ),

                            html.Br(), 

                            html.P( "Select highest education level attained."),                                                        

                            dcc.Checklist(
                                    id="checklist",
                                    options=[
                                        {"label": "Advanced degree", "value": 12},
                                        {"label": "Bachelors degree", "value": 10},
                                        {"label": "Some college", "value": 8},
                                        {"label": "High school", "value": 6},
                                    ],
                                    labelStyle={"align-items": "center", "margin-right": "10px"},  
                                    value=[12],
                                    className="dbc"
                                )                                      
                                
                        ], width="auto"),
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

    # print (f'edu_checklist {edu_checklist}')
    # print (f'forecast_year_slider {forecast_year_slider}')
    # print (f'model_selection {model_selection}')

    fig = px.line(df, x='year', y=df.columns[edu_checklist])

    # Loop through an array of checked values and load the respective models.
    # After loading, generate forecasts and plot

    # If Naive selected then use function defined above
    if model_selection == 'Naive':


        for edu_column_name in df.columns[edu_checklist].values:
            naive_forecast_values = naive_forecast(df[edu_column_name], forecast_year_slider)

            # print(f'Naive forecast values: {naive_forecast_values}')

            # The dataframe has the latest year as the last row, so find the latest year as the starting point
            # to add new values
            last_year_in_data = df.iloc[-1]['year']

            # create range for forecasted steps
            added_years = range(last_year_in_data, last_year_in_data + forecast_year_slider)

            fig.add_trace(
                go.Scatter(
                    x=list(added_years),
                    y=naive_forecast_values,
                    mode='lines',
                    name=f'{edu_column_name}_naive_forecast'
                )
            )

    else:

        for edu_column_name in df.columns[edu_checklist].values:

            # Call specified model with years selected
            # e.g. bachelors_salary_ARIMA.pkl
            loaded_model = pickle.load(open(join(THIS_FOLDER, 'models', f'{edu_column_name}_{model_selection}.pkl.'), 'rb'))

            forecasts = round(loaded_model.forecast( forecast_year_slider))

            # print(f'model_selection:{model_selection}, forecasts:{forecasts}')

            # Convert the forecasts index (which is Index of Timestamps) into a list of years as int
            forecast_years = [timestamp.year for timestamp in forecasts.index]


            fig.add_trace(
                go.Scatter(
                    x=forecast_years,
                    y=forecasts.values,
                    mode='lines',
                    name=f'{edu_column_name}_{model_selection}_forecast'
                )
            )


    fig.update_layout(showlegend=True, 
                xaxis_title="Year",
                yaxis_title="Average salary",
                legend_title="Education level",
                plot_bgcolor="aliceblue")
    

    return fig

if __name__ == '__main__':
    app.run(debug=True)
