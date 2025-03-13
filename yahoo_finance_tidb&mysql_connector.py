import yfinance as yf
import pandas as pd
import time
from flask import Flask
import datetime
import requests
import mysql.connector
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mattermost server configuration
enable_message_notify = False
mattermost_url = "https://na.com"
team_name = "-"
channel_id = "-"
token = "-"

host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
port = int(os.getenv('DB_PORT', 3306))  # Default to 3306 if not set
user = os.getenv('DB_USER', 'root')  # Default to 'root' if not set
password = os.getenv('DB_PASSWORD', '-')  # Default to '-' if not set
database = os.getenv('DB_NAME', '-')  # Default to '-' if not set

app = Flask(__name__)

# Create database connection
# TIDB
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port,
    charset='utf8mb4',
    autocommit=True,
    use_pure=True,
)

# Create cursor object
cursor = conn.cursor()


def mysql_upsert(table, data_iter):
    sql = "INSERT IGNORE INTO finance.stock_market_data " \
          "(`Date`, `Stock Code`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`) VALUES "
    logging.info("data len: %s", len(data_iter))
    for data in data_iter:
        # Avoid to use ORM
        result = sql + f"('{data['Date']}', '{data['Stock Code']}', {data['Open']}, {data['High']}, " \
                       f"{data['Low']}, {data['Close']}, {data['Adj Close']}, {data['Volume']}) "
        cursor.execute(result)


def download(stock_code, begin_date, end_date):
    data = yf.download(stock_code, start=begin_date, end=end_date)
    data = pd.DataFrame(data)
    data.insert(0, "Stock Code", stock_code)
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].dt.strftime("%Y-%m-%d 00:00:00")
    mysql_upsert('stock_market_data', data.to_dict(orient='records'))


def update_data(begin_date, end_date):
    company_code_list = []
    cu = conn.cursor()

    query = "SELECT `Stock Code` as code FROM stock_code WHERE `Available` = 'T' ORDER BY `Stock Code` ASC"

    cu.execute(query)
    for row in cu.fetchall():
        company_code_list.append(row[0])
    cu.close()

    logging.info("Stock List: %s,%s", company_code_list, len(company_code_list))

    for company_code in company_code_list:
        logging.info("%s", company_code)
        download(company_code, begin_date, end_date)
        # download(company_code,"2000-01-01","2023-07-01")
        time.sleep(1.5)


# download("AAPL","2000-01-01","2023-07-01")


# API endpoint for creating a new post
api_endpoint = f"{mattermost_url}/api/v4/posts"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}


def message_notify(msg=""):
    if not enable_message_notify:
        logging.info("message:%s", msg)
        return
    # Post data
    post_data = {
        "channel_id": channel_id,
        "message": msg,
    }
    # Make the API request to create a new post
    response = requests.post(api_endpoint, headers=headers, json=post_data)
    # Check the response status
    if response.status_code == 201:
        logging.info("Post created successfully!")
    else:
        logging.info("Failed to create post. Status code: %s, %s ", response.status_code, response.text)


@app.route('/')
def index():
    t1 = time.time()
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    message_notify("Updating stock data, begin_date:" + begin_date + "end_date:" + end_date)
    update_data(begin_date, end_date)
    t2 = time.time()
    message_notify("Stock data update completed, begin_date:" + begin_date + "end_date:" + end_date + "Time taken:" + str(t2 - t1) + "s")
    return 'exec time: ' + str(t2 - t1)


def main(
        begin_date="",
        end_date="",
):
    t1 = time.time()
    if begin_date == "" or end_date == "":
        begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    logging.info("begin_date: %s, end_date:%s ", begin_date, end_date)
    message_notify("Updating stock data, begin_date:" + begin_date + "end_date:" + end_date)
    update_data(begin_date, end_date)
    t2 = time.time()
    message_notify("Stock data update completed, begin_date:" + begin_date + "end_date:" + end_date + "Time taken:" + str(t2 - t1) + "s")
    return {"exec_time": str(t2 - t1)}

# main()
