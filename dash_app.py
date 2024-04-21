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
import os
import pickle

df = pd.read_csv('data/salary_clean.csv')

print(df.info())

# stylesheet with the .dbc class from dash-bootstrap-templates library
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

models_dir = 'models'
saved_models = os.listdir(models_dir)

app.layout = html.Div([
    html.H1(children='Indiana University Spring 2024 Group 3 Time series project', style={'textAlign':'center'}),
    html.P(
    [
        "Plot average salaries in the United States by education level attained. Data provided by the ",
        html.A("US Census Bureau", href = "https://www.census.gov/data/tables/time-series/demo/educational-attainment/cps-historical-time-series.html"),
        ".\n Please choose a model to use for forecasting."
    ]),
    #dcc.Dropdown(["Naive", "ARIMA", "SARIMAX", "LSTM"], "None"),

    dcc.Graph(id='model_graph',
              config={'displayModeBar': False},
              figure={}
              ),

    dcc.Dropdown(
        id='model-dropdown',
        options=[{'label': model_name, 'value': model_name} for model_name in saved_models],
        value=None
    ),
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
    Output('model_graph', 'figure'),
    Input('checklist', 'value'),
    Input('model-dropdown', 'value')
)
# def update_graph(value):

#     print (value)

#     fig = px.line(df, x='year', y=df.columns[value])

    
#     fig.update_layout(showlegend=True, 
#                 xaxis_title="Year",
#                 yaxis_title="Average salary",
#                 legend_title="Education level",
#                 plot_bgcolor="aliceblue")
    

#     return fig

def update_graph(selected_model):
    if selected_model is not None:
        # Load the selected model
        model_path = os.path.join(models_dir, selected_model)
        print(model_path)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Generate predictions using the model
        # Here you should replace the sample code with your actual model predictions
        predictions = model.predict(df['year'])  # Replace data['year'] with your input data

        # Create a plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['year'], y=df['total_earners_salary'], mode='lines+markers', name='Actual'))
        fig.add_trace(go.Scatter(x=df['year'], y=predictions, mode='lines', name='Predicted'))

        # Update layout
        fig.update_layout(title='Model Predictions vs Actual',
                          xaxis_title='Year',
                          yaxis_title='Total Earners Salary')

        return fig
    else:
        # Return an empty figure if no model is selected
        return {}


if __name__ == '__main__':
    app.run(debug=True)
