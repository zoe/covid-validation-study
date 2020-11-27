# dataset pipeline generation parameters
# options are train and test
DATASET=train
GENERATION_DATE=1125
# this is the day when the model is intended to be frozen
FREEZE_DATE=2020-12-01

# training/validation set start date
START_DATE=2020-04-01
# training/validation set end date and test set start date
SPLIT_DATE=2020-10-15
# test set end dates
#TEST_END_DATE=2020-11-25
# number days from the onset of symptoms
DAYS_ONSET=3
#max number of days between falling sick and test
DAYS_SICK_TEST=10
VALIDATION_FRACTION=0.2
DATA_FOLDER_LOCAL=data
DATA_FOLDER_GCP=covid-internal-data/covid-validation-study

# other things we might want to define here
# - what you want to call the file
# - if it's training (training + validation) or test
# - if you want to aggregate on episode ID or not
# - (if you want to add nhs-region level prevalence data)
