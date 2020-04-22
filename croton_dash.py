import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Croton Stats'),

    dcc.Graph(id='metrics_graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000, #msec
        n_intervals=0
        )
    ])

@app.callback(Output('metrics_graph', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    
    df = pd.read_csv('croton.csv', delimiter='\t').sort_values(by='Time')

    fig = make_subplots(rows=2,
                        cols=1,
                        subplot_titles=("Light [Lux]", "Pressure [Pa] & Temperature [°C]"),
                        shared_xaxes=True,
                        specs=[[{"secondary_y": False}],
                               [{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df['Time'],
                             y=df['Light Intensity [Lux]'],
                             name='Light [Lux]'),
                             row=1,
                             col=1,
                             )

    fig.add_trace(go.Scatter(x=df['Time'],
                             y=df['Pressure [Pa]'],
                             name='Pressure [Pa]'),
                             row=2,
                             col=1,
                             )

    fig.add_trace(go.Scatter(x=df['Time'],
                             y=df['Temperature [C]'],
                             name='Temperature [°C]'),
                             secondary_y=True,
                             row=2,
                             col=1,
                             )

    fig.update_layout(  height=800,
                        font=dict(
                        family="Vollkorn",
                        size=18,
                        color="#7f7f7f"),
                        #xaxis=dict(
                        #    rangeselector=dict(
                        #        buttons=list([
                        #        dict(count=1,
                        #            label="1d",
                        #            step="day",
                        #            stepmode="backward"),
                        #        dict(count=6,
                        #            label="6h",
                        #            step="hour",
                        #            stepmode="backward"),
                        #        dict(count=60,
                        #            label="-1h",
                        #            step="minute",
                        #            stepmode="todate"),
                        #        dict(step="all")
                        #    ])
                        #    ),
                        #rangeslider=dict(
                        #    visible=True
                        #),
                        #type="date"
                        #)
                    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.178.34')
