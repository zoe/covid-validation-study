import google.auth
from google.cloud import bigquery as bq
from google.cloud import bigquery_storage_v1beta1 as bqs
import gcsfs
import pandas as pd
import argparse
import warnings

# get credentials
credentials, project_id = google.auth.default(
scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
gcp_fs = gcsfs.GCSFileSystem()


def run_query(credentials, project_id, query_template, start_date, end_date):
    # make clients
    bqclient = bq.Client(credentials=credentials,
                         project=project_id)
    bqsclient = bqs.BigQueryStorageClient(credentials=credentials)

    query = query_template.format(start_date=start_date, end_date=end_date)
    dframe = bqclient.query(query).result().to_dataframe(bqstorage_client=bqsclient)
    dframe['date_sick'] = pd.to_datetime(dframe['date_sick'])
    return dframe


if __name__ == '__main__':

    warnings.filterwarnings('ignore')

    parser = argparse.ArgumentParser()
    parser.add_argument("-start_date", help="Start date (YYYY-MM-DD)", type=str)
    parser.add_argument("-end_date", help="End date (YYYY-MM-DD)", type=str)
    parser.add_argument("-query_file", help="train / test query template", type=str)
    parser.add_argument("-outfile", help="Out file name", type=str)
    args = parser.parse_args()

    with open(args.query_file, 'r') as file:
        query_temp = file.read().replace('\n', '')

    df = run_query(credentials, project_id, query_temp, args.start_date, args.end_date)

    df.to_csv(args.outfile, index=False)