import pandas as pd
import argparse
import warnings

def rename_column(data, old_name, new_name):
    return data.rename(columns={old_name: new_name})


if __name__ == '__main__':

    warnings.filterwarnings('ignore')

    parser = argparse.ArgumentParser()
    parser.add_argument("-inputfile", help="Raw file to clean", type=str)
    parser.add_argument("-outfile", help="Outputfile", type=str)
    args = parser.parse_args()

    df = pd.read_csv(args.inputfile)
    rename_column(df, old_name='f0_', new_name='number_of_contributors').to_csv(args.outfile, index=False)
