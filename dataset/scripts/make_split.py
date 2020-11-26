import pandas as pd
import numpy as np
import argparse
import warnings


#function to split the data
def make_split(pre_processed, fraction_validation):
    val_set = pd.DataFrame({})
    #define training set
    train_set = pd.DataFrame({})
    #ids that we already have
    ids_for_train = set()
    ids_for_val = set()
    #iterate over unique days
    for day in pre_processed.day_updated_at.unique():
        #get data for that day
        data = pre_processed[pre_processed.day_updated_at == day]
        #shuffle the data
        shuffled = data.sample(frac = 1)
        ids = shuffled.episode_id.unique()
        size_val = int(shuffled.episode_id.nunique() * fraction_validation)
        train_ids = ids[size_val:]
        val_ids = ids[:size_val]
        #check intersections
        inter_train_train = set(train_ids).intersection(ids_for_train)
        inter_train_val = set(train_ids).intersection(ids_for_val)
        inter_val_train = set(val_ids).intersection(ids_for_train)
        inter_val_val = set(val_ids).intersection(ids_for_val)
        #if we already have in train add to train
        if len(inter_train_train) != 0:
            #add to train
            train_set = pd.concat([train_set, shuffled[shuffled.episode_id.isin(inter_train_train)]])
            #remove id from train
            train_ids = set(train_ids).difference(inter_train_train)
        #if we already have in val add to val
        if len(inter_val_val) != 0:
            #add to train
            val_set = pd.concat([val_set, shuffled[shuffled.episode_id.isin(inter_val_val)]])
            #remove id from val
            val_ids = set(val_ids).difference(inter_val_val)
        #if we have train into val, add to val and remove id from train
        if len(inter_train_val) != 0:
            val_set = pd.concat([val_set, shuffled[shuffled.episode_id.isin(inter_train_val)]])
            #remove from the id list
            train_ids = set(train_ids).difference(inter_train_val)
        #if we have it in train, remove from val and add to train
        if len(inter_val_train) != 0:
            train_set = pd.concat([train_set, shuffled[shuffled.episode_id.isin(inter_val_train)]])
            #remove from the id list
            val_ids = set(val_ids).difference(inter_val_train)
        #you have unique remaining values
        remaining = set(train_ids).union(set(val_ids))
        #from these do same props
        frac_val = int(len(remaining) * fraction_validation)
        ids_rem_train = list(remaining)[frac_val:]
        ids_rem_val = list(remaining)[:frac_val]
        train_set = pd.concat([train_set, shuffled[shuffled.episode_id.isin(ids_rem_train)]])
        val_set = pd.concat([val_set, shuffled[shuffled.episode_id.isin(ids_rem_val)]])
        ids_for_train = ids_for_train.union(ids_rem_train)
        ids_for_val = ids_for_val.union(ids_rem_val)
    return train_set, val_set

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    parser = argparse.ArgumentParser()
    parser.add_argument("-processed_data", help="This is the pre-processed data", type=str)
    parser.add_argument("-fraction_validation", help="This is the fraction of data to insert in validation", type=float)
    parser.add_argument("-output_train", help="This is the path where we save the train data", type=str)
    parser.add_argument("-output_val", help="This is the path where we save the validation data", type=str)
    args = parser.parse_args()
    #read the data
    processed_data = pd.read_csv(args.processed_data)
    #make the split
    train_set, val_set = make_split(processed_data, args.fraction_validation)
    #save the split data
    train_set.to_csv(args.output_train, index = False)
    val_set.to_csv(args.output_val, index = False)
    

