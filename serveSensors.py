#import chart_studio.plotly as py
#import plotly.graph_objects as go
#import dash
#import dash_core_components as dcc
#import dash_html_components as html
import time
import sensors
import led
import numpy as np
import os

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# username = 'aretaon'
# api_key = '4q0zJEtf8HRh9TEKl7DJ'
# stream_token = 'li7n0zerim'
# py.sign_in(username, api_key)

light = sensors.BH1750()
temp_press = sensors.BME280()
warn = led.State()

measuring_interval_sec = 60
accumulate_data_points = 10

max_light_lux = 1000
min_light_lux = 200

outfile = 'croton.csv'

time_array = []
light_array = []
temp_array = []
press_array = []

c = 0

# empty run to initialise sensors
_ = light.lux()
_, _ = temp_press.temp_and_pressure()

while True:
    if c == accumulate_data_points:
        c = 0
        
        if not os.path.isfile(outfile):
            with open(outfile, 'w') as f:
                f.write('Time\tLight Intensity [Lux]\tTemperature [C]\tPressure [Pa]\n')
        with open(outfile, 'a') as f:
            a = np.asarray([time_array, light_array, temp_array, press_array])
            np.savetxt(f, np.transpose(a), delimiter='\t', fmt='%s')
#        fig = go.Figure(data=go.Scatter(x=time_array, y=light_array))
#        new_data = go.Scatter(x=time_array, y=light_array)
#        print('Sending Data')
#
#        plot_url = py.plot ([new_data], filename='light_test', auto_open=False)

    measuring_time = np.datetime64(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    lux = light.lux()
    temp, pressure = temp_press.temp_and_pressure()

    if (lux > min_light_lux) and (lux < max_light_lux):
        warn.good()
    else:
        warn.bad()
   
    time_array.append(measuring_time)
    light_array.append(lux)
    temp_array.append(temp)
    press_array.append(pressure)

    c += 1
    time.sleep(measuring_interval_sec)



