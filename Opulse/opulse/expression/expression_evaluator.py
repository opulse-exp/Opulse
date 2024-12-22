from typing import Tuple, Optional, Union, Dict
from operatorplus.operator_manager import OperatorManager
from collections import defaultdict
from expression.expression_node import (
    ExpressionNode,
    NumberNode,
    BinaryExpressionNode,
    UnaryExpressionNode,
    VariableNode,
)
from typing import cast
from operatorplus.operator_info import OperatorInfo
from expression.base_converter import BaseConverter
from config import ParamConfig, LogConfig


class ExpressionEvaluator:

    def __init__(
        self,
        param_config: ParamConfig,
        logger: LogConfig,
        operator_manager: OperatorManager,
        base_converter: BaseConverter = None,
    ):
        """
        Initializes an instance of the ExpressionEvaluator class.

        This constructor sets up the expression evaluator with necessary configurations and managers.
        It initializes attributes to manage expression trees, operators, logging, and base conversions.
        Additionally, it prepares data structures to track operator priorities, operation counts, and highest n-order values.

        Parameters:
            param_config (ParamConfig): Configuration settings for controlling the behavior of the expression evaluator.
            logger (LogConfig): Configuration for setting up logging. Used to create a logger instance for this evaluator.
            operator_manager (OperatorManager): Manager object that provides information about operators used in expressions.
            base_converter (BaseConverter, optional): Converter object for handling different numerical bases in expressions. Defaults to None.
        """
        self.param_config = param_config
        self.logger = logger.get_logger()
        # Initialization of relevant expressions to None
        self.id = None
        self.expression_tree: ExpressionNode = None
        self.expression_str: str = None
        self.operator_manager = operator_manager
        self.base_converter = base_converter
        self.all_priority = []
        self.operation_count = 0
        self.highest_n_order = 0
        # Record all operators key: op id, value: number of occurrences
        self.all_operators: Dict[int, int] = defaultdict(int)
        self.with_all_brackets = False

        # Used to replace meta words in expression strings
        self.load_atoms()

    def set_with_all_brackets(self, with_all_brackets: bool) -> None:
        """
        Sets whether to include all brackets in the expression string.

        This method configures the behavior for generating expression strings. If set to True, it ensures that all parts of the 
        expression that require parentheses for correct order of operations will be enclosed in brackets. This can be useful 
        for ensuring clarity or for specific formatting requirements.

        Parameters:
            with_all_brackets (bool): A flag indicating whether to include all necessary brackets in the expression string.
        """
        self.with_all_brackets = with_all_brackets

    def load_atoms(self) -> None:
        """
        Loads atomic symbols from the parameter configuration.
        """
        self.atoms = {
            "left_bracket": self.param_config.get("other_symbols_atoms")[
                "left_parenthesis"
            ],
            "right_bracket": self.param_config.get("other_symbols_atoms")[
                "right_parenthesis"
            ],
            "NaN": self.param_config.get("other_symbols_atoms")["nan_symbol"],
            "equal": self.param_config.get("other_symbols_atoms")["equals_sign"],
        }

    def init_expr(self, expression_tree, id, op_mode: bool = False):
        """
        Initializes expression attributes with an expression tree and ID.

        This method sets up the initial state for an expression by assigning an identifier and an expression tree.
        It also initializes counters and dictionaries that will be used to track various properties of the expression,
        such as operator priorities, operation counts, and operator occurrences. Finally, it generates string representations 
        of the expression based on the provided tree structure and optional parameters.

        Parameters:
            expression_tree (ExpressionNode): The root node of the expression tree to initialize.
            id (any): An identifier for the expression, which can be any type that uniquely identifies the expression.
            op_mode (bool, optional): A flag indicating whether the expression should be processed in operator mode. Defaults to False.
        """
        self.id = id
        self.expression_tree = expression_tree
        self.all_priority = []
        self.operation_count = 0
        self.highest_n_order = 0
        self.all_operators: Dict[int, int] = defaultdict(int)
        if op_mode:
            self.expression_str = self.tree_to_str(self.expression_tree, op_mode=True)
        else:
            self.expression_str = self.tree_to_str(self.expression_tree)
            self.expression_str_no_base_symbol = self.tree_to_str(
                self.expression_tree, with_base_symbol=False
            )

    def tree_to_str(
        self,
        node: ExpressionNode,
        parent_op: OperatorInfo = None,
        with_base_symbol: bool = True,
        op_mode: bool = False,
    ) -> str:
        """
        Converts an expression tree node to a string representation.

        This method recursively traverses the expression tree and builds a string representation based on the node type.
        For binary and unary expression nodes, it checks the operator priority relative to the parent node's operator priority
        to determine if parentheses are needed to preserve correct order of operations.
        For number and variable nodes, it returns their direct string representations.

        Parameters:
            node (ExpressionNode): The expression node to convert.
            parent_op (OperatorInfo, optional): Information about the parent operator, used to determine if parentheses are needed. Defaults to None.
            with_base_symbol (bool, optional): Whether to include base symbols in the string. Defaults to True.
            op_mode (bool, optional): A flag indicating operator mode. Defaults to False.

        Returns:
            str: String representation of the expression node.

        Raises:
            NotImplementedError: If an unsupported expression node type is encountered.
        """
        # Requires the priority of the parent node's operator for determining whether to add brackets
        if isinstance(node, NumberNode):
            node = cast(NumberNode, node)
            if op_mode:
                return f"{node.to_str_no_base_symbol(op_mode=True)}"
            else:
                if with_base_symbol:
                    return f"{node.to_str(self.operator_manager,self.base_converter)}"
                else:
                    return f"{node.to_str_no_base_symbol()}"
        elif isinstance(node, VariableNode):
            return f"{node.v}"
        elif isinstance(node, BinaryExpressionNode):
            node = cast(BinaryExpressionNode, node)
            # Statistical priority for calculating calculate_priority_hierarchical_complexity
            if (
                node.operator.priority != None
                and node.operator.priority not in self.all_priority
            ):
                self.all_priority.append(node.operator.priority)
            # Count the number of operations and associate the expression with the operator
            self.operation_count += 1
            self.all_operators[node.operator.id] += 1
            # Count the n_order info
            if self.highest_n_order < node.operator.n_order:
                self.highest_n_order = node.operator.n_order
            # Convert the expression of the subtree
            left_str = self.tree_to_str(
                node.left_expr,
                node.operator,
                with_base_symbol=with_base_symbol,
                op_mode=op_mode,
            )
            right_str = self.tree_to_str(
                node.right_expr,
                node.operator,
                with_base_symbol=with_base_symbol,
                op_mode=op_mode,
            )

            if self.with_all_brackets:
                return f"{self.atoms['left_bracket']}{left_str}{node.operator.symbol}{right_str}{self.atoms['right_bracket']}"
            # self.logger.debug(f"parent_op: {parent_op}")
            if parent_op != None and node.operator.priority < parent_op.priority:
                return f"{self.atoms['left_bracket']}{left_str}{node.operator.symbol}{right_str}{self.atoms['right_bracket']}"
            elif parent_op != None and node.operator.priority == parent_op.priority:
                # If it has the same priority as parent op, choose whether to add parentheses or not based on location and binding.
                if (
                    parent_op.associativity_direction == "left"
                    and node.position == "right"
                ):
                    return f"{self.atoms['left_bracket']}{left_str}{node.operator.symbol}{right_str}{self.atoms['right_bracket']}"
                elif (
                    parent_op.associativity_direction == "right"
                    and node.position == "left"
                ):
                    return f"{self.atoms['left_bracket']}{left_str}{node.operator.symbol}{right_str}{self.atoms['right_bracket']}"
                else:
                    return f"{left_str}{node.operator.symbol}{right_str}"
            else:
                return f"{left_str}{node.operator.symbol}{right_str}"
        elif isinstance(node, UnaryExpressionNode):
            node = cast(UnaryExpressionNode, node)
            # Statistical priority for calculating calculate_priority_hierarchical_complexity
            if (
                node.operator.priority != None
                and node.operator.priority not in self.all_priority
            ):
                self.all_priority.append(node.operator.priority)
            # Count the number of operations and associate the expression with the operator
            self.operation_count += 1
            self.all_operators[node.operator.id] += 1
            # Count the n_order info
            if self.highest_n_order < node.operator.n_order:
                self.highest_n_order = node.operator.n_order
            unary_str = self.tree_to_str(
                node.unary_expr,
                node.operator,
                with_base_symbol=with_base_symbol,
                op_mode=op_mode,
            )
            # Doubt: Always choose to add brackets to unary
            return f"({node.operator.symbol}{unary_str})"
        else:
            raise NotImplementedError("ExpressionEvaluator.tree_to_str")

    def calculate_highest_n_order(self) -> int:
        """
        Calculates the highest n-order of the expression.

        Returns: 
            (int): The highest n-order value.
        """
        return self.highest_n_order

    def calculate_priority_hierarchical_complexity(self) -> int:
        """
        Calculates the priority-based hierarchical complexity.

        Returns: 
            (int): The complexity value.
        """
        return len(self.all_priority)

    def calculate_normalized_expansion_degree(self) -> Union[int, str]:
        # Implementing the computational logic for normalized expansion degree
        """
        Calculates the normalized expansion degree of the expression.

        Returns: 
            (int): The normalized expansion degree or "NaN".
        """
        # return "NaN"
        if hasattr(self, "normalized_expansion_degree"):
            return (
                self.normalized_expansion_degree
                if self.normalized_expansion_degree != "NaN"
                else self.atoms["NaN"]
            )
        else:
            degree, result = self.calculate_normalized_expansion_degree_node(
                self.expression_tree
            )
            self.normalized_expansion_degree = degree
            self.expr_result = result
            return (
                self.normalized_expansion_degree
                if self.normalized_expansion_degree != "NaN"
                else self.atoms["NaN"]
            )

    def calculate_result(self) -> Union[int, str]:
        """
        Calculates the normalized expansion degree of the expression.

        The normalized expansion degree is a measure that represents how much an expression has been expanded or simplified.
        It can be used to evaluate the complexity of the expression in terms of its structure and size after operations.

        Returns: 
            (Union[int, str]): The normalized expansion degree or "NaN".s an integer or "NaN" if it cannot be calculated.
        """
        # return "NaN"
        if hasattr(self, "expr_result"):
            return self.expr_result if self.expr_result != "NaN" else self.atoms["NaN"]
        else:
            degree, result = self.calculate_normalized_expansion_degree_node(
                self.expression_tree
            )
            self.normalized_expansion_degree = degree
            self.expr_result = result
            return self.expr_result if self.expr_result != "NaN" else self.atoms["NaN"]

    def calculate_normalized_expansion_degree_node(
        self, node: ExpressionNode
    ) -> Tuple[Union[int, str], Union[int, str]]:
        """
        Helper method to recursively calculate the normalized expansion degree for each node in the expression tree.

        This method traverses the expression tree and computes the degree based on the type and structure of nodes.

        Args:
            node (ExpressionNode): The current node in the expression tree.
        
        Returns: 
            (Tuple[Union[int, str], Union[int, str]]): A tuple containing the normalized expansion degree and the evaluation result of the node.
        
        Raises:
            NotImplementedError: If the node type is not recognized.

        """
        # For a single expression tree node, compute the normalized expansion of the tree rooted at this node and the resultant
        if isinstance(node, NumberNode):
            return 0, node.value
        elif isinstance(node, UnaryExpressionNode):
            sub_degree, sub_result = self.calculate_normalized_expansion_degree_node(
                node.unary_expr
            )
            if sub_degree == "NaN" or sub_result == "NaN":
                return "NaN", "NaN"
            cur_result = node.operator.get_compute_function()(sub_result)
            cur_degree = node.operator.get_count_function()(sub_result)
            return cur_degree + sub_degree, cur_result
        elif isinstance(node, BinaryExpressionNode):
            # 二元操作符，分别计算左右子树的归一展开度
            left_degree, left_result = self.calculate_normalized_expansion_degree_node(
                node.left_expr
            )
            if left_degree == "NaN" or left_result == "NaN":
                return "NaN", "NaN"
            right_degree, right_result = (
                self.calculate_normalized_expansion_degree_node(node.right_expr)
            )
            if right_degree == "NaN" or right_result == "NaN":
                return "NaN", "NaN"
            cur_result = node.operator.get_compute_function()(left_result, right_result)
            cur_degree = node.operator.get_count_function()(left_result, right_result)
            if cur_degree == "NaN" or cur_result == "NaN":
                return "NaN", "NaN"
            return cur_degree + left_degree + right_degree, cur_result
        elif isinstance(node, VariableNode):
            return "NaN", "NaN"
        else:
            raise NotImplementedError(
                "ExpressionEvaluator.calculate_normalized_expansion_degree_node"
            )

    def calculate_operation_count(self):
        """
        Calculates the total number of operations in the expression.

        This method returns the count of all operations that were encountered during the construction of the expression tree.

        Returns: 
            (int): The operation count as an integer.
        """
        # 实现运算次数的计算逻辑
        return self.operation_count

    def calculate_complexity_ratio(self):
        """
        Calculates the complexity ratio based on normalized expansion degree and operation count.

        The complexity ratio provides a measure of how complex the expression is relative to the number of operations it contains.
        It is calculated by dividing the normalized expansion degree by the operation count.

        Returns: 
            (int): The complexity ratio as a floating-point number. Returns 0 if the operation count is 0 or the expansion degree is "NaN".
        """
        operation_count = self.calculate_operation_count()
        normalized_expansion_degree = self.calculate_normalized_expansion_degree()
        return (
            normalized_expansion_degree / operation_count
            if operation_count > 0 and normalized_expansion_degree != "NaN"
            else 0
        )

    def calculate_max_digit_count(self):
        """
        Calculates the maximum digit count in the expression string.

        This method extracts all numbers from the expression string, converts them to integers, and determines the length of the largest number.

        Returns: 
            (int): The maximum digit count as an integer. Returns 0 if there are no digits in the expression string.
        """
        numbers = [int(num) for num in self.expression_str.split() if num.isdigit()]
        return max((len(str(num)) for num in numbers), default=0)

    def evaluate(self):
        """
        Evaluates the expression and returns its properties.

        This method aggregates various metrics about the expression, such as its highest n-order, hierarchical complexity,
        normalized expansion degree, operation count, complexity ratio, maximum digit count, and result.

        Returns: 
            (dict): A dictionary containing various properties of the evaluated expression.
        """
        return {
            "id": self.id,
            "expression_no_base_symbol": self.expression_str_no_base_symbol,
            "expression": self.expression_str,
            "highest_n_order": self.calculate_highest_n_order(),
            "priority_hierarchical_complexity": self.calculate_priority_hierarchical_complexity(),
            "normalized_expansion_degree": self.calculate_normalized_expansion_degree(),
            "operation_count": self.calculate_operation_count(),
            "complexity_ratio": self.calculate_complexity_ratio(),
            "max_digit_count": self.calculate_max_digit_count(),
            "tree": self.expression_tree.to_dict(),
            "used_operators": list(self.all_operators.keys()),
            "result": self.calculate_result(),
        }


# if __name__ == "__main__":
#     # 示例使用
#     from expression.expression_generator import ExpressionGenerator
#     from operatorplus.operator_manager import OperatorManager

#     manager = OperatorManager("data/operator/available_operators.jsonl")
#     expr_generator = ExpressionGenerator("data/operator/available_operators.jsonl")
#     rand_expr_tree = expr_generator.create_expression()
#     # expression = "(3 ⊗ (2 ⊕ 5) ⊖ (4 ⊘ 2)) ⊕ 9"
#     evaluator = ExpressionEvaluator()
#     properties = evaluator.evaluate()
