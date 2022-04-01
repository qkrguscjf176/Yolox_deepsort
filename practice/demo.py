# installations



# Import the Modules
import dash
from dash import html, dcc
from flask import Flask
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Initiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP])


# Read the Files
df = pd.read_csv('count.csv')
df1 = pd.read_csv('data.csv')



# Companents

# Header Companent
Header_component = html.H1("Traffic Analysis Dashboard", style = {'color':'DarkCyan', 'font-size':'72px', 'text-align':'center'})

# Component 1
countfig = go.FigureWidget()
countfig.add_scatter(name = "bus",x=df['Time'], y=df["bus"], fill = "tonexty", showlegend=True, line_shape='spline')
countfig.add_scatter(name = "car",x=df['Time'], y=df["car"], fill = "tonexty", showlegend=True, line_shape='spline')
countfig.update_layout(title = "Vehicle Time Line")

# Component 2
countfig_cum = go.FigureWidget()
countfig_cum.add_scatter(name = "bus",x=df['Time'], y=df["bus"].cumsum(), fill = "tonexty", showlegend=True, line_shape='spline')
countfig_cum.add_scatter(name = "car",x=df['Time'], y=df["car"].cumsum(), fill = "tonexty", showlegend=True, line_shape='spline')
countfig_cum.update_layout(title = "Cumulative Traffic")

# Component 3
indicator = go.FigureWidget(go.Indicator(
    mode = "gauge+number",
    value = df1["car"].mean(),
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Speed km/h"}))
indicator.update_layout(title ="Average Car Speed")

# Component 4
indicator2 = go.FigureWidget(go.Indicator(
    mode = "gauge+number",
    value = df1["bus"].mean(),
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Speed km/h"},
    gauge = {'bar': {'color': "Cyan"}}))
indicator2.update_layout(title ="Average Bus Speed")

# Component 5
piefig = go.FigureWidget(px.pie(labels=['car', 'bus'],
                names =['car', 'bus'] ,
                        values=[df['car'].sum(), df['bus'].sum()],
                        hole=.4,
                        title = "Traffic Distribution - Vehicle Type"))
piefig.update_layout(title ="Traffic Distribution")


# App Layout
app.layout = html.Div(style = {'padding-top':'10px'},
    children = [
        dbc.Row([dbc.Col([Header_component])]), #Row 1
        dbc.Row([
            dbc.Col([dcc.Graph(figure = countfig)], width = 6),
            dbc.Col([dcc.Graph(figure = countfig_cum)], width = 6),
        ]),#Row2
        dbc.Row([
            dbc.Col([dcc.Graph(figure = indicator)], width = 4),
            dbc.Col([dcc.Graph(figure = indicator2)], width = 4),
            dbc.Col([dcc.Graph(figure = piefig)], width = 4),
        ]), #Row3
    ]
)


# Run the app
if __name__ == '__main__':
    app.run_server(debug =True)
