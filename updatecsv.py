import mysql.connector
import pandas as pd
import numpy as np
from mysql.connector import Error

try:
# MySQL connection
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='shansgan98',
        database='clientquerydb9'
    )
    cursor = conn.cursor()
    
# Read CSV file
    df = pd.read_csv("D:/guvi - project CRM/env/Scripts/synthetic static.csv")
    df = df.replace({np.nan: None})
    
# Bulk insert 
    insert_query = """
    INSERT INTO pastqueries
    (id, client_email, client_mobile, query_heading, query_description, status, date_raised, date_closed)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

# Convert DataFrame to list of tuples
    data_to_insert = [tuple(row) for row in df.values]
    
# Execute bulk insert
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    
    print(f"Successfully inserted {cursor.rowcount} rows")
    
except Error as e:
    print(f"Error: {e}")
    
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
