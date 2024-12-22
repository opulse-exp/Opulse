import json
from typing import List, Dict, Optional, Any

class OperatorInfo:
    def __init__(
        self,
        id: int,
        symbol: str,
        n_ary: int,  # 1 for unary, 2 for binary
        unary_position: Optional[str],  # 'prefix', 'postfix', or None
        is_base: Optional[int],  # Used to identify the base type, e.g., 2 for binary, 10 for decimal, 16 for hexadecimal
        definition: Optional[str],
        definition_type: Optional[str],  # Types: simple_definition, recursive_definition, branch_definition
        priority: int,  # Priority for operations with the same level, higher values represent higher priority
        associativity_direction: Optional[str],  # 'left', 'right', or None
        n_order: int,  # Order, used to measure complexity, particularly for recursive definitions
        op_compute_func: Optional[
            str
        ],  # Function code for the operator, e.g., "def op_11(a, b): ..."
        op_count_func: Optional[str],  # Function code to calculate the count, e.g., base = 0
        z3_compute_func: Optional[str] = None, ##TODO:Still in the process of realising, Used for constraint solving
        properties: Optional[Dict[str, bool]] = None,  # Other properties such as "commutative", "associative", "idempotent", etc.
        dependencies: Optional[List[int]] = None,  # Record dependencies on other operators
        is_temporary: bool = False,  # Whether the operator is temporary (for incomplete information)
        recursive_used_cases: int = 0b00000000,  # Record used recursive cases
        is_recursion_enabled: bool = True  # Whether recursion can still be enabled based on the recursive type
    ):
        """
        Initializes the OperatorInfo object with various parameters describing the operator's properties.

        Args:
            id (int): Unique identifier for the operator.
            symbol (str): Symbol representing the operator.
            n_ary (int): Arity of the operator, either 1 for unary or 2 for binary.
            unary_position (Optional[str]): Position for unary operators ('prefix', 'postfix', or None).
            is_base (Optional[int]): Base type identifier (e.g., 2 for binary, 10 for decimal).
            definition (Optional[str]): Definition of the operator (could be a string representation of the definition).
            definition_type (Optional[str]): Type of definition ('simple_definition', 'recursive_definition', or 'branch_definition').
            priority (int): Priority of the operator, higher means higher priority.
            associativity_direction (Optional[str]): Direction of associativity ('left', 'right', or None).
            n_order (int): Order to measure complexity, especially for recursive operators.
            op_compute_func (Optional[str]): Code string for computing the operator's result.
            op_count_func (Optional[str]): Code string for counting the operations.
            properties (Optional[Dict[str, bool]]): Additional properties of the operator (commutative, associative, etc.).
            dependencies (Optional[List[int]]): List of dependencies on other operators.
            is_temporary (bool): Whether the operator is temporary, typically used when its information is incomplete.
            recursive_used_cases (int): Record of the recursive cases used.
            is_recursion_enabled (bool): Whether recursion is still allowed for this operator.
        """
        self.id = id
        self.symbol = symbol
        self.n_ary = n_ary
        self.unary_position = unary_position
        self.is_base = is_base
        self.definition = definition
        self.definition_type = definition_type
        self.priority = priority
        self.associativity_direction = associativity_direction
        self.n_order = n_order
        self.op_compute_func = op_compute_func
        self.op_count_func = op_count_func
        self.z3_compute_func = z3_compute_func
        self.properties = properties
        self.dependencies = dependencies
        self.is_temporary = is_temporary
        self.recursive_used_cases = recursive_used_cases
        self.is_recursion_enabled = is_recursion_enabled
        self.compiled_functions = {}  # Cache compiled functions to avoid recompiling

    def __repr__(self):
        """
        Provides a string representation of the operator information object.
        
        Returns:
            str: A string representation of the OperatorInfo object.
        """
        return (
            f"OperatorInfo(id={self.id}, symbol='{self.symbol}', n_ary={self.n_ary}, "
            f"unary_position={self.unary_position!r}, is_base={self.is_base}, "
            f"definition={self.definition!r}, definition_type={self.definition_type!r}, "
            f"priority={self.priority}, "
            f"associativity_direction={self.associativity_direction!r}, n_order={self.n_order}, "
            f"op_compute_func={self.op_compute_func!r}, op_count_func={self.op_count_func!r}, "
            # f"properties={self.properties!r}, "
            f"dependencies={self.dependencies!r}, "
            f"compiled_functions={'{}' if not self.compiled_functions else f'{{...}}'})"
        )

    def to_json(self) -> str:
        """
        Converts the operator information object to a JSON string, excluding temporary and compiled function data.
        
        Returns:
            str: A JSON string representing the OperatorInfo object.
        """
        serializable_dict = self.__dict__.copy()
        # Remove attributes that should not be serialized
        for key in ['properties','is_temporary', 'recursive_used_cases', 'is_recursion_enabled', 'compiled_functions']:
            serializable_dict.pop(key, None)
        return json.dumps(serializable_dict, ensure_ascii=False)

    @staticmethod
    def from_json(json_str: str) -> "OperatorInfo":
        """
        Creates an OperatorInfo object from a JSON string.
        
        Args:
            json_str (str): A JSON string representing an OperatorInfo object.
        
        Returns:
            OperatorInfo: An instance of the OperatorInfo class initialized from the JSON data.
        """
        data = json.loads(json_str)
        return OperatorInfo(**data)

    def get_compute_function(
        self, available_funcs: Dict[str, Any] = None
    ) -> Optional[Any]:
        """
        Retrieves the compute function for the operator, compiling it if necessary, and handling dependencies.
        
        Args:
            available_funcs (Dict[str, Any], optional): A dictionary of available functions that can be used by the operator's function.
        
        Returns:
            Optional[Any]: The compiled function object or None if it cannot be compiled.
        """
        available_funcs = available_funcs or {}
        return self._compile_function(
            self.op_compute_func, f"op_{self.id}", available_funcs
        )

    def get_count_function(
        self, available_funcs: Dict[str, Any] = None
    ) -> Optional[Any]:
        """
        Retrieves the count function for the operator, compiling it if necessary, and handling dependencies.
        
        Args:
            available_funcs (Dict[str, Any], optional): A dictionary of available functions that can be used by the operator's function.
        
        Returns:
            Optional[Any]: The compiled function object or None if it cannot be compiled.
        """
        available_funcs = available_funcs or {}
        return self._compile_function(
            self.op_count_func, f"op_count_{self.id}", available_funcs
        )

    def _compile_function(
        self, func_code: Optional[str], func_name: str, available_funcs: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Compiles a given function code string into an executable function object, caching it for future use.
        
        Args:
            func_code (Optional[str]): The code for the function to be compiled.
            func_name (str): The name of the function being compiled.
            available_funcs (Dict[str, Any]): A dictionary of functions available in the current context.
        
        Returns:
            Optional[Any]: The compiled function object, or None if compilation fails.
        """
        if not func_code:
            return None
        if func_name in self.compiled_functions:
            return self.compiled_functions[func_name]

        try:
            # Create a local namespace and add available functions
            local_namespace = {}
            local_namespace.update(available_funcs)

            # Execute the function code in the local namespace to compile the function
            exec(func_code, local_namespace, local_namespace)
            compiled_func = local_namespace.get(func_name, None)
            self.compiled_functions[func_name] = compiled_func  # Cache the compiled function
            return compiled_func
        except Exception as e:
            print(f"Error compiling function '{func_name}' for operator '{self.symbol}': {e}")
            return None
