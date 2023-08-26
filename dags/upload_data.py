import pandas as pd
import time
from sqlalchemy import create_engine

engine = create_engine('postgresql://airflow:airflow@postgres:5432/airflow')

df_iter = pd.read_csv( 
    '/opt/airflow/dags/out.csv', 
    iterator=True, 
    chunksize=10
)

def upload():
    for chunk in df_iter:
        t_start = time.time()
        chunk.to_sql(name='job_offers', con=engine, if_exists='append')
        t_end = time.time()
        print(f'inserted another chunk..., took {t_end - t_start:.3f} seconds')
        
