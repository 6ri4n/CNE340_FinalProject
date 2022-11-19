# air quality index project

import mysql.connector
import requests
import json
import time
import calendar
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_db():
    # TODO - connects to the 'cne340_finalproject' database
    con = mysql.connector.connect(
        user = 'root',
        password = '',
        host = '127.0.0.1',
        database = 'cne340_finalproject'
    )
    return con

def create_db_table(cursor):
    # TODO - creates a table in the 'cne340_finalproject' database
    pass

def query(cursor, query):
    # TODO - executes a query statement to a table in the 'cne340_finalproject' database
    cursor.execute(query)
    return cursor

def load_api_data():
    # TODO - sends a http request method (a get request) to the api
    api_key = '{INSERT API KEY HERE}'
    url = f'https://api.waqi.info/feed/Renton/?token={api_key}'
    response = requests.get(url)
    return json.loads(response.text)

def parse_date(dict):
    parsed_dict = {}
    for key, value in dict.items():
        parsed_key = key[-2:]
        parsed_dict[parsed_key] = value
    return parsed_dict

def graph(cursor, dict):
    # TODO -
    #   graphs the air quality for the week and current month
    #   and saves an image of the graph (overrides previous saves)
    title_year = dict.keys()[0][:4]
    num_month = dict.keys()[0][5:7]
    # TODO - convert into integer and remove leading zero
    if num_month[0] == '0':
        num_month = int(num_month[-1])
    else:
        num_month = int(num_month)
    title_month = calendar.month_name[num_month]

    week_dict = parse_date(dict)
    graph_dict = {
        'Week': week_dict
    }

    # TODO - query for current month aqi
    q = f''
    cur = query(cursor, q)
    key_list = cur.fetchall()
    q = f''
    cur = query(cursor, q)
    value_list = cur.fetchall()
    month_dict = dict(zip(key_list, value_list))
    graph_dict['Month'] = month_dict

    # TODO - create data structures for graph
    week = pd.Series(graph_dict["Week"].values(), index = graph_dict["Week"].keys())
    month = pd.Series(graph_dict["Month"].values(), index = graph_dict["Month"].keys())
    df1 = pd.DataFrame({'Week': week})
    df2 = pd.DataFrame({'Month': month})

    # TODO - create graph
    fig, graph = plt.subplots(nrows = 2, ncols = 1, figsize = [10, 8])
    df1.plot(ax = graph[0], marker = '.', markersize = 10, color = 'tab:orange')
    df2.plot(ax = graph[1], marker = '.', markersize = 10, color = 'tab:blue')
    graph[0].set(title = 'Average PM2.5 For The Week')
    graph[1].set(title = 'PM2.5 For The Month', xlabel = 'Day', ylabel = 'PM2.5')
    graph[1].yaxis.set_label_coords(-.08, 1.1)
    graph[1].xaxis.set_label_coords(.5, -0.18)
    fig.suptitle(f'Air Quality Index for {title_month} {title_year}', fontsize = 18, y = .95)
    fig.savefig('aqi_visual.png')

def add_to_table(cursor, data):
    # TODO - adds a row into a table in the 'cne340_finalproject' database
    pass

def parse_forecast_data(dict, data):
    # TODO - parses data for date and average pm25 and adds them to dict
    forecast_data = data['data']['forecast']['daily']['pm25']
    for row in forecast_data:
        dict[row['day']] = row['avg']
    return dict

def check_if_day_exist(cursor, date):
    # TODO -
    #   returns true or false if the current day exist in the 'cne340_finalproject' database
    pass

def work(cursor):
    # TODO -
    #   parse api data (current and forecast) -
    #       create a dictionary and add the parsed data from current
    #       pass the dictionary to parse_forecasts_data and reassign the value of the dictionary
    #   add current data to the 'cne340_finalproject' database (only if the aqi for that day hasn't been added)
    #   pass the dictionary into graph
    pass

def main():
    con = connect_to_db()
    cursor = con.cursor()
    create_db_table(cursor)
    print('>> script: active')

    #while True:
        #work(cursor)
        # 21600 seconds = 6 hours
        #time.sleep(21600)

if __name__ == '__main__':
    main()