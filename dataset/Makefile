CONFIG = config.mk
include ${CONFIG}

# 1. Fetch data
## 1a Query

RAW_FILENAME = ${DATA_FOLDER_LOCAL}/raw_${DATASET}_${START_DATE}_${SPLIT_DATE}

query: query_done

query_done: ${CONFIG}
	@echo "Querying for training data between ${START_DATE} and ${SPLIT_DATE}"
	@mkdir -p ${DATA_FOLDER_LOCAL}
	python -m scripts.query \
	-start_date ${START_DATE} -end_date ${SPLIT_DATE} -days_from_onset ${DAYS_ONSET} -days_between_sick_test ${DAYS_SICK_TEST} -query_file sql/${DATASET}_query.txt -outfile ${RAW_FILENAME}.csv -set_type $(DATASET)
	@touch query_done
	@echo "Created ${RAW_FILENAME}.csv"

## 1b Clean query output

PROCESSED_FILENAME = ${DATA_FOLDER_LOCAL}/processed_${DATASET}_${START_DATE}_${SPLIT_DATE}

clean_data: cleaning_done

cleaning_done: query_done
	@echo "Cleaning ${RAW_FILENAME}.csv"
	python -m scripts.clean_query_output \
	-inputfile ${RAW_FILENAME}.csv -outfile ${PROCESSED_FILENAME}.csv
	@touch cleaning_done
	@echo "Created ${PROCESSED_FILENAME}.csv"

# 2. Train validation split

# these are not used yet
TRAIN_FILENAME = ${DATA_FOLDER_LOCAL}/split_train_${START_DATE}_${SPLIT_DATE}_gen$(shell date +%m%d)
VAL_FILENAME = ${DATA_FOLDER_LOCAL}/split_validation_${START_DATE}_${SPLIT_DATE}_gen$(shell date +%m%d)

train_split: train_split_done

train_split_done: cleaning_done
	python -m scripts.make_split \
	-processed_data ${PROCESSED_FILENAME}.csv -fraction_validation ${VALIDATION_FRACTION} -output_train ${TRAIN_FILENAME} -output_val ${VAL_FILENAME}
	@touch train_split_done
	@echo "Split made! Training and validation created."

# 3. General preprocessing with the option to aggregate on episode-id level
# OPTIONAL, we can do it later

# 4. Saving datasets to GCP with proper naming

GCP_save: GCP_save_done

GCP_save_done: cleaning_done
	@echo saving to GCP
	python -m scripts.upload_to_gcp \
	-train ${TRAIN_FILENAME}.csv -val ${VAL_FILENAME}.csv -test ${PROCESSED_FILENAME}.csv \
	-gcp_folder ${DATA_FOLDER_GCP} -split_date ${SPLIT_DATE}
	@touch GCP_save_done

# Whole train and test pipeline

train_data: query clean_data train_split
test_data: query clean_data
