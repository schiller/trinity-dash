import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('app', server=server)

df = pd.read_csv('timestamp_hist.csv')

unique_days = df.day.unique()

app.layout = html.Div([
    dcc.Graph(id='histogram'),

    html.Div(
        dcc.RangeSlider(
            id='day-slider',
            marks={str(day): str(day) for day in unique_days},
            min=unique_days[0],
            max=unique_days[-1],
            value=[unique_days[1], unique_days[-2]]
        ),
        style={'padding': '0px 60px'}
    )
])


@app.callback(
    Output('histogram', 'figure'),
    [Input('day-slider', 'value')])
def update_figure(selected_days):
    filtered_df = df[
        (df.day >= selected_days[0]) &
        (df.day <= selected_days[1])
    ]

    bars = [go.Bar(
        x=filtered_df.day.astype('str') + ", " + filtered_df.hour.astype('str') + "h",
        y=filtered_df['count'],
        name='bar chart example'
    )]

    return {
        'data': bars,
        'layout': go.Layout(
            title='Article Views - Trinity Mirror',
            xaxis={'title': 'Day, Hour'},
            yaxis={'title': 'Hourly Total Views'}
        )
    }


if __name__ == '__main__':
    app.run_server()
