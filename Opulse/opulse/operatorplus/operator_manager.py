from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, deque
from operatorplus.operator_info import OperatorInfo
from config import LogConfig, ParamConfig
import json
from lark.tree import Tree
import re
import os

class OperatorManager:
    def __init__(
        self, 
        config_file: str,
        param_config: ParamConfig,
        logger: LogConfig
    ):
        self.config_file = config_file
        self.param_config = param_config
        self.logger = logger.get_logger()
        self.operators: Dict[int, OperatorInfo] = (
            {}
        )  # key: operator id, value: OperatorInfo
        self.symbol_to_operators: Dict[str, List[OperatorInfo]] = defaultdict(
            list
        )  # key: operator symbol, value: list of OperatorInfo
        self.base_operators: Dict[int, List[OperatorInfo]] = defaultdict(list)
        # key: is_base, value: list of OperatorInfo

        self.available_funcs: Dict[str, Any] = {}  # to store available functions
        self.load_operators()
        self.temp_file_path = "data/operator/temp_operators.temp"  # Temporary file path

    def load_operators(self):
        """
        Loads operator definitions from a JSONL file.

        This method reads the configuration file line by line, parses each line into an
        `OperatorInfo` object, and stores the operators in various structures:
        - `self.operators`: A dictionary with operator ID as the key and `OperatorInfo` as the value.
        - `self.symbol_to_operators`: A dictionary with operator symbol as the key and a list of `OperatorInfo` as the value.
        - `self.base_operators`: A dictionary to store base operators based on their base status.
        
        Additionally, it updates the available functions for computation and counting based on the loaded operators.

        Logs relevant information about the loading process for monitoring and debugging purposes.
        """
        self.logger.info(f"Loading operators from configuration file: {self.config_file}")
        
        with open(self.config_file, "r", encoding="utf-8") as f:
            line_count = 0
            for line in f:
                line_count += 1
                if not line.strip():
                    self.logger.debug(f"Skipping empty line {line_count}.")
                    continue  # Skip empty lines
                try:
                    operator = OperatorInfo.from_json(line)
                    self.operators[operator.id] = operator
                    self.symbol_to_operators[operator.symbol].append(operator)
                    
                    # Update available functions for the operator
                    if operator.is_base:
                        self.base_operators[operator.is_base].append(operator)
                    
                    self._update_available_funcs(operator)
                    self.logger.debug(f"Loaded operator {operator.id} ({operator.symbol}) from line {line_count}.")
                
                except Exception as e:
                    self.logger.warning(f"Failed to parse operator from line {line_count}: {e}")
        
        self.logger.info(f"Successfully loaded {len(self.operators)} operators from the configuration file.")
    
    def save_operators_to_jsonl(self, file_path: str):
        """
        Saves all operators to a JSONL file.

        This method serializes each operator in `self.operators` and writes it to the specified file path in JSONL format.
        
        Args:
            file_path (str): The path to the file where the operators should be saved.

        Logs the process of saving operators to the file.
        """
        self.logger.info(f"Saving operators to {file_path}.")
        
        with open(file_path, "w", encoding="utf-8") as file:
            for operator in self.operators.values():
                json_line = operator.to_json()
                file.write(json_line + "\n")
                self.logger.debug(f"Saved operator {operator.id} ({operator.symbol}) to {file_path}.")
        
        self.logger.info(f"Successfully saved all operators to {file_path}.")

    def save_operator_to_temp(self, operator):
        """
        Saves a single operator to a temporary file.

        This method serializes the given operator and appends it to a temporary file defined in `self.temp_file_path`.

        Args:
            operator (OperatorInfo): The operator to be saved.

        Logs the process of saving the operator to the temporary file.
        """
        self.logger.info(f"Saving operator {operator.id} ({operator.symbol}) to temporary file.")
        
        with open(self.temp_file_path, 'a', encoding="utf-8") as temp_file:
            json_line = operator.to_json()
            temp_file.write(json_line + "\n")
            self.logger.debug(f"Operator {operator.id} ({operator.symbol}) saved to temporary file.")

    def clear_temp_file(self):
        """
        Clears the temporary file by removing it if it exists.

        This method checks if the temporary file exists and removes it. If the file doesn't exist, a warning is logged.
        In case of any error during file removal, an error log is generated.

        Logs the status of the file clearance operation.
        """
        try:
            if os.path.exists(self.temp_file_path):
                os.remove(self.temp_file_path)
                self.logger.info(f"Temporary file {self.temp_file_path} cleared.")
            else:
                self.logger.warning(f"Temporary file {self.temp_file_path} does not exist.")
        except Exception as e:
            self.logger.error(f"Error clearing temporary file: {e}")
    
    def rename_temp_to_jsonl(self, file_path: str):
        """Renames the temporary file to the specified file_path."""
        # Ensure the temporary file exists at self.temp_file_path
        if os.path.exists(self.temp_file_path):
            # If the destination file doesn't exist, create it
            if not os.path.exists(file_path):
                # Create an empty file at the destination path
                open(file_path, 'w', encoding="utf-8").close()

            try:
                # Now, rename the temporary file to the specified file_path
                os.rename(self.temp_file_path, file_path)
                self.logger.info(f"Renamed temporary file {self.temp_file_path} to {file_path}")
            except OSError as e:
                self.logger.error(f"Error renaming file {self.temp_file_path} to {file_path}: {e}")
        else:
            self.logger.warning(f"Temporary file not found: {self.temp_file_path}")
       
    def _update_available_funcs(self, operator: OperatorInfo):
        """
        Update available_funcs with the compute and count functions of the given operator.
        """
        if operator.op_compute_func:
            self.available_funcs[f"op_{operator.id}"] = operator.get_compute_function(
                self.available_funcs
            )
        if operator.op_count_func:
            self.available_funcs[f"op_count_{operator.id}"] = (
                operator.get_count_function(self.available_funcs)
            )

    def get_available_funcs(self) -> Dict[str, Any]:
        """
        Returns the available functions (compute and count functions).
        """
        return self.available_funcs

    def add_available_funcs(self, operator: OperatorInfo):
        """
        Updates the available functions whenever a new operator is added.
        """
        self._update_available_funcs(operator)

    def get_next_operator_id(self) -> int:
        """
        Retrieves the next available operator ID.

        This method checks if there are existing operators, and if so, returns the next ID based on the 
        current maximum operator ID. If there are no operators, it starts from ID 1.

        Returns:
            int: The next available operator ID.
        """
        self.logger.debug("Getting the next available operator ID.")
        
        if not self.operators:
            self.logger.debug("No operators found, starting from ID 1.")
            return 1

        # Get the current maximum operator ID
        max_id = max(self.operators.keys())
        
        # Return the next ID
        self.logger.debug(f"Current maximum operator ID is {max_id}. Returning next ID: {max_id + 1}.")
        return max_id + 1

    def get_operator_by_id(self, op_id: int) -> OperatorInfo:
        """
        Retrieves an operator by its ID.

        Args:
            op_id (int): The operator ID.

        Returns:
            OperatorInfo: The operator corresponding to the given ID.

        Raises:
            ValueError: If the operator ID does not exist.
        """
        self.logger.debug(f"Fetching operator with ID {op_id}.")
        
        if op_id not in self.operators:
            self.logger.error(f"Operator ID {op_id} does not exist.")
            raise ValueError(f"Operator ID {op_id} does not exist.")
        
        self.logger.debug(f"Operator ID {op_id} found.")
        return self.operators[op_id]

    def get_operators_by_symbol(self, symbol: str) -> List[OperatorInfo]:
        """
        Retrieves all operators corresponding to a given symbol.

        Args:
            symbol (str): The operator symbol.

        Returns:
            List[OperatorInfo]: A list of operators corresponding to the symbol.
        """
        self.logger.debug(f"Fetching operators with symbol '{symbol}'.")
        
        operators = self.symbol_to_operators.get(symbol, [])
        
        self.logger.debug(f"Found {len(operators)} operators for symbol '{symbol}'.")
        return operators

    def get_operator_symbols(self) -> List[str]:
        """
        Retrieves a list of all operator symbols.

        Returns:
            List[str]: A list of operator symbols.
        """
        self.logger.debug("Fetching all operator symbols.")
        
        symbols = list(self.symbol_to_operators.keys())
        
        self.logger.debug(f"Found {len(symbols)} operator symbols.")
        return symbols

    def get_operator_function_id(
        self, operator_symbol: str, is_unary: bool
    ) -> Optional[tuple[int, bool]]:
        """
        Retrieves the function ID and temporary status of an operator based on its symbol and type (unary or binary).

        Args:
            operator_symbol (str): The operator symbol.
            is_unary (bool): A boolean indicating whether the operator is unary (True) or binary (False).

        Returns:
            Optional[tuple[int, bool]]: A tuple containing the operator's function ID and its temporary status.
                                        If no matching operator is found, returns (None, False).
        """
        self.logger.debug(f"Fetching function ID for operator symbol '{operator_symbol}' and type {'unary' if is_unary else 'binary'}.")
        
        for operator in self.symbol_to_operators.get(operator_symbol, []):
            if (is_unary and operator.n_ary == 1) or (not is_unary and operator.n_ary == 2):
                self.logger.debug(f"Found operator {operator.id} ({operator.symbol}) matching the criteria.")
                return operator.id, operator.is_temporary

        self.logger.debug(f"No matching operator found for symbol '{operator_symbol}' and type {'unary' if is_unary else 'binary'}.")
        return None, False

    def get_operator_by_base(self, base: int) -> OperatorInfo:
        """
        Retrieves an operator based on the given base (number system).

        Args:
            base (int): The base (e.g., 2 for binary, 10 for decimal, etc.).

        Returns:
            OperatorInfo: The operator corresponding to the given base.

        Raises:
            ValueError: If no operators are available for the given base.
        """
        self.logger.debug(f"Fetching operator for base {base}.")
        
        if base not in self.base_operators:
            self.logger.error(f"Base type {base} does not exist.")
            raise ValueError(f"Base type {base} does not exist.")
        
        self.logger.debug(f"Found operator(s) for base {base}.")
        return self.base_operators[base]

    def get_unary_and_binary_operators(
        self,
    ) -> Tuple[List[OperatorInfo], List[OperatorInfo], List[OperatorInfo]]:
        """
        Retrieves the lists of unary prefix operators, unary postfix operators, and binary operators.

        This method categorizes the operators into three types:
        - Unary prefix operators: Operators that appear before their operands.
        - Unary postfix operators: Operators that appear after their operands.
        - Binary operators: Operators that take two operands.

        Returns:
            Tuple[List[OperatorInfo], List[OperatorInfo], List[OperatorInfo]]:
            A tuple containing three lists:
            1. List of unary prefix operators
            2. List of unary postfix operators
            3. List of binary operators
        """
        self.logger.debug("Fetching unary and binary operators.")

        # Get unary prefix operators
        unary_prefix_ops = [
            op
            for op in self.operators.values()
            if op.n_ary == 1 and op.unary_position == "prefix"
        ]
        
        self.logger.debug(f"Found {len(unary_prefix_ops)} unary prefix operators.")
        
        # Get unary postfix operators
        unary_postfix_ops = [
            op
            for op in self.operators.values()
            if op.n_ary == 1 and op.unary_position == "postfix"
        ]
        
        self.logger.debug(f"Found {len(unary_postfix_ops)} unary postfix operators.")
        
        # Get binary operators
        binary_ops = [op for op in self.operators.values() if op.n_ary == 2]

        self.logger.debug(f"Found {len(binary_ops)} binary operators.")
        
        return unary_prefix_ops, unary_postfix_ops, binary_ops

    def get_operators_by_priority(self) -> List[OperatorInfo]:
        """
        Sorts and returns operators based on their priority.

        This method sorts all operators by their priority, where operators with lower priority come first.

        Returns:
            List[OperatorInfo]: A list of operators sorted by priority.
        """
        self.logger.debug("Sorting operators by priority.")
        
        # Sort operators by priority in ascending order (lower priority first)
        sorted_operators = sorted(
            self.operators.values(), key=lambda op: op.priority, reverse=False
        )
        
        self.logger.debug(f"Sorted {len(sorted_operators)} operators by priority.")
        
        return sorted_operators
    
    def extract_op_dependencies(self, op_id: int):
        """
        Extracts dependencies of a given operator by analyzing its compute function.

        This method uses a regular expression to match operator IDs in the `op_compute_func` 
        field of the operator and identifies any dependencies (operators that the current 
        operator relies on).

        Parameters:
            op_id (int): The ID of the operator whose dependencies need to be extracted.
        
        Updates:
            - The `dependencies` attribute of the operator is updated to a list of dependent operator IDs.
        """
        self.logger.debug(f"Extracting dependencies for operator ID {op_id}.")

        # Get the operator by ID
        operator = self.get_operator_by_id(op_id)

        # Regular expression pattern to match operator dependencies (e.g., op_1, op_2, etc.)
        op_pattern = r"op_(\d+)"

        # Use re.findall to extract all matching operator IDs from the function
        op_numbers = re.findall(op_pattern, operator.op_compute_func)

        # Convert matched strings to integers and remove duplicates
        op_numbers = list(set(map(int, op_numbers)))

        # If the operator itself is in the list of dependencies, remove it
        if op_id in op_numbers:
            op_numbers.remove(op_id)

        # Update operator dependencies
        operator.dependencies = op_numbers
        self.logger.info(f"Operator {op_id} dependencies updated to: {op_numbers}.")
        
    def calculate_order(self, operator_id: int):
        """
        Calculates the order (n_order) of a specific operator based on its dependencies.

        The order of an operator is determined by its dependencies' orders:
        - For recursive definitions: max order of dependencies + 1.
        - For non-recursive definitions: max order of dependencies.

        If no dependencies exist, the order is set to 1.

        Parameters:
            operator_id (int): The ID of the operator whose order is to be calculated.
        """
        self.logger.debug(f"Calculating order for operator ID {operator_id}.")

        # Retrieve the operator's information using the provided operator ID
        operator_info = self.operators.get(operator_id)

        if not operator_info:
            self.logger.error(f"Operator with ID {operator_id} not found.")
            return

        # If the operator has dependencies, calculate its order based on them
        if operator_info.dependencies:
            # Get the n_order values of all dependencies
            dependency_orders = [
                self.operators[dep_id].n_order for dep_id in operator_info.dependencies
            ]
            self.logger.debug(f"Dependency orders for operator {operator_id}: {dependency_orders}.")

            if operator_info.definition_type == "recursive_definition":
                # For recursive definitions, the order is the max order of dependencies + 1
                operator_info.n_order = max(dependency_orders) + 1
                self.logger.debug(f"Operator {operator_id} is recursive; setting n_order to {operator_info.n_order}.")
            else:
                # For non-recursive definitions, the order is the max order of dependencies
                operator_info.n_order = max(dependency_orders)
                self.logger.debug(f"Operator {operator_id} is non-recursive; setting n_order to {operator_info.n_order}.")
        else:
            # If the operator has no dependencies, set its order to 1
            operator_info.n_order = 1
            self.logger.debug(f"Operator {operator_id} has no dependencies; setting n_order to 1.")

        # Log the final n_order value for the operator
        self.logger.info(f"Operator {operator_info.symbol} (ID: {operator_id}) has n_order: {operator_info.n_order}.")

    def update_operator_temporary_status(self, operator_id: int, new_status: bool) -> bool:
        """
        Updates the 'is_temporary' status of the specified operator.

        This function looks for an operator by its ID and sets its 'is_temporary' status
        to the provided new status.

        Parameters:
            operator_id (int): The ID of the operator to update.
            new_status (bool): The new 'is_temporary' status to set for the operator.

        Returns:
            bool: Returns True if the update was successful, otherwise returns False if the operator was not found.
        """
        self.logger.debug(f"Attempting to update 'is_temporary' status for operator ID {operator_id} to {new_status}.")

        # Loop through all operators to find the one with the specified ID
        for operators in self.symbol_to_operators.values():
            for operator in operators:
                if operator.id == operator_id:
                    # Found the operator, updating its is_temporary status
                    operator.is_temporary = new_status
                    self.logger.info(f"Operator {operator_id}: 'is_temporary' status successfully updated to {new_status}.")
                    return True  # Update successful
        
        # If the operator ID was not found, log an error and return False
        self.logger.error(f"Operator with ID {operator_id} not found. Update failed.")
        return False  # Operator not found

    def add_operator(self, operator_data: Dict[str, Any]):
        """
        Dynamically adds a new operator to the system.

        This method assigns a new operator ID (if not provided), ensures that 
        the operator's `n_order` is set to `None` for later processing, and 
        adds the operator to the internal storage.

        Parameters:
            operator_data (Dict[str, Any]): A dictionary containing the operator's details, 
                                             such as 'symbol', 'id', and other relevant properties.

        Returns:
            OperatorInfo: The newly created operator object.
        """
        self.logger.debug("Attempting to add a new operator with data: %s", operator_data)

        # Automatically assign an ID if not provided
        if "id" not in operator_data or operator_data["id"] is None:
            new_id = max(self.operators.keys(), default=0) + 1
            operator_data["id"] = new_id
            self.logger.info(f"Automatically assigned operator ID: {new_id}")
        else:
            new_id = operator_data["id"]
            if new_id in self.operators:
                self.logger.error(f"Operator ID {new_id} already exists.")
                raise ValueError(f"Operator ID {new_id} already exists.")

        # Ensure that n_order is set to None for later processing by calculate_order
        operator_data["n_order"] = None  # Let calculate_order handle this

        # Create the new operator
        new_operator = OperatorInfo(**operator_data)

        # Add the operator to the operators dictionary
        self.operators[new_operator.id] = new_operator

        # Map the operator to its symbol in the symbol_to_operators dictionary
        if new_operator.symbol not in self.symbol_to_operators:
            self.symbol_to_operators[new_operator.symbol] = []
        self.symbol_to_operators[new_operator.symbol].append(new_operator)
        self.logger.debug(f"Operator {new_operator.symbol} (ID: {new_operator.id}) added to symbol_to_operators.")

        # Add the operator to the base_operators dictionary based on its base type
        if new_operator.is_base is not None:
            if new_operator.is_base not in self.base_operators:
                self.base_operators[new_operator.is_base] = []
            self.base_operators[new_operator.is_base].append(new_operator)
            self.logger.debug(f"Operator {new_operator.symbol} (ID: {new_operator.id}) added to base_operators.")

        return new_operator

    def remove_operator(self, op_id: int):
        """
        Dynamically removes an operator from the system.

        This method removes an operator by its ID, updating the internal storage 
        (both `self.operators` and `self.symbol_to_operators`) accordingly. 

        Parameters:
            op_id (int): The ID of the operator to be removed.

        Raises:
            ValueError: If the operator ID does not exist in the system.
        """
        self.logger.debug("Attempting to remove operator with ID: %d", op_id)

        if op_id not in self.operators:
            self.logger.error(f"Operator ID {op_id} does not exist.")
            raise ValueError(f"Operator ID {op_id} does not exist.")

        # Retrieve and remove the operator from the operators dictionary
        operator = self.operators.pop(op_id)
        self.available_funcs.pop(f"op_{operator.id}", None)
        self.available_funcs.pop(f"op_count_{operator.id}", None)
        self.logger.info(f"Removed operator {operator.symbol} (ID: {op_id}).")

        # Remove the operator from the symbol_to_operators mapping
        if operator.symbol in self.symbol_to_operators:
            self.symbol_to_operators[operator.symbol].remove(operator)
            self.logger.debug(f"Operator {operator.symbol} (ID: {op_id}) removed from symbol_to_operators.")
            
    def update_operator(self, op_id: int, updated_data: Dict[str, Any]):
        """
        Dynamically updates an existing operator in the system.

        This method replaces the operator with the given ID (`op_id`) using the data 
        in `updated_data`. It performs the necessary checks and ensures that all required fields 
        are provided before updating the operator in the internal storage.

        Parameters:
            op_id (int): The ID of the operator to be updated.
            updated_data (dict): A dictionary containing the updated data for the operator.

        Raises:
            ValueError: If the operator ID does not exist or required fields are missing.
        """
        self.logger.debug("Attempting to update operator with ID: %d", op_id)

        # Check if the operator exists
        if op_id not in self.operators:
            self.logger.error(f"Operator ID {op_id} does not exist.")
            raise ValueError(f"Operator ID {op_id} does not exist.")

        # Ensure the 'id' in updated_data matches the op_id
        updated_data["id"] = op_id

        # Ensure 'compute_func' is provided in the updated data
        if "compute_func" not in updated_data or not updated_data["compute_func"]:
            self.logger.error("compute_func must be provided.")
            raise ValueError("compute_func must be provided.")

        # Set 'n_order' to None, letting calculate_order handle it later
        updated_data["n_order"] = None

        # Remove the old operator
        old_operator = self.operators.pop(op_id)
        self.symbol_to_operators[old_operator.symbol].remove(old_operator)
        self.logger.info(f"Removed old operator {old_operator.symbol} (ID: {op_id}).")

        # Add the updated operator
        updated_operator = OperatorInfo(**updated_data)
        self.operators[updated_operator.id] = updated_operator
        self.symbol_to_operators[updated_operator.symbol].append(updated_operator)
        self.logger.info(f"Updated operator {updated_operator.symbol} (ID: {op_id}).")

        # Recalculate order after the update
        self.calculate_order()
        self.logger.debug(f"Recalculated order for operator ID: {op_id}.")

    def delete_one_operator(self, op_id: int) -> None:
        """
        Delete an operator and recursively remove dependent operators. 
        Afterward, reassign IDs for the remaining operators.

        Parameters:
            op_id (int): The ID of the operator to be deleted.
        """
        self.logger.debug("Attempting to delete operator with ID: %d", op_id)

        # Recursively delete the operator and its dependencies
        self.delete_one_operator_by_dep(op_id)

        # Reassign operator IDs after deletion
        sorted_keys = sorted(self.operators.keys())
        op_pattern = r"def op_(\d+)"
        op_count_pattern = r"def op_count_(\d+)"

        for i, old_key in enumerate(sorted_keys, start=1):
            if old_key != i:
                self.operators[i] = self.operators[old_key]
                # Update the ID of the operator
                self.operators[i].id = i
                # Update the operator's function string
                self.operators[i].op_compute_func = re.sub(
                    op_pattern,
                    lambda m: f"op_{i}",
                    self.operators[i].op_compute_func,
                    count=1,
                )
                self.operators[i].op_count_func = re.sub(
                    op_count_pattern,
                    lambda m: f"op_count_{i}",
                    self.operators[i].op_count_func,
                    count=1,
                )
                for operator in self.operators.values():
                    if old_key in operator.dependencies:
                        # Replace old_key with i in dependencies
                        operator.dependencies = [i if dep == old_key else dep for dep in operator.dependencies]
                        # Also, update the operator's compute functions to reflect the new op_id
                        operator.op_compute_func = re.sub(
                            rf"op_{old_key}",
                            lambda m: f"op_{i}",
                            operator.op_compute_func
                        )
                        operator.op_count_func = re.sub(
                            rf"op_count_{old_key}",
                            lambda m: f"op_count_{i}",
                            operator.op_count_func
                        )
                del self.operators[old_key]

        self.logger.info("Operator with ID %d and its dependencies removed. Operator IDs reassigned.", op_id)

    def delete_one_operator_by_dep(self, op_id: int) -> None:
        """
        Recursively delete an operator and its dependencies.
        
        Parameters:
            op_id (int): The ID of the operator to be deleted.
        
        Raises:
            ValueError: If the operator with the given ID does not exist.
        """
        self.logger.debug("Attempting to recursively delete operator with ID: %d", op_id)

        # Check if the operator exists
        if op_id not in self.operators:
            self.logger.error(f"Operator ID {op_id} does not exist.")
            raise ValueError(f"Operator ID {op_id} does not exist.")
        
        # Set to keep track of operators that need to be deleted
        to_delete_ids = set()

        # Recursively find all operators that depend on the given operator
        self._find_all_dependent_operator_ids(op_id, to_delete_ids)

        # Remove the operators
        for op_id_to_delete in to_delete_ids:
            self.remove_operator(op_id_to_delete)

        self.logger.debug("Completed recursive deletion for operator ID: %d and its dependencies.", op_id)

    def _find_all_dependent_operator_ids(self, op_id: int, to_delete_ids: set) -> None:
        """
        Helper function to recursively find all dependent operators that should be deleted.
        
        Parameters:
            op_id (int): The ID of the operator whose dependencies should be found.
            to_delete_ids (set): A set that stores all operator IDs that should be deleted.
        """
        # If this operator has already been marked for deletion, return early
        if op_id in to_delete_ids:
            return
        
        # Mark this operator for deletion
        to_delete_ids.add(op_id)

        # Recursively find operators that depend on the current operator
        for operator in self.operators.values():
            if op_id in operator.dependencies:
                self._find_all_dependent_operator_ids(operator.id, to_delete_ids)




