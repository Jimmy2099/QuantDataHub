import pandas as pd
import pymysql

# Read Excel file
excel_path = 'sse.xls'
df = pd.read_excel(excel_path)

# Database configuration
host = '-'
port = 0
user = '-'
password = '-'
database = '-'

# Connect to database
conn = pymysql.connect(host=host,port=port, user=user, password=password, database=database, charset='utf8mb4')
cursor = conn.cursor()

# Insert data
insert_query = """
INSERT INTO `stock_code` (`Stock Code`, `Company Name`, `Exchange`, `Available`)
VALUES (%s, %s, %s, %s)
"""

for _, row in df.iterrows():
    stock_code = row['A股代码']
    if pd.notna(row['A股代码']) == "":
        continue
    stock_code = str(stock_code) + ".SS"
    company_name = row['公司英文全称']
    exchange = 'SSE'
    available = 'T'
    cursor.execute(insert_query, (stock_code, company_name, exchange, available))

# Commit transaction
conn.commit()
cursor.close()
conn.close()

print("Data insertion completed!")
