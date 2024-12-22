#!/bin/bash


CONFIG_PATH=""
OPERATOR_FILE_PATH=""
OUTPUT_OPERATOR_FILE_PATH=""


python assign_operator_priority.py \
  --config "$CONFIG_PATH" \
  --operator-file "$OPERATOR_FILE_PATH" \
  --output-operator-file "$OUTPUT_OPERATOR_FILE_PATH"
