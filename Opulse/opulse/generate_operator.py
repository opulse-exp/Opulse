from lark import Lark
import argparse
from operatorplus import *
from expression.expression_generator import ExpressionGenerator
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
import ast
from config import LogConfig, ParamConfig
from typing import Dict, Any
import random

global config
global logger
global compute_func, count_func

def check_syntax(code: str) -> bool:
    logger.debug(f"Checking syntax for code: {code}")
    try:
        ast.parse(code)
        logger.info("Syntax is valid.")
        return True  
    except SyntaxError as e:
        logger.error(f"Syntax error: {e}")
        return False

@given(st.integers())
@settings(max_examples=100)
def test_unary_op_compute_func(a: int):
    # logger.debug(f"Running test_unary_op_compute_func with a: {a}")
    try:
        result = compute_func(a)
        # logger.debug(f"Result of compute_func: {result}")
        assert isinstance(result, (int, str)), f"Expected result to be either an integer or a string, but got {type(result)}"
        # logger.info(f"test_unary_op_compute_func passed for a: {a}")
    except Exception as e:
        logger.error(f"Error in test_unary_op_compute_func with a: {a} - {e}")

@given(st.integers())
@settings(max_examples=100)
def test_unary_op_count_func(a: int):
    # logger.debug(f"Running test_unary_op_count_func with a: {a}")
    try:
        result = count_func(a)
        # logger.debug(f"Result of count_func: {result}")
        assert isinstance(result, (int, str)), f"Expected result to be either an integer or a string, but got {type(result)}"
        # logger.info(f"test_unary_op_count_func passed for a: {a}")
    except Exception as e:
        logger.error(f"Error in test_unary_op_count_func with a: {a} - {e}")

@given(st.integers(), st.integers())
@settings(max_examples=100)
def test_binary_op_compute_func(a: int, b: int):
    # logger.debug(f"Running test_binary_op_compute_func with a: {a}, b: {b}")
    try:
        result = compute_func(a, b)
        # logger.debug(f"Result of compute_func: {result}")
        assert isinstance(result, (int, str)), f"Expected result to be either an integer or a string, but got {type(result)}"
        # logger.info(f"test_binary_op_compute_func passed for a: {a}, b: {b}")
    except Exception as e:
        logger.error(f"Error in test_binary_op_compute_func with a: {a}, b: {b} - {e}")

@given(st.integers(), st.integers())
@settings(max_examples=100)
def test_binary_op_count_func(a: int, b: int):
    # logger.debug(f"Running test_binary_op_count_func with a: {a}, b: {b}")
    try:
        result = count_func(a, b)
        # logger.debug(f"Result of count_func: {result}")
        assert isinstance(result, (int, str)), f"Expected result to be either an integer or a string, but got {type(result)}"
        # logger.info(f"test_binary_op_count_func passed for a: {a}, b: {b}")
    except Exception as e:
        logger.error(f"Error in test_binary_op_count_func with a: {a}, b: {b} - {e}")

def test_syntax_validity(op_compute_func: str, op_count_func: str) -> bool:
    logger.debug(f"Testing syntax validity for op_compute_func: {op_compute_func} and op_count_func: {op_count_func}")
    if check_syntax(op_compute_func) and check_syntax(op_count_func):
        logger.info("Both operator functions have valid syntax.")
        return True
    else:
        logger.error("One or both operator functions have syntax errors.")
        return False

def test_unary_op_executability():
    logger.debug("Running test_unary_op_executability")
    try:
        test_unary_op_compute_func()  # Just run the test, if no exception occurs, it passes
        test_unary_op_count_func()
        logger.info("Unary operator functions are executable.")
        return True
    except Exception as e:
        logger.error(f"Error in test_unary_op_executability: {e}")
        return False

def test_binary_op_executability():
    logger.debug("Running test_binary_op_executability")
    try:
        test_binary_op_compute_func() 
        test_binary_op_count_func()
        logger.info("Binary operator functions are executable.")
        return True
    except Exception as e:
        logger.error(f"Error in test_binary_op_executability: {e}")
        return False


# st_integers_range = st.integers(min_value=-1000, max_value=1000)

# The idempotency verification (for unary operators)
@given(st.integers())
@settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_unary_idempotency(a: int):
    try:
        assert compute_func(compute_func(a)) == compute_func(a)
    except Exception as e:
        print(f"Error in {e}")
        pass

def valid_unary_idempotency():
    try:
        test_unary_idempotency() 
        return True
    except Exception as e:
        print(e)
        pass
    
# Check commutativity: a op b == b op a
@given(st.integers(), st.integers())
@settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_binary_commutativity(a: int, b:int):
    try:
        assert compute_func(a,b) == compute_func(b,a)
    except Exception as e:
        print(f"Error in {e}")
        return False

def valid_binary_commutativity():
    try:
        test_binary_commutativity() 
        return True
    except Exception as e:
        print(e)
        return False
    
# Check associativity: (a op b) op c == a op (b op c)
@given(st.integers(), st.integers(), st.integers())
@settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_binary_associativity(a: int, b: int, c: int):
    try:
        lhs = compute_func(compute_func(a, b), c)
        rhs = compute_func(a, compute_func(b, c))
        assert lhs == rhs
    except Exception as e:
        print(f"Error in {e}")
        pass

def valid_binary_associativity():
    try:
        test_binary_associativity() 
        return True
    except Exception as e:
        print(e)
        return False
    
# Check absorption law: a op (a op b) == a
@given(st.integers(), st.integers())
@settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_binary_absorption(a: int, b: int):
    try:
        assert compute_func(a, compute_func(a, b)) == a
    except Exception as e:
        print(f"Error in {e}")
        pass

def valid_binary_absorption():
    try:
        test_binary_absorption() 
        return True
    except Exception as e:
        print(e)
        return False
    
# Check idempotency: a op a == a
@given(st.integers())
@settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_binary_idempotency(a: int):
    try:
        assert compute_func(a, a) == a
    except Exception as e:
        print(f"Error in {e}")
        pass

def valid_binary_idempotency():
    try:
        test_binary_idempotency() 
        return True
    except Exception as e:
        print(e)
        return False
    
def validate_unary_property():
    """
    Validates all properties and returns a dictionary containing the validation results of all properties
    """
    validation_results = {
        "idempotency": valid_unary_idempotency(),
    }
    return validation_results

def validate_binary_property():
    """
    Validates all properties and returns a dictionary containing the validation results of all properties
    """
    validation_results = {
        "commutativity": valid_binary_commutativity(),
        "associativity": valid_binary_associativity(),
        "absorption": valid_binary_absorption(),
        "idempotency": valid_binary_idempotency(),
    }
    return validation_results


def initialize_globals(config_path: str, initial_operators_path: str):
    """
    Initializes global variables including configuration loading, 
    creation of the operator manager, and related generators.
    
    This function loads the configuration, sets up logging, initializes
    the operator manager, and generates the required generators for 
    handling operators, conditions, and expressions.
    
    Args:
        config_path (str): Path to the configuration file.
        initial_operators_path (str): Path to the initial operator definitions.
    
    Returns:
        dict: A dictionary containing the initialized objects for configuration, logging, 
              operator manager, condition generator, expression generator, operator generator, 
              parser, transformer, and operator priority manager.
    """
    # Load configuration
    global config
    config = ParamConfig(config_path)
    logging_config = config.get_logging_config()
    log = LogConfig(logging_config)
    global logger
    logger = log.get_logger()
    # Initialize Operator Manager
    op_manager = OperatorManager(initial_operators_path, config, log)

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
    
    # Parsers and transformers
    parser = OperatorDefinitionParser(config, log)
    transformer = OperatorTransformer(config, log, op_manager)
    op_priority_manager = OperatorPriorityManager(log, op_manager)
    
    # Debug logging
    logger.debug("Global variables initialized successfully.")
    
    return {
        'config': config,
        'log': log,
        'logger': logger,
        'op_manager': op_manager,
        'condition_generator': condition_generator,
        'expr_generator': expr_generator,
        'op_generator': op_generator,
        'parser': parser,
        'transformer': transformer,
        'op_priority_manager': op_priority_manager
    }

def generate_operator_type(globals_dict, operator_type, num):
    """
    Generate a specified type of operators and handle their creation, parsing, 
    transformation, and execution validation.

    This function:
    - Generates operators of the specified type.
    - Attempts to parse the operator definitions.
    - Transforms the parsed definition into executable functions.
    - Validates the syntax and executability of the generated operators.
    - Handles dependencies, calculates operator order, and saves valid operators.

    :param globals_dict: A dictionary containing all global objects including the operator manager and generators.
    :param operator_type: The type of operator to generate (e.g., 'simple_definition', 'recursive_definition').
    :param num: The number of operators to generate.
    """
    generated_count = 0
    while generated_count < num:
        # Create a new operator based on the specified type
        operator_data = globals_dict["op_generator"].create_operator_info(choice=operator_type)
        new_operator = globals_dict["op_manager"].add_operator(operator_data)

        # Update operator state to ensure it's not temporary
        new_operator.is_temporary = False
        globals_dict["logger"].debug(f"Operator Definition: {new_operator.definition}")

        if operator_type != "recursive_definition":
            try:
                # Attempt to parse the operator definition into a tree
                def_tree = globals_dict["parser"].parse_definition(new_operator.definition)
                globals_dict["logger"].debug(f"Parsed definition: {def_tree}")
            except Exception as e:
                globals_dict["logger"].error(f"Error parsing definition: {e}")
                globals_dict["op_manager"].remove_operator(new_operator.id)
                continue

            if def_tree is not None:
                try:
                    # Transform the parsed definition into compute and count functions
                    new_operator.op_compute_func, new_operator.op_count_func = globals_dict["transformer"].generate_function(new_operator.id, new_operator.n_ary, def_tree)
                    new_operator.is_temporary = True
                except Exception as e:
                    globals_dict["logger"].error(f"Error transforming the parsed definition: {e}")
                    globals_dict["op_manager"].remove_operator(new_operator.id)
                    continue

        # Get the available functions from the operator manager
        available_funcs = globals_dict["op_manager"].get_available_funcs()

        # Update global variables to ensure the correct compute and count functions are set
        global compute_func, count_func
        compute_func = new_operator.get_compute_function(available_funcs)
        count_func = new_operator.get_count_function(available_funcs)

        # First, check the syntax validity of the compute and count functions
        if test_syntax_validity(new_operator.op_compute_func, new_operator.op_count_func) == False:
            globals_dict["logger"].debug("Code for operators has syntax errors")
            continue
            
        # Validate whether the operator is executable based on its arity (1 or 2)
        if new_operator.n_ary == 1:
            is_executable = test_unary_op_executability()
        elif new_operator.n_ary == 2:
            is_executable = test_binary_op_executability()

        # Process successful operators
        if is_executable:
            new_operator.is_temporary = False
            # Record the operator's dependencies
            globals_dict["op_manager"].extract_op_dependencies(new_operator.id)
            # Calculate the operator's order (priority)
            globals_dict["op_manager"].calculate_order(new_operator.id)
            globals_dict["op_manager"].add_available_funcs(new_operator)
            
            # Validate the operator's properties
            #TODO: will be optimised to use the z3 library to find unsatisfiable a and b
            # if new_operator.n_ary == 1:
            #     new_operator.properties = validate_unary_property()
            # elif new_operator.n_ary == 2:
            #     new_operator.properties = validate_binary_property()
            
            globals_dict["logger"].debug(f"Operator {new_operator.id} is executable.")
            globals_dict["op_manager"].save_operator_to_temp(new_operator)
            globals_dict["logger"].debug(f"Operator {new_operator.id} has been successfully written to the temp file.")
            generated_count += 1
        else:
            globals_dict["op_manager"].remove_operator(new_operator.id)

def generate_randop(globals_dict: Dict[str, Any], file_path: str, num: int):
    """
    Generates random operators based on different types of definitions 
    and assigns priorities. The function will generate operators of 
    various types (simple, recursive, and branch) and then assign 
    binding, priority, and generate compute and count functions.

    The function follows these steps:
    1. Generates operators of different types (simple, recursive, 
       branch).
    2. Assigns binding and priority to the operators.
    3. Generates compute and count code for each operator.
    4. Saves the operators to a temporary file and assigns them to 
       the operator manager.

    Args:
        globals_dict (Dict[str, Any]): The global dictionary containing 
            configurations and relevant objects for operator generation.
        file_path (str): Path to the file where generated operators 
            will be saved.
        num (int): The total number of operators to generate.
    """
    
    # Get the number of base operators
    base_operators_num = globals_dict["config"].get("max_base")
    num = num - base_operators_num

    # Calculate the number of operators for each type of definition
    simple_definition_num = int(num * 0.2)  # Number of simple definitions
    # recursive_definition_num = int(num * 0.2)  # Number of recursive definitions
    branch_definition_num = int(num * 0.2)  # Number of branch definitions
    random_definition_num = num - simple_definition_num - branch_definition_num
    
    # Generate simple definitions
    globals_dict["logger"].debug(f"Generating {simple_definition_num} simple definitions.")
    generate_operator_type(globals_dict, 'simple_definition', simple_definition_num)
    
    # Generate recursive definitions
    #TODO:Problems with large numerical values
    # globals_dict["logger"].debug(f"Generating {recursive_definition_num} recursive definitions.")
    # generate_operator_type(globals_dict, 'recursive_definition', recursive_definition_num)
    
    # Generate branch definitions
    globals_dict["logger"].debug(f"Generating {branch_definition_num} branch definitions.")
    generate_operator_type(globals_dict, 'branch_definition', branch_definition_num)

    # Generate random operators (simple, recursive, or branch)
    remaining_operators = random_definition_num
    while remaining_operators > 0:
        # operator_type = random.choice(['simple_definition', 'branch_definition', 'recursive_definition'])
        operator_type = random.choice(['simple_definition', 'branch_definition'])
        globals_dict["logger"].debug(f"Generating 1 random operator of type {operator_type}.")
        generate_operator_type(globals_dict, operator_type, 1)
        remaining_operators -= 1

    # Assign priorities to all operators
    globals_dict["logger"].debug("Assigning priorities to operators.")
    globals_dict['op_priority_manager'].assign_priorities()

    # Generate and add base operators to the operator manager
    globals_dict["logger"].debug("Generating and adding base operators to the manager.")
    globals_dict["op_generator"].generate_base_operators()

    # Rename temporary operators and save them to the specified file
    globals_dict["logger"].debug(f"Renaming temporary operators and saving to {file_path}.")
    # globals_dict["op_manager"].rename_temp_to_jsonl(file_path)
    globals_dict["op_manager"].save_operators_to_jsonl(file_path)
    
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Initialize and run the operator manager with custom configuration paths.")
    parser.add_argument('--config', type=str, default='config/generate_operator.yaml', help='Path to the config file')
    parser.add_argument('--initial-operators-path', type=str, default='data/operator/initial_operators.jsonl', help='Path to the initial operator JSONL file')
    parser.add_argument('--generated-operators-path', type=str, default='data/operator/generated_operators.jsonl', help='Path where the final results should be saved')
    parser.add_argument('--num', type=int, default=100, help='Number of operators to generate')

    # Parse arguments
    args = parser.parse_args()
    
    # Print debugging information
    print("==================================================")
    print("Starting the operator generation process...")
    print(f"Config Path: {args.config}")
    print(f"Initial Operators Path: {args.initial_operators_path}")
    print(f"Generated Operators Path: {args.generated_operators_path}")
    print(f"Number of Operators to Generate: {args.num}")

    # Initialize global objects
    globals_dict = initialize_globals(config_path=args.config, initial_operators_path=args.initial_operators_path)

    # Generate the operators
    generate_randop(globals_dict, args.generated_operators_path, args.num)






