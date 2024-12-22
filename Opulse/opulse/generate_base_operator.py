import argparse
from operatorplus import *
from expression.expression_generator import ExpressionGenerator
from config import LogConfig, ParamConfig


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Generate operators based on given configuration.")
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')
    parser.add_argument('--operator-file', type=str, required=True, help='Path to the input operator file')
    parser.add_argument('--output-file', type=str, required=True, help='Path to save the generated operators')

    # Parse arguments
    args = parser.parse_args()

    # Load configuration and logging using command line arguments
    config = ParamConfig(args.config)  # Use the passed config path
    logging_config = config.get_logging_config()
    log = LogConfig(logging_config)

    # Initialize OperatorManager using the passed operator file path
    op_manager = OperatorManager(args.operator_file, config, log)

    # Initialize Generators
    condition_generator = ConditionGenerator(config, log, op_manager)
    expr_generator = ExpressionGenerator(config, log, op_manager)
    op_generator = OperatorGenerator(
        param_config=config, 
        logger=log, 
        condition_generator=condition_generator, 
        expr_generator=expr_generator,
        operator_manager=op_manager
    )

    # Generate base operators
    op_generator.generate_base_operators()

    # Save generated operators to file
    op_manager.save_operators_to_jsonl(args.output_file)  # Save to the output path from command line
    print(f"Generated operators saved to {args.output_file}")
