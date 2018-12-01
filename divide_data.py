import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('data_all.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date'])

    training_data_condition = df.index < pd.Timestamp("2016-01-01 00:00:00")
    testing_data_condition = df.index >= pd.Timestamp("2016-01-01 00:00:00")

    training_data = df.loc[training_data_condition]
    testing_data = df.loc[testing_data_condition]

    training_data.to_csv('training_data.csv')
    testing_data.to_csv('testing_data.csv')
