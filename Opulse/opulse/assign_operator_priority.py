import argparse
import logging
from operatorplus import *
from expression.expression_generator import ExpressionGenerator
from config import LogConfig, ParamConfig

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate and assign priorities to operators.")
    
    parser.add_argument('--config', type=str, required=True, help="Path to the config file")
    parser.add_argument('--operator-file', type=str, required=True, help="Path to the operator input JSONL file")
    parser.add_argument('--output-operator-file', type=str, required=True, help="Path to save the generated operators")
    
    args = parser.parse_args()
    
    # Load config
    config = ParamConfig(args.config)
    
    # Setup logging
    logging_config = config.get_logging_config()
    log = LogConfig(logging_config)
    
    # Initialize OperatorManager
    op_manager = OperatorManager(args.operator_file, config, log)
    
    # Initialize OperatorPriorityManager and assign priorities
    op_priority_manager = OperatorPriorityManager(log, op_manager)
    op_priority_manager.assign_priorities()

    # Save the operators to the specified output file
    op_manager.save_operators_to_jsonl(args.output_operator_file)
