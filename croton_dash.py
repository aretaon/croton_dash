import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('croton.csv', delimiter='\t')

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Time'],
                         y=df['Light Intensity [Lux]'],
                         mode='markers',
                         ))
fig.update_layout(
                    title="Light",
                    xaxis_title="Time",
                    yaxis_title="Light intensity [Lux]",
                    font=dict(
                    family="Vollkorn",
                    size=18,
                    color="#7f7f7f"
                )
                        )
app.layout = html.Div(children=[
    html.H1(children='Croton Stats'),

    html.Div(children='''
                      See how your croton is doing!
                      '''),

    dcc.Graph(
        id='example-graph',
        figure = fig
    )
])
if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.178.34')
