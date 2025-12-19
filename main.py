import pandas as pd

# globals
prev_ema = -1

def fetch_data():
    df = pd.read_csv('data/output_file.csv', parse_dates=['date'])
    df = df.astype({'ticker': 'string'})

    return df

def monthly_aggregation(df):
    f = {'open': 'first', 'close': 'last', 'high': 'max', 'low': 'min'}
    monthly = df.sort_values('date').groupby(['ticker', pd.Grouper(key='date', freq='ME')], observed=True).agg(f).reset_index()#.drop(columns=['date'])

    return monthly

def sma(df, window):
    return df.rolling(window=window).mean()

def add_sma(df, col, periods):
    for period in periods:
        df[f'sma_{period}'] = sma(df[col], period)

    return df

def ema(x, window):
    global prev_ema

    cur_price = x[-1]
    mult = 2 / (window + 1)
    ema = (cur_price - prev_ema) * mult + prev_ema
    prev_ema = ema

    return ema

def add_ema(df, col, periods):
    global prev_ema

    for period in periods:
        prev_ema = sma(df[col], period).dropna().iloc[0]
        df[f'ema_{period}'] = df[col].rolling(window=period).apply(lambda x: ema(x, period), raw=True)
        
    return df

def add_techincal_indicators(df):
    symbol = set(df["ticker"].values).pop()
    df = add_sma(df, 'close', [10, 20])
    df = add_ema(df, 'close', [10, 20])

    return df, symbol

def generate_result_files(df):
    for i in range(0, len(df), 24):
        res, SYMBOL = add_techincal_indicators(df[i : i + 24].copy())
        print(f"Generating {SYMBOL} report")
        res.to_csv(f'output/result_{SYMBOL}.csv', index=False)


if __name__ == "__main__":
    df = fetch_data()
    monthly = monthly_aggregation(df)
    generate_result_files(monthly)
