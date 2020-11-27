import pandas as pd
import argparse
import warnings
import google.auth
import gcsfs
import os
import gzip

warnings.filterwarnings('ignore')
gcp_project_name = os.getenv('GOOGLE_CLOUD_PROJECT')
gcp_fs = gcsfs.GCSFileSystem(
    project=gcp_project_name
)


if __name__ == '__main__':

    warnings.filterwarnings('ignore')
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", help="Training filename", type=str)
    parser.add_argument("-val", help="Validation filename", type=str)
    parser.add_argument("-test", help="Test filename", type=str)
    parser.add_argument("-gcp_folder", help="GCP location", type=str)
    parser.add_argument("-dataset", help="dataset train/test", type=str)
    parser.add_argument("-gen_date", help="Date when training set ends and test starts", type=str)
    parser.add_argument("-freeze_date", help="Date when the model is intended to be frozen", type=str)
    args = parser.parse_args()

    file_counter=0
    folder_name = f'gen_{args.gen_date}_freeze_{args.freeze_date}'

    for fname in [args.test, args.train, args.val]:

        if os.path.exists(fname):
            print(f'Found {fname}')
            data = pd.read_csv(fname)
            short_filename = os.path.basename(fname)
            remote_path = os.path.join(args.gcp_folder,folder_name,short_filename)
            with gcp_fs.open(remote_path+'.gz', 'w') as file_obj:
                data.to_csv(file_obj, index=False, compression='gzip')
            print(f'{remote_path} written to GCP')

            file_counter+=1

    if file_counter > 0:
        remote_path=os.path.join(args.gcp_folder,folder_name,f'config_gen{args.gen_date}_freeze{args.freeze_date}_{args.dataset}.mk')
        gcp_fs.put('config.mk', remote_path)
        print(f'{remote_path} written to GCP')

