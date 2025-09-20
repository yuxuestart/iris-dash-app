import dash
from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = [iris.target_names[i] for i in iris.target]

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Iris Dataset Explorer", 
            style={'textAlign': 'center', 'marginBottom': 30, 'color': '#2c3e50'}),
    
    # Introduction section
    html.Div([
        html.P("Welcome to the Iris Dataset Explorer! This interactive dashboard helps you explore the famous Iris dataset.",
               style={'textAlign': 'center', 'fontSize': 16, 'marginBottom': 20}),
        html.P("The dataset contains measurements of 150 iris flowers from three different species: Setosa, Versicolor, and Virginica.",
               style={'textAlign': 'center', 'fontSize': 14, 'color': '#7f8c8d'})
    ], style={'marginBottom': 30}),
    
    # Controls section
    html.Div([
        html.Div([
            html.Label("Select X-axis feature:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=[{'label': col, 'value': col} for col in iris.feature_names],
                value=iris.feature_names[0],
                style={'marginBottom': 20}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.Label("Select Y-axis feature:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': col, 'value': col} for col in iris.feature_names],
                value=iris.feature_names[1],
                style={'marginBottom': 20}
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'marginBottom': 30}),
    
    # Scatter plot
    html.Div([
        html.H3("Scatter Plot", style={'textAlign': 'center', 'color': '#34495e'}),
        dcc.Graph(id='scatter-plot')
    ], style={'marginBottom': 40}),
    
    # Histogram section
    html.Div([
        html.H3("Feature Distribution", style={'textAlign': 'center', 'color': '#34495e'}),
        html.Div([
            html.Div([
                html.Label("Select feature for histogram:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='histogram-dropdown',
                    options=[{'label': col, 'value': col} for col in iris.feature_names],
                    value=iris.feature_names[0]
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
            
            html.Div([
                html.Label("Group by species:", style={'fontWeight': 'bold'}),
                dcc.Checklist(
                    id='species-checkbox',
                    options=[{'label': 'Yes', 'value': 'yes'}],
                    value=['yes']
                )
            ], style={'width': '30%', 'display': 'inline-block'})
        ], style={'marginBottom': 20}),
        
        dcc.Graph(id='histogram-plot')
    ], style={'marginBottom': 40}),
    
    # Data table
    html.Div([
        html.H3("Dataset Preview", style={'textAlign': 'center', 'color': '#34495e'}),
        html.Div([
            html.Label("Number of rows to display:", style={'fontWeight': 'bold', 'marginRight': 10}),
            dcc.Input(
                id='table-rows-input',
                type='number',
                value=10,
                min=1,
                max=150,
                style={'width': 80, 'marginRight': 20}
            )
        ], style={'marginBottom': 20}),
        
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.head(10).to_dict('records'),
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                }
            ]
        )
    ], style={'marginBottom': 40}),
    
    # Statistics section
    html.Div([
        html.H3("Dataset Statistics", style={'textAlign': 'center', 'color': '#34495e'}),
        html.Div(id='statistics-output')
    ])
])

# Callback for scatter plot
@callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(x_feature, y_feature):
    fig = px.scatter(df, x=x_feature, y=y_feature, color='species',
                     title=f'{x_feature} vs {y_feature}',
                     labels={x_feature: x_feature, y_feature: y_feature})
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    return fig

# Callback for histogram
@callback(
    Output('histogram-plot', 'figure'),
    [Input('histogram-dropdown', 'value'),
     Input('species-checkbox', 'value')]
)
def update_histogram(feature, group_by_species):
    if 'yes' in group_by_species:
        fig = px.histogram(df, x=feature, color='species', 
                          title=f'Distribution of {feature} by Species',
                          barmode='overlay', opacity=0.7)
    else:
        fig = px.histogram(df, x=feature, 
                          title=f'Distribution of {feature}',
                          color_discrete_sequence=['#3498db'])
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    return fig

# Callback for data table
@callback(
    Output('data-table', 'data'),
    [Input('table-rows-input', 'value')]
)
def update_table(rows):
    return df.head(rows).to_dict('records')

# Callback for statistics
@callback(
    Output('statistics-output', 'children'),
    [Input('histogram-dropdown', 'value')]
)
def update_statistics(feature):
    stats = df[feature].describe()
    species_stats = df.groupby('species')[feature].describe()
    
    return html.Div([
        html.Div([
            html.H4(f"Overall Statistics for {feature}"),
            html.P(f"Mean: {stats['mean']:.2f}"),
            html.P(f"Standard Deviation: {stats['std']:.2f}"),
            html.P(f"Minimum: {stats['min']:.2f}"),
            html.P(f"Maximum: {stats['max']:.2f}")
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.H4("Statistics by Species"),
            html.Div([
                html.Div([
                    html.H5(species),
                    html.P(f"Mean: {species_stats.loc[species, 'mean']:.2f}"),
                    html.P(f"Std: {species_stats.loc[species, 'std']:.2f}")
                ], style={'marginBottom': 15, 'padding': 10, 'backgroundColor': '#ecf0f1', 'borderRadius': 5})
                for species in species_stats.index
            ])
        ], style={'width': '48%', 'display': 'inline-block'})
    ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
