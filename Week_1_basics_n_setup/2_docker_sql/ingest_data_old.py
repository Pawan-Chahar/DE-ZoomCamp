
import os 
import argparse 

from time import time 
import pandas as pd 
import pyarrow 
import pyarrow.parquet as pq 

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

        output_file_path_csv = 'yellow_tripdata_2024.csv'

        # Get the current directory
        current_dir = os.getcwd()

    # Set the output file path in the current directory
        output_file_path = os.path.join(current_dir, "yellow_tripdata_2024.parquet")


        #result = wget.download(f'{url}')

        wget.download(url , output_file_path)

        df = pd.read_parquet(output_file_path)


        df.to_csv(output_file_path_csv , index=False)

        df_iter = pd.read_csv(output_file_path_csv, iterator=True , chunksize=100000)
        
        df = next(df_iter)


        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        # Test connection
        with engine.connect() as conn:
            print("Database connection successful!")
    
        df.head(n=0).to_sql(name= table_name ,con=engine , if_exists='replace' )


        df.to_sql(name=table_name ,con=engine , if_exists='append')
    
    except OperationalError as e:
        print(f"Failed to connect to database: {e}")
        return


    while True:
        try:

            t_start = time()

            df = next(df_iter)

            df.to_sql(name=table_name, con= engine, if_exists='replace',index=False)

            t_end = time()

            print('Inserted another chunk........, took %.3f seconds' % (t_end - t_start))
        
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break


       
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

    