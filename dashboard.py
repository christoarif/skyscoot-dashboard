import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load the CSV data
df = pd.read_csv('mock_data.csv')
df['departureTime'] = pd.to_datetime(df['departureTime'])  # Convert departureTime column to datetime

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Flight Dashboard"),
    html.Div([
        html.Label("Flight Number"),
        dcc.Dropdown(
            id='flight-dropdown',
            options=[{'label': num, 'value': num} for num in df['flightNumber'].unique()],
            value=df['flightNumber'].unique()[0]
        )
    ]),
    html.Div([
        html.Label("Departure Time"),
        dcc.Dropdown(
            id='departure-dropdown',
            value=df[df['flightNumber'] == df['flightNumber'].unique()[0]]['departureTime'].unique()[0],
            placeholder="Select Departure Time"
        )
    ]),
    dcc.Graph(id='flight-status'),
    dcc.Graph(id='item-quantity'),
])

# Define the flight status callback
@app.callback(
    Output('flight-status', 'figure'),
    Input('flight-dropdown', 'value'),
    Input('departure-dropdown', 'value')
)
def update_flight_status(flight_number, departure_time):
    filtered_data = df[(df['flightNumber'] == flight_number) & (df['departureTime'] == departure_time)]
    status_counts = filtered_data['status'].value_counts()

    fig = {
        'data': [go.Bar(x=status_counts.index, y=status_counts.values)],
        'layout': {
            'title': f"Flight Status for {flight_number} ({pd.to_datetime(departure_time).strftime('%Y-%m-%d %H:%M:%S')})",
            'xaxis': {'title': 'Status'},
            'yaxis': {'title': 'Count'}
        }
    }
    return fig

# Define the item quantity callback
@app.callback(
    Output('item-quantity', 'figure'),
    Input('flight-dropdown', 'value'),
    Input('departure-dropdown', 'value')
)
def update_item_quantity(flight_number, departure_time):
    filtered_data = df[(df['flightNumber'] == flight_number) & (df['departureTime'] == departure_time)]
    item_counts = filtered_data.groupby('ItemName')['quantity'].sum()

    fig = {
        'data': [go.Bar(x=item_counts.index, y=item_counts.values)],
        'layout': {
            'title': f"Item Quantity for {flight_number} ({pd.to_datetime(departure_time).strftime('%Y-%m-%d %H:%M:%S')})",
            'xaxis': {'title': 'Item Name'},
            'yaxis': {'title': 'Quantity'}
        }
    }
    return fig

# Update departure dropdown options based on flight selection
@app.callback(
    Output('departure-dropdown', 'options'),
    Input('flight-dropdown', 'value')
)
def update_departure_dropdown_options(flight_number):
    departure_times = df[df['flightNumber'] == flight_number]['departureTime'].unique()
    options = [{'label': dt.strftime('%Y-%m-%d %H:%M:%S'), 'value': dt} for dt in departure_times]
    return options

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
