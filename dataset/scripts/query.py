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


def get_newly_sick_by_result(credentials, project_id, start_date, end_date):
    # make clients
    bqclient = bq.Client(credentials=credentials,
                         project=project_id)
    bqsclient = bqs.BigQueryStorageClient(credentials=credentials)

    # get data from BigQuery
    query = f'''
    select
        date_sick,
        result,
        count(distinct patient_id)
        from `intermediate_data.newly_sick_with_test_results`
        where result in ('positive', 'negative')
        AND date_sick BETWEEN "{start_date}" AND "{end_date}"
        group by date_sick, result
    '''
    dframe = bqclient.query(query).result().to_dataframe(bqstorage_client=bqsclient)
    dframe['date_sick'] = pd.to_datetime(dframe['date_sick'])
    return dframe


if __name__ == '__main__':

    warnings.filterwarnings('ignore')

    parser = argparse.ArgumentParser()
    parser.add_argument("-start_date", help="Start date (YYYY-MM-DD)", type=str)
    parser.add_argument("-end_date", help="End date (YYYY-MM-DD)", type=str)
    parser.add_argument("-outfile", help="Out file name", type=str)
    args = parser.parse_args()

    df = get_newly_sick_by_result(credentials, project_id, args.start_date, args.end_date)

    df.to_csv(args.outfile, index=False)