#!/bin/bash


CONFIG_PATH="config/default.yaml"
OPERATORS_PATH=""
GENERATED_EXPRESSION_PATH=""
GENERATED_OPEXPRESS_DEPENDENCY_PATH=""


NUM=100
THREADS=1


python generate_expression.py --config "$CONFIG_PATH" \
                              --operators-path "$OPERATORS_PATH" \
                              --generated-expression-path "$GENERATED_EXPRESSION_PATH" \
                              --generated-opexpr-dependency-path "$GENERATED_OPEXPRESS_DEPENDENCY_PATH" \
                              --num "$NUM" \
                              --thread "$THREADS"


