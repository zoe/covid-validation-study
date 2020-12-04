# Validation study dataset generation pipeline

## About Makefiles

A nice [tutorial](https://makefiletutorial.com/) on makefiles. We only need really basic stuff but this is a good point of reference.

## Generate data

Note: if you need to rerun some part of the pipeline, you need to remove the files generates that are ending `done`.

### Training set

In `config.mk`, set `DATASET=train`. You'll also need to set the followings:
* generation date and freeze date define the name of the GCP folder where you'll save the files. Ideally, this should be the same for train and the corresponding test file.
* start date is the start of the training dataset
* split date is the end of the training dataset and the start of the future test set
```
# today's date, or when the train set is generated
GENERATION_DATE=1204
# this is the day when the model is intended to be frozen
FREEZE_DATE=2020-10-15

# training`/validation set start date
START_DATE=2020-04-01
# training/validation set end date and test set start date
SPLIT_DATE=2020-10-15
```

```
make train_data

#optional 
make aggregate

# optional
make gcp_save
```

### Test set

In `config.mk`, set `DATASET=test`. Make sure all other parameters are the way you want them to be, with attention to the freeze data and the generation date.
```
make test_data

#optional 
make aggregate

# optional
make gcp_save
```

#### Optional features

__make aggregate__  
* aggregates the records on episode_id level
* if the contributor ever logged fever in the report, fever will be True in the aggregate dataset

__make gcp_save__
* saves the train-validation split or the test set to GCP