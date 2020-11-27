# Validation study dataset generation pipeline

## About Makefiles

A nice [tutorial](https://makefiletutorial.com/) on makefiles. We only need really basic stuff but this is a good point of reference.

## Generate data

Note: if you need to rerun some part of the pipeline, you need to remove the files generates that are ending `done`.

### Training set

In `config.mk`, set `DATASET=train`.
```
make train_data

make gcp_save #(optional)
```

### Test set

In `config.mk`, set `DATASET=test`.
```
make test_data

make gcp_save #(optional)
```