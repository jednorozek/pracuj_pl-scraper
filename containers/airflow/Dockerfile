FROM apache/airflow:2.2.0
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install --no-cache-dir beautifulsoup4 pandas sqlalchemy psycopg2-binary