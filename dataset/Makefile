CONFIG = config.mk
include ${CONFIG}

# 1. Fetch data
## 1a Query

RAW_FILENAME = ${DATA_FOLDER_LOCAL}/raw_${DATASET}_${START_DATE}_${SPLIT_DATE}

query: ${RAW_FILENAME}_done

${RAW_FILENAME}_done: ${CONFIG}
	@echo "Querying for training data between ${START_DATE} and ${SPLIT_DATE}"
	@mkdir -p ${DATA_FOLDER_LOCAL}
	python -m scripts.query \
	-start_date ${START_DATE} -end_date ${SPLIT_DATE} -query_file sql/${DATASET}_query.txt -outfile ${RAW_FILENAME}.csv
	@touch ${RAW_FILENAME}_done
	@echo "Created ${RAW_FILENAME}.csv"

## 1b Clean query output

PROCESSED_FILENAME = ${DATA_FOLDER_LOCAL}/processed_${DATASET}_${START_DATE}_${SPLIT_DATE}

clean_data: ${PROCESSED_FILENAME}_done

${PROCESSED_FILENAME}_done: ${RAW_FILENAME}_done
	@echo "Cleaning ${RAW_FILENAME}.csv"
	python -m scripts.clean_query_output \
	-inputfile ${RAW_FILENAME}.csv -outfile ${PROCESSED_FILENAME}.csv
	@touch ${PROCESSED_FILENAME}_done
	@echo "Created ${PROCESSED_FILENAME}.csv"

# 2. Train validation split

# these are not used yet
TRAIN_FILENAME = ${DATA_FOLDER_LOCAL}/${DATASET}_${START_DATE}_${SPLIT_DATE}_train.csv
TEST_FILENAME = ${DATA_FOLDER_LOCAL}/${DATASET}_${START_DATE}_${SPLIT_DATE}_test.csv

train_split: train_split_done

train_split_done: ${PROCESSED_FILENAME}_done
	@echo doing the split
	@touch train_split_done

# 3. General preprocessing with the option to aggregate on episode-id level - OPTIONAL, we can do it later

# 4. Saving datasets to GCP with proper naming

#GCP_save

GCP_save: GCP_save_done

GCP_save_done: ${PROCESSED_FILENAME}_done
	@echo saving to GCP
	@touch GCP_save_done

# Whole train and test pipeline

train_data: query clean_data train_split GCP_save
test_data: query clean_data GCP_save