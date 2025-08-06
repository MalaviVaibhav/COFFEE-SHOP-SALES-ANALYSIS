import pandas as pd
from sqlalchemy import create_engine
import os
import time
import logging

# Create logs folder if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Basic logging setup
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filemode="a"
)

# MySQL connection
host = "localhost"
user = "root"
password = "Bobby$Data123"
database = "datas"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)

def ingest(df, tablename):
    # Make table name lowercase and replace spaces
    tablename = tablename.lower().replace(' ', '_')
    df.to_sql(tablename, con=engine, if_exists="append", index=False)

def load_row_data():
    start = time.time()
    data = r'D:\POWERBI-PROJECTS\Coffee Sales Analysis'
    
    for file in os.listdir(data):
        if file.endswith(".csv"):
            try:
                file_path = os.path.join(data, file)
                print(f"Processing {file}")
                df = pd.read_csv(file_path)
                
                # Create table name from filename
                table_name = file.replace('.csv', '')
                

                ingest(df, table_name)
                print(f"Success: {file} to table {table_name.lower().replace(' ', '_')}")
                
            except Exception as e:
                print(f"Error: {str(e)}")
    
    total_time = (time.time() - start) / 60
    print(f"Total time: {total_time:.2f} minutes")
    engine.dispose()

# Run the function
if __name__ == "__main__":
    load_row_data()