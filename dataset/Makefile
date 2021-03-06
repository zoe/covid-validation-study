CONFIG = config.mk
include ${CONFIG}

# 1. Fetch data
## 1a Query

ifeq ($(DATASET),train)
	RAW_FILENAME = ${DATA_FOLDER_LOCAL}/raw_${DATASET}_${START_DATE}_${SPLIT_DATE}_gen${GENERATION_DATE}
	PROCESSED_FILENAME = ${DATA_FOLDER_LOCAL}/processed_${DATASET}_${START_DATE}_${SPLIT_DATE}_gen${GENERATION_DATE}
	TRAIN_FILENAME = ${DATA_FOLDER_LOCAL}/split_train_${START_DATE}_${SPLIT_DATE}_gen${GENERATION_DATE}
	VAL_FILENAME = ${DATA_FOLDER_LOCAL}/split_validation_${START_DATE}_${SPLIT_DATE}_gen${GENERATION_DATE}
	TRAIN_AGGREGATED = ${TRAIN_FILENAME}_aggregated
	VAL_AGGREGATED = ${VAL_FILENAME}_aggregated
	FILE_DEP = train_split_done

else
	RAW_FILENAME = ${DATA_FOLDER_LOCAL}/raw_${DATASET}_${SPLIT_DATE}_gen${GENERATION_DATE}
	PROCESSED_FILENAME = ${DATA_FOLDER_LOCAL}/processed_${DATASET}_${SPLIT_DATE}_gen${GENERATION_DATE}
	TEST_AGGREGATED = ${PROCESSED_FILENAME}_aggregated
	FILE_DEP = cleaning_done
endif

.PHONY: query
query: query_done

query_done: ${CONFIG}
	@echo "Querying for training data between ${START_DATE} and ${SPLIT_DATE}"
	@mkdir -p ${DATA_FOLDER_LOCAL}
	python -m scripts.query \
	-start_date ${START_DATE} -end_date ${SPLIT_DATE} \
	-days_from_onset ${DAYS_ONSET} \
	-days_between_sick_test ${DAYS_SICK_TEST} -query_file sql/${DATASET}_query.txt \
	-outfile ${RAW_FILENAME}.csv -set_type ${DATASET}
	@touch query_done
	@echo "Created ${RAW_FILENAME}.csv"

## 1b Clean query output

.PHONY: clean_data
clean_data: cleaning_done

cleaning_done: query_done
	@echo "Cleaning ${RAW_FILENAME}.csv"
	python -m scripts.clean_query_output \
	-inputfile ${RAW_FILENAME}.csv -outfile ${PROCESSED_FILENAME}.csv
	@touch cleaning_done
	@echo "Created ${PROCESSED_FILENAME}.csv"

# 2. Train validation split

.PHONY: train_split
train_split: train_split_done

train_split_done: cleaning_done
	python -m scripts.make_split \
	-processed_data ${PROCESSED_FILENAME}.csv -fraction_validation ${VALIDATION_FRACTION} -output_train ${TRAIN_FILENAME} -output_val ${VAL_FILENAME}
	@touch train_split_done
	@echo "Split made! Training and validation created."

# 3. General preprocessing with the option to aggregate on episode-id level
# OPTIONAL, we can do it later
.PHONY: aggregate
aggregate: aggregate_done

aggregate_done: ${FILE_DEP}
	if [ "${FILE_DEP}" = "train_split_done" ]; then \
		python -m scripts.aggregate -processed_data ${TRAIN_FILENAME}.csv -output ${TRAIN_AGGREGATED}; \
		python -m scripts.aggregate -processed_data ${VAL_FILENAME}.csv -output ${VAL_AGGREGATED}; \
	else \
		python -m scripts.aggregate -processed_data ${PROCESSED_FILENAME}.csv -output ${TEST_AGGREGATED}; fi; \
	touch aggregate_done

# 4. Saving datasets to GCP with proper naming

.PHONY: GCP_save
GCP_save: GCP_save_done

GCP_save_done:
	@echo saving to GCP
	python -m scripts.upload_to_gcp \
	-start_date ${START_DATE} -split_date ${SPLIT_DATE} \
	-gen_date ${GENERATION_DATE} -freeze_date ${FREEZE_DATE} \
	-dataset ${DATASET} -gcp_folder ${DATA_FOLDER_GCP}
	@touch GCP_save_done

# Whole train and test pipeline

.PHONY: train_data
train_data: query clean_data train_split

.PHONY: test_data
test_data: query clean_data
