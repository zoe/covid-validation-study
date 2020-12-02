import pandas as pd
import numpy as np
import argparse



#define a function to aggregate the features on episode ID
def aggregate_features(df):
    return pd.concat([df.groupby(['episode_id']).agg(lambda x: x.sum()/ x.shape[0]),
                      df.groupby(['episode_id'])['result'].mean()], axis=1).reset_index()


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument("-processed_data", help="Processed data to aggregate")
    parser.add_argument("-output", help="Output file")
    args = parser.parse_args()
    #pass the raw file to clean
    df = pd.read_csv(args.processed_data)
    df = aggregate_features(df)
    df.to_csv(args.output+'.csv', index=False)

