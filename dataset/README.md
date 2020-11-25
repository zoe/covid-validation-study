# Validation study dataset generation pipeline

## Intro to makefiles + folder structure

For now, this folder contains some example scripts, a Makefile and a config file to demonstrate how Makefiles work. You can try them by running 

```
cd covid-validation-study/dataset
make query
make clean data
```

A nice [tutorial](https://makefiletutorial.com/) on makefiles. We only need really basic stuff but this is a good point of reference.

### Training set

```
make train_data
```

### Test set

```
make test_data
```