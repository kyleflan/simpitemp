from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
from datetime import datetime
from datetime import timezone
import time
import pytz
from TimeLimitedRedisDict import TimeLimitedRedisDict
import json
import pandas as pd

# set up two redis TimeLimitedRedisDicts to store read readings from
# this data will be populated by stats_collector.py
tlrd_temp = TimeLimitedRedisDict(redis_key='temperature')
tlrd_hum = TimeLimitedRedisDict(redis_key='humidity')

system_tz = time.tzname[time.daylight]
display_tz = 'US/Central'

# default route
@app.route('/')
def return_temp_hum():
    # Uncomment to print readings
    #print("Temp: {0:0.1f} F Humidity: {1:0.1f} %".format(temperature, humidity))

    timestamp = datetime.now(pytz.timezone('US/Central')).strftime("%Y-%m-%d %H:%M:%S")

    # get latest values
    tlrd_temp.read_dict()
    tlrd_hum.read_dict()

    # find and remove outlier stats
    df_hum = pd.DataFrame(tlrd_hum.d.values(),
                          index=pd.to_datetime(pd.Series(tlrd_hum.d.keys())),
                          columns=['hum'])
    df_hum.sort_index(inplace=True)
    df_temp = pd.DataFrame(tlrd_temp.d.values(),
                           index=pd.to_datetime(pd.Series(tlrd_temp.d.keys())),
                           columns=['temp'])
    df_temp.sort_index(inplace=True)

    removed_outliers_hum = df_hum['hum'].between(df_hum['hum'].mean() - 5.0, 
                                                 df_hum['hum'].mean() + 5.0)
    removed_outliers_temp = df_temp['temp'].between(df_temp['temp'].mean() - 5.0,
                                                    df_temp['temp'].mean() + 5.0)

    # remove dropped labels from both df's
    df_hum.drop(df_hum[~removed_outliers_hum].index, inplace=True)
    df_temp.drop(df_temp[~removed_outliers_temp].index, inplace=True)

    temp_labels = list(df_temp.index.tz_localize(system_tz).tz_convert(display_tz))
    hum_labels = list(df_hum.index.tz_localize(system_tz).tz_convert(display_tz))

    temp_values = list(df_temp['temp'])
    hum_values = list(df_hum['hum'])

    temp_avg = df_temp['temp'].mean()
    hum_avg = df_hum['hum'].mean()

    # format temp labels (for better rendering on the chart)
    formatted_temp_labels = [label.strftime('%H:%M:%S') for label in temp_labels]

    # get "instantaneous" metrics, which are the values at the latest index
    temp_inst = df_temp.loc[df_temp.index.max()].squeeze()
    hum_inst = df_hum.loc[df_hum.index.max()].squeeze()

    return render_template("index.html", 
            avg_temperature='%0.2f' % temp_avg, 
            inst_temperature='%0.2f' % temp_inst,
            avg_humidity='%0.2f' % hum_avg,
            inst_humidity='%0.2f' % hum_inst,
            timestamp=timestamp,
            temp_labels=formatted_temp_labels, 
            temp_values=temp_values,
            hum_values=hum_values)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
