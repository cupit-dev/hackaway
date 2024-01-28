from taipy.gui import Gui, notify
import pandas as pd
import datetime
from datetime import date
import numpy as np
import pickle

with open('toms_test.pkl', 'rb') as file:
    emotion_metrics_over_time = pickle.load(file)

def format_data(data):
    
    vals = list(data.values())
    column_names = list(vals[0].keys())

    formatted = pd.DataFrame(columns = column_names)
    dtypes = {column_name: 'float64' for column_name in column_names}
    formatted = formatted.astype(dtypes)


    # Function to process and split string values
    def process_value(value):
        if isinstance(value, str):  # Check if the value is a string
            x = value.split(' ')[-1]
            return round(float(x), 1)  # Return the last part after splitting
        return round(float(value), 1)  # Return the original value if it's not a string

    # Iterate through the dictionary of dictionaries
    for _, value_dict in data.items():
        # Process each value in the sub-dictionary
        processed_dict = {k: process_value(v) for k, v in value_dict.items()}
        
        # Convert the processed dictionary to a DataFrame row
        row_df = pd.DataFrame([processed_dict])
        
        # Append the row DataFrame to the main DataFrame
        formatted = pd.concat([formatted, row_df], ignore_index=True)


    formatted['Date'] = list(emotion_metrics_over_time.keys())

    # Reverse the order of rows and columns
    formatted = formatted.iloc[::-1].reset_index(drop=True)
    formatted = formatted[formatted.columns[::-1]]

    return formatted

dataset = format_data(emotion_metrics_over_time)

columns = dataset.columns.tolist()

page = """
<br/>
<div style='text-align: center;'><strong style='font-size: 26px;'>Your Recent Moods</strong></div>
<br/>
<br/>
"""

section2 = """
<|{dataset}|chart|mode=lines|x={columns[0]}|y[1]={columns[1]}|y[2]={columns[2]}|y[3]={columns[3]}|y[4]={columns[4]}|y[5]={columns[5]}|color[1]=#F2A7FF|color[2]=#29B9FD|color[3]=#29FD66|color[4]=#F7D784|color[5]=#FB9017|>

"""

section3 = """

<|layout|columns = 1 5|
<|
#### Select Date
**Starting Date**\n\n<|{start_date}|date|not with_time|on_change=start_date_onchange|>
<br/><br/>
**Ending Date**\n\n<|{end_date}|date|not with_time|on_change=end_date_onchange|>
<br/>
<br/>
<|button|label=GO|on_action=button_action|>
|>
<|

<br/>
<center>
<|{dataset}|table|page_size=10|height=500px|width=65%|>
</center>
<center> <h2>Data</h2><|{download_data}|file_download|on_action=download|>
</center>

<br/>
<br/>
|>
|>
"""

def start_date_onchange(state, var_name, value):
    state.start_date = value

def end_date_onchange(state, var_name, value):
    state.end_date = value

def filter_by_date_range(dataset, start_date, end_date):
    dataset['Date'] = pd.to_datetime(dataset['Date']).dt.date
    mask = (dataset['Date']>start_date) & (dataset['Date'] <= end_date)
    return dataset.loc[mask]

def button_action(state):
    state.dataset = filter_by_date_range(dataset, state.start_date, state.end_date)
    notify(state, "info", "Updated date range from {} to {}.".format(start_date.strftime("%m%d%Y"), end_date.strftime("%m%d%Y")))

def download(state):
    state.dataset.to_csv('download.csv')

start_date = datetime.date(2024, 1, 1) 
end_date = date.today() 
download_data = "download.csv"

Gui(page=page + section2 + section3).run(dark_mode = True)
