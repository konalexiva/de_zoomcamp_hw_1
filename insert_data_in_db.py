import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import argparse
import os


def main(params):
    csv_url = params.csv_url
    csv_archive_path = params.csv_archive_path
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    csv_path = params.csv_path

    os.system(f"wget {csv_url} -O {csv_archive_path}")
    os.system(f"gunzip {csv_archive_path}")

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    )

    df_iter = pd.read_csv(f"{csv_path}", iterator=True, chunksize=10000)

    for df in df_iter:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists="append")


if __name__ == "__main__":

    load_dotenv()

    parser = argparse.ArgumentParser(description="ingest csv into db")

    parser.add_argument(
        "--csv_url", help="url for csv tar", default=os.environ.get("CSV_URL")
    )
    parser.add_argument(
        "--csv_archive_path", help="local path for csv", default=os.environ.get("CSV_ARCHIVE_PATH")
    )
    parser.add_argument(
        "--user", help="username for db", default=os.environ.get("POSTGRES_USER")
    )
    parser.add_argument(
        "--password",
        help="password for db",
        default=os.environ.get("POSTGRES_PASSWORD"),
    )
    parser.add_argument(
        "--host", help="host for db", default=os.environ.get("POSTGRES_HOST")
    )
    parser.add_argument("--port", help="port for db", default=5432)
    parser.add_argument(
        "--db", help="database name for db", default=os.environ.get("POSTGRES_DB")
    )
    parser.add_argument(
        "--table_name",
        help="table name for db",
        default=os.environ.get("POSTGRES_TABLE"),
    )
    parser.add_argument(
        "--csv_path", help="path for csv", default=os.environ.get("CSV_PATH")
    )

    args = parser.parse_args()

    main(args)
