import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import calendar
import fix_yahoo_finance

CURRENT_DIRECTORY = str((Path(__file__) / '..').resolve())

def get_datetime(datetime_string):
    return datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')

def move_before_9am_to_previous_day(df):
    for index, row in df.iterrows():
        datetime_object = get_datetime(df.iloc[index, 0])
        if datetime_object.hour <= 8:
            df.iloc[index, 0] = str(datetime_object - timedelta(days=1))

def move_weekend_to_friday(df):
    for index, row in df.iterrows():
        datetime_object = get_datetime(df.iloc[index, 0])
        if datetime_object.weekday() == 5:
            df.iloc[index, 0] = str(datetime_object - timedelta(days=1))
        if datetime_object.weekday() == 6:
            df.iloc[index, 0] = str(datetime_object - timedelta(days=2))

if __name__ == '__main__':
    df = pd.read_csv(CURRENT_DIRECTORY + '/data/news/doc2vec_goog.csv')
    move_before_9am_to_previous_day(df)
    move_weekend_to_friday(df)

    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index(['time'])

    # average in 1 day
    df = df.resample('1D').mean().dropna()
    df.to_csv('sentiment_and_vector.csv')
