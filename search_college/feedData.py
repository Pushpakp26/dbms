import mysql.connector
import pandas as pd

host = "localhost"
port = 3307
user = "root"
password = ""
database = "CM_SYSTEM"
table_name = "search_app_cutoff"
csv_file = "mhtcet.csv"

conn = mysql.connector.connect(host=host, port=port, user=user, passwd=password, db=database)
cursor = conn.cursor()

df = pd.read_csv(csv_file)
data = df.values.tolist() 
columns = ', '.join(df.columns)

for i in range(len(data)): 
    data[i].insert(0, i+1)
    insert_data = tuple(data[i])
    sql = f"INSERT INTO {table_name} VALUES {insert_data}"  
    print(f"({i+1}) Record Inserted!")
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted into MySQL.")
