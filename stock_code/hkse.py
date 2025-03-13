import pandas as pd
import pymysql
import os

# Read Excel file
excel_path = 'hkse.xlsx'
df = pd.read_excel(excel_path, dtype={'Stock Code': str}, skiprows=2)

# Check and clean column names
df.columns = df.columns.str.strip()

# Verify the column names to ensure 'Stock Code' is present
print("Columns in the DataFrame:", df.columns)

# Database configuration
host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
port = int(os.getenv('DB_PORT', 3306))  # Default to 3306 if not set
user = os.getenv('DB_USER', 'root')  # Default to 'root' if not set
password = os.getenv('DB_PASSWORD', '-')  # Default to '-' if not set
database = os.getenv('DB_NAME', '-')  # Default to '-' if not set

# Connect to database
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8mb4')
cursor = conn.cursor()

# Insert data
insert_query = """
INSERT INTO `stock_code` (`Stock Code`, `Company Name`, `Exchange`, `Available`)
VALUES (%s, %s, %s, %s)
"""

for _, row in df.iterrows():
    if not row['Category'] == "Equity":
        continue
    if not row['Sub-Category'] == "Equity Securities (Main Board)":
        continue
    stock_code = row['Stock Code']
    if stock_code == "":
        continue
    stock_code = str(stock_code) + ".HK"
    company_name = row['Name of Securities']
    exchange = 'HKSE'
    available = 'T'
    print(stock_code, company_name)
    cursor.execute(insert_query, (stock_code, company_name, exchange, available))

# Commit transaction
conn.commit()
cursor.close()
conn.close()

print("Data insertion completed!")
