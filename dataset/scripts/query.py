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


def run_query(credentials, project_id, query_template, start_date, end_date, days_from_onset, days_between_sick_test, set_type):
    # make clients
    bqclient = bq.Client(credentials=credentials,
                         project=project_id)
    bqsclient = bqs.BigQueryStorageClient(credentials=credentials)
    if set_type == 'train':
        query = query_template.format(start_date=start_date, end_date=end_date, days_from_onset=days_from_onset, days_between_sick_test=days_between_sick_test)
    else: 
        query = query_template.format(start_date=end_date, days_from_onset=days_from_onset, days_between_sick_test=days_between_sick_test)
    dframe = bqclient.query(query).result().to_dataframe(bqstorage_client=bqsclient)
    dframe['date_sick'] = pd.to_datetime(dframe['date_sick'])
    return dframe


if __name__ == '__main__':

    warnings.filterwarnings('ignore')

    parser = argparse.ArgumentParser()
    parser.add_argument("-start_date", help="Start date (YYYY-MM-DD)", type=str)
    parser.add_argument("-end_date", help="End date (YYYY-MM-DD)", type=str)
    parser.add_argument("-days_from_onset", help="Days from the onset of symptoms", type=str)
    parser.add_argument("-days_between_sick_test", help="Max days between onset of symptoms and test", type=str)
    parser.add_argument("-query_file", help="train / test query template", type=str)
    parser.add_argument("-set_type", help='Type of set you want to generate', type=str)
    parser.add_argument("-outfile", help="Out file name", type=str)
    args = parser.parse_args()

    with open(args.query_file, 'r') as file:
        query_temp = file.read().replace('\n', '')

    df = run_query(credentials, project_id, query_temp, args.start_date, args.end_date, args.days_from_onset, args.days_between_sick_test, args.set_type)
    df.to_csv(args.outfile, index=False)
