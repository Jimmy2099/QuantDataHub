import pandas as pd
import talib
import pymysql
import os

host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
port = int(os.getenv('DB_PORT', 3306))  # Default to 3306 if not set
user = os.getenv('DB_USER', 'root')  # Default to 'root' if not set
password = os.getenv('DB_PASSWORD', '-')  # Default to '-' if not set
database = os.getenv('DB_NAME', '-')  # Default to '-' if not set


# 1. Load data from the database
def load_data_from_db(stock_code, start_date, end_date, db_query_sec_record_num_limit=20000):
    try:
        with pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4'
        ) as conn:
            # Query to get stock market data
            query = f"""
            SELECT `Date`, `Stock Code`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`
            FROM `stock_market_data`
            WHERE `Stock Code` = '{stock_code}' AND `Date` BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY `Date` ASC
            LIMIT {db_query_sec_record_num_limit}
            """

            # Use pandas to load data from MySQL into DataFrame
            df = pd.read_sql(query, conn)

            # Ensure 'Date' column is of datetime type
            df['Date'] = pd.to_datetime(df['Date'])

            return df

    except pymysql.MySQLError as e:
        print(f"Database connection or query failed: {e}")
        return None


# 2. Calculate stock indicators
def calculate_indicators(df):
    print("Calculating indicators...")
    # Initialize a dictionary to store all indicators
    indicators = {}

    # Chaikin A/D Line (AD)
    indicators['AD'] = talib.AD(df['High'], df['Low'], df['Close'], df['Volume'])

    # Chaikin A/D Oscillator (ADOSC)
    indicators['ADOSC'] = talib.ADOSC(df['High'], df['Low'], df['Close'], df['Volume'])

    # Average Directional Movement Index (ADX)
    indicators['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'])

    # Average Directional Movement Index Rating (ADXR)
    indicators['ADXR'] = talib.ADXR(df['High'], df['Low'], df['Close'])

    # Absolute Price Oscillator (APO)
    indicators['APO'] = talib.APO(df['Close'])

    # Aroon
    indicators['AROON'] = talib.AROON(df['High'], df['Low'])

    # Aroon Oscillator
    indicators['AROONOSC'] = talib.AROONOSC(df['High'], df['Low'])

    # Average True Range (ATR)
    indicators['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'])

    # Bollinger Bands (BBANDS)
    indicators['BBANDS_upper'], indicators['BBANDS_middle'], indicators['BBANDS_lower'] = talib.BBANDS(df['Close'])

    # Commodity Channel Index (CCI)
    indicators['CCI'] = talib.CCI(df['High'], df['Low'], df['Close'])

    # Exponential Moving Average (EMA)
    indicators['EMA'] = talib.EMA(df['Close'])

    # Moving Average Convergence/Divergence (MACD)
    indicators['MACD'], indicators['MACD_signal'], indicators['MACD_hist'] = talib.MACD(df['Close'])

    # Relative Strength Index (RSI)
    indicators['RSI'] = talib.RSI(df['Close'])

    # Simple Moving Average (SMA)
    indicators['SMA'] = talib.SMA(df['Close'])

    # Stochastic Oscillator (STOCH)
    indicators['STOCH_k'], indicators['STOCH_d'] = talib.STOCH(df['High'], df['Low'], df['Close'])

    # True Range (TRANGE)
    indicators['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])

    # Williams' %R (WILLR)
    indicators['WILLR'] = talib.WILLR(df['High'], df['Low'], df['Close'])

    return indicators


# 3. Main program
def calc_stock_indicators(stock_code, start_date, end_date, record_num_limit=14):
    # 1. Load data from the database
    df = load_data_from_db(stock_code, start_date, end_date, record_num_limit)

    if df is not None:
        df_with_indicators = calculate_indicators(df)

        print(df_with_indicators)


# Example call
if __name__ == "__main__":
    calc_stock_indicators('AAPL', '2022-01-01', '2022-12-31')
