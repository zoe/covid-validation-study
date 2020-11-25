CONFIG = config.mk
include ${CONFIG}

# 1. Fetch data
## 1a Query

RAW_FILENAME = ${DATA_FOLDER_LOCAL}/raw_train_${START_DATE}_${SPLIT_DATE}

.PHONY: query
query: ${RAW_FILENAME}_done

${RAW_FILENAME}_done: ${CONFIG}
	@echo "Querying for training data between ${START_DATE} and ${SPLIT_DATE}"
	@mkdir -p ${DATA_FOLDER_LOCAL}
	python -m scripts.query \
	-start_date ${START_DATE} -end_date ${SPLIT_DATE} -outfile ${RAW_FILENAME}.csv
	@touch ${RAW_FILENAME}_done
	@echo "Created ${RAW_FILENAME}.csv"

## 1b Clean query output

PROCESSED_FILENAME = ${DATA_FOLDER_LOCAL}/processed_train_${START_DATE}_${SPLIT_DATE}

.PHONY: clean_data
clean_data: ${PROCESSED_FILENAME}_done

${PROCESSED_FILENAME}_done: ${RAW_FILENAME}_done
	@echo "Cleaning ${RAW_FILENAME}.csv"
	python -m scripts.clean_query_output \
	-inputfile ${RAW_FILENAME}.csv -outfile ${PROCESSED_FILENAME}.csv
	@touch ${PROCESSED_FILENAME}_done
	@echo "Created ${PROCESSED_FILENAME}.csv"

# 2. Train validation split

# 3. General preprocessing with the option to aggregate on episode-id level - OPTIONAL, we can do it later

# 4. Saving datasets to GCP with proper naming
