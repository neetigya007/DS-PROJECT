#!/usr/bin/env python
# coding: utf-8

# TASK 2.1: Create a Dash application and give it a meaningful title
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
# TASK 2.4: Read data to be visualized
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# TASK 2.2: Add drop-down menus to your dashboard with appropriate titles and options
# List of years for the dropdown
year_list = [i for i in range(1980, 2024, 1)]

# TASK 2.3: Create the layout of the app including dropdowns and output container
dropdown_style = {'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}

app.layout = html.Div([
    # Title of the Dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#000000', 'font-size': 24}),

    # Dropdown to select statistics type
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select a report type',
            style=dropdown_style
        )
    ]),

    # Dropdown to select year
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2020,
            placeholder='Select-year',
            style=dropdown_style
        )
    ]),

    # TASK 2.3: Add a division for output display with appropriate id and classname property
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# TASK 2.4: Creating Callbacks; Enable/Disable year dropdown based on selection
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# TASK 2.4: Creating Callbacks; Output update logic based on inputs
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # TASK 2.5: Create and display graphs for Recession Report Statistics

        # Plot 1: Average automobile sales over recession years
        recession_data = data[data['Recession'] == 1]
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                            title="Average Automobile Sales Over Recession Years"))

        # Plot 2: Average vehicles sold by vehicle type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                                           title="Average Vehicle Type Sales During Recession"))

        # Plot 3: Advertising expenditure share
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                                          title="Advertising Expenditure Share During Recession"))

        # Plot 4: Unemployment vs Vehicle Type Sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                                           labels={'unemployment_rate': 'Unemployment Rate'},
                                           title='Effect of Unemployment on Vehicle Type Sales'))

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif input_year and selected_statistics == 'Yearly Statistics':
        # TASK 2.6: Create and display graphs for Yearly Report Statistics

        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly average automobile sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                            title="Average Automobile Sales Per Year"))

        # Plot 2: Monthly total automobile sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                            title='Total Monthly Automobile Sales'))

        # Plot 3: Average vehicle sales by type in selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                                           title=f'Average Vehicles Sold in {input_year}'))

        # Plot 4: Advertisement expenditure by vehicle type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                                          title='Total Advertisement Expenditure by Vehicle'))

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    else:
        return None

# TASK 2.6: Run the application
if __name__ == '__main__':
    app.run(debug=True)

