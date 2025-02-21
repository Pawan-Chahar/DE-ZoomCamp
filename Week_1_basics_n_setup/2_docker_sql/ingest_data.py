
import os 
import argparse 

from time import time 
import pandas as pd 
import pyarrow 
import wget 
 
from sqlalchemy import create_engine 
from sqlalchemy.exc import OperationalError

def main(params):
    try:
            
        user = params.user
        password = params.password
        host = params.host
        port = params.port
        db = params.db
        table_name = params.table_name
        url = params.url


        #result = os.system(f"wget {url} ")



       # Set file paths
        current_dir = os.getcwd()
        output_file_parquet = os.path.join(current_dir, "yellow_tripdata_2024.parquet")
        output_file_csv = os.path.join(current_dir, "yellow_tripdata_2024.csv")

        #result = wget.download(f'{url}')
         # Download the parquet file
        print(f"Downloading file from {url}...")
        wget.download(url, output_file_parquet)
        print("\nDownload completed.")

        # Read parquet file and save it as CSV
        print("Converting parquet file to CSV...")
        df = pd.read_parquet(output_file_parquet)
        df.to_csv(output_file_csv, index=False)
        print("Conversion completed.")



        
        # Create PostgreSQL engine
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        
        # Test connection
        with engine.connect() as conn:
            print("Database connection successful!")

        # Load data into PostgreSQL in chunks
        print("Ingesting data into PostgreSQL...")

        df_iter = pd.read_csv(output_file_csv, iterator=True, chunksize=100000)
        df = next(df_iter)

        # Create table structure
        df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

        # Insert first chunk
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    
    

        while True:
            try:

                t_start = time()

                df = next(df_iter)

                df.to_sql(name=table_name, con= engine, if_exists='append',index=False)

                t_end = time()

                print(f'Inserted another chunk........, took %.3f seconds' % (t_end - t_start))
            
            except StopIteration:
                print("Finished ingesting data into the postgres database")
                break

        engine.dispose()

    except OperationalError as e:
        print(f"Failed to connect to database: {e}")
        



       
       #user , password , host , port , database name , table name 
#url of the parquet 







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)

    