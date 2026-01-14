import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

# Load the processed data
df = pd.read_csv('pink_morsel_sales.csv')

# Convert date to datetime for proper sorting
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Add a column to indicate before/after price increase
df['price_period'] = df['date'].apply(
    lambda x: 'After Price Increase' if x >= pd.Timestamp('2021-01-15') else 'Before Price Increase'
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    # Header
    html.H1("Pink Morsel Sales Analysis", style={'textAlign': 'center'}),
    
    # Description
    html.Div([
        html.P("This dashboard visualizes the sales of Pink Morsels before and after the price increase on January 15, 2021."),
        html.P("The vertical red line indicates the date of the price increase.")
    ], style={'margin': '20px'}),
    
    # Line chart
    dcc.Graph(id='sales-chart'),
    
    # Region filter
    html.Div([
        html.Label('Select Region:'),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': 'All Regions', 'value': 'all'}] +
                   [{'label': region, 'value': region} for region in df['region'].unique()],
            value='all',
            clearable=False,
            style={'width': '50%', 'margin': '10px 0'}
        )
    ], style={'width': '50%', 'margin': '20px'}),
    
    # Summary statistics
    html.Div(id='summary-stats', style={'margin': '20px', 'padding': '10px', 'border': '1px solid #ddd'})
])

# Callback to update the chart based on region selection
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('summary-stats', 'children')],
    [Input('region-filter', 'value')]
)
def update_chart(selected_region):
    # Filter data by selected region
    if selected_region == 'all':
        filtered_df = df
        title_suffix = "All Regions"
    else:
        filtered_df = df[df['region'] == selected_region]
        title_suffix = f"{selected_region.capitalize()} Region"
    
    # Create the line chart
    fig = px.line(
        filtered_df, 
        x='date', 
        y='sales', 
        color='region',
        title=f'Sales Over Time - {title_suffix}',
        labels={'sales': 'Sales ($)', 'date': 'Date', 'region': 'Region'}
    )
    
    # Add a vertical line for the price increase date
    fig.add_vline(
        x=pd.Timestamp('2021-01-15'), 
        line_dash="dash", 
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top"
    )
    
    # Calculate summary statistics
    before = filtered_df[filtered_df['price_period'] == 'Before Price Increase']['sales'].sum()
    after = filtered_df[filtered_df['price_period'] == 'After Price Increase']['sales'].sum()
    total_sales = filtered_df['sales'].sum()
    
    # Create summary statistics text
    stats = [
        html.H3("Summary Statistics"),
        html.P(f"Total Sales: ${total_sales:,.2f}"),
        html.P(f"Sales Before Price Increase: ${before:,.2f}"),
        html.P(f"Sales After Price Increase: ${after:,.2f}"),
        html.P(f"Percentage Change: {((after - before) / before * 100):.1f}%")
    ]
    
    return fig, stats

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
