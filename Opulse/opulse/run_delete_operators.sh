#!/bin/bash


CONFIG_PATH=""
OPERATOR_FILE=""
OUTPUT_FILE=""


OPERATOR_IDS=()


OPERATOR_IDS_ARG=$(IFS=' ' ; echo "${OPERATOR_IDS[*]}")


python delete_operators_batch.py \
  --config "$CONFIG_PATH" \
  --operator-file "$OPERATOR_FILE" \
  --operator-ids $OPERATOR_IDS_ARG \
  --output-operator-file "$OUTPUT_FILE"

