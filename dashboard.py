import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.colors

# Load the CSV data
df = pd.read_csv('mock_data.csv')
df['departureTime'] = pd.to_datetime(df['departureTime'])  # Convert departureTime column to datetime

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    html.H1("SkyScoot Dashboard"),
    dbc.Row([
        dbc.Col([
            html.Label("Flight Number"),
            dcc.Dropdown(
                id='flight-dropdown',
                options=[{'label': num, 'value': num} for num in df['flightNumber'].unique()],
                value=df['flightNumber'].unique()[0]
            )
        ]),
        
        dbc.Col([
            html.Label("Date Range"),
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=df['departureTime'].min(),
                end_date=df['departureTime'].max(),
                display_format='YYYY-MM-DD',
            )
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='order-status')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='item-quantity-pie')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='item-quantity-bar')
        ], width=12)
    ])
])



# Define the order status callback
@app.callback(
    Output('order-status', 'figure'),
    Input('flight-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_order_status(flight_number, start_date, end_date):
    filtered_data = df[(df['flightNumber'] == flight_number) & (df['departureTime'].between(start_date, end_date))]
    status_counts = filtered_data['status'].value_counts()

    # Assign colors based on order status
    colors = ['red' if status == 'Out of Stock' else 'green' for status in status_counts.index]

    fig = {
        'data': [go.Bar(x=status_counts.index, y=status_counts.values, marker=dict(color=colors))],
        'layout': {
            'title': f"Order Status for Flight {flight_number} for the Time Range",
            'xaxis': {'title': 'Status'},
            'yaxis': {'title': 'Count'}
        }
    }
    return fig

# Define the item quantity callback
@app.callback(
    Output('item-quantity-bar', 'figure'),
    Output('item-quantity-pie', 'figure'),
    Input('flight-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)

def update_item_quantity(flight_number, start_date , end_date):
    filtered_data = df[(df['flightNumber'] == flight_number) & (df['departureTime'].between(start_date, end_date))]
    item_counts = filtered_data.groupby('ItemName')['quantity'].sum()
    item_statuses = filtered_data.groupby(['ItemName', 'status'])['quantity'].sum().unstack(fill_value=0)

    # Get the top 5 frequent items
    top_items = item_counts.nlargest(5)

    # Calculate the total quantity of top items
    total_quantity_top_items = top_items.sum()

    # Calculate the quantity of "Others"
    others_quantity = item_counts.sum() - total_quantity_top_items

    # Create the stacked bar chart
    bar_chart_data = []
    for item in item_counts.index:
        bar_chart_data.append(go.Bar(name='Success', x=[item], y=[item_statuses.loc[item, 'Success']], marker=dict(color='green')))
        bar_chart_data.append(go.Bar(name='Out of Stock', x=[item], y=[item_statuses.loc[item, 'Out of Stock']], marker=dict(color='red')))

    bar_chart_fig = {
        'data': bar_chart_data,
        'layout': {
            'title': f"Items Sold for Flight {flight_number} for the Time Range",
            'xaxis': {'title': 'Item Name'},
            'yaxis': {'title': 'Quantity'},
            'barmode': 'stack',
            'showlegend': False 
        }
    }

    # Create the pie chart including "Others" in grey color
    pie_labels = list(top_items.index) + ['Others']
    pie_values = list(top_items.values) + [others_quantity]
    num_top_items = len(top_items)
    pie_colors = plotly.colors.qualitative.Plotly[:num_top_items] + ['grey']
    pie_chart_fig = {
        'data': [go.Pie(labels=pie_labels, values=pie_values, marker=dict(colors=pie_colors))],
        'layout': {
            'title': f"Items Sold (Pie Chart) for Flight {flight_number} for the Time Range"
        }
    }

    return bar_chart_fig, pie_chart_fig


# Update departure dropdown options based on flight selection
# @app.callback(
#     Output('departure-dropdown', 'options'),
#     Input('flight-dropdown', 'value')
# )
# def update_departure_dropdown_options(flight_number):
#     departure_times = df[df['flightNumber'] == flight_number]['departureTime'].unique()
#     options = [{'label': dt.strftime('%Y-%m-%d %H:%M'), 'value': dt} for dt in departure_times]
#     return options

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
