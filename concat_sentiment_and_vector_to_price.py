import fix_yahoo_finance as yf
import pandas as pd

if __name__ == '__main__':
    data = yf.download('GOOGL', start='2007-01-01', end='2016-12-27')
    print(data)

    df = pd.read_csv('sentiment_and_vector.csv')
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index(['time'])
    df.index.names = ['Date']
    print(df)

    # new_df = pd.merge(data, df, left_index=True, right_index=True)
    new_df = pd.concat([data, df], axis=1)
    print(new_df)
    new_df.to_csv('concat_sentiment_and_vector_to_price.csv')
