import random
from typing import Dict, Any, List
from expression.expression_evaluator import ExpressionEvaluator
from operatorplus.operator_manager import OperatorManager
from operatorplus.operator_info import OperatorInfo
import json
from collections import defaultdict
from expression.expression_node import (
    ExpressionNode,
    NumberNode,
    BinaryExpressionNode,
    UnaryExpressionNode,
    VariableNode,
)
import time
from expression.base_converter import BaseConverter
from config import LogConfig, ParamConfig


class ExpressionGenerator:

    def __init__(
        self,
        param_config: ParamConfig,
        logger: LogConfig,
        operator_manager: OperatorManager,
        # variables: List[str] = None,
        # min_value: int = 0,
        # max_value: int = 100,
        # max_depth: int = 3,
        # expr_type_weights: Dict[str, float] = None,
        # atoms_type_weights: Dict[str, float] = None,
    ):
        """
        Initializes the ExpressionGenerator with configuration parameters and dependencies.

        Args:
            param_config (ParamConfig): Configuration parameters for expression generation.
            logger (LogConfig): Logging configuration to record events and errors.
            operator_manager (OperatorManager): Manager for handling operators used in expressions.
        """
        self.param_config = param_config
        self.logger = logger.get_logger()
        self.variables = self.param_config.get("expr_variables")
        self.max_value = self.param_config.get("expr_numeric_range")["max_value"]
        self.min_value = self.param_config.get("expr_numeric_range")["min_value"]
        # 表达式树的最大深度 防止递归超过最大深度
        self.max_depth = self.param_config.get("expr_max_depth")
        # 设置表达式类型的概率分布，若未传入则使用默认值
        self.expr_type_weights = self.param_config.get("expr_type_weights")
        # {
        #     "binary": 0.7,
        #     "unary_prefix": 0.2,
        #     "unary_postfix": 0,
        #     "atoms": 0.1,  # 数值
        # }
        self.cur_expr_id = 0
        self.operator_manager = operator_manager
        self.base_converter = BaseConverter(
            self.param_config.get("max_base"), self.param_config.get("custom_digits")
        )
        self.max_base = self.param_config.get("max_base")
        self.expr_evaluator = ExpressionEvaluator(
            param_config,
            logger,
            operator_manager,
            base_converter=self.base_converter,
        )
        unary_prefix_ops, unary_postfix_ops, self.binary_ops = (
            operator_manager.get_unary_and_binary_operators()
        )

        self.unary_postfix_ops = [
            opinfo for opinfo in unary_postfix_ops if opinfo.is_base is None
        ]
        self.unary_prefix_ops = [
            opinfo for opinfo in unary_prefix_ops if opinfo.is_base is None
        ]
        # operator到expression id的映射
        self.operators2expr: Dict[int, list[int]] = defaultdict(list)

        # 当是变量和数字的组合时，才需要考虑两者之间的权重分布
        self.atoms_type_weights = self.param_config.get("expr_atom_type_weights")
        # {
        #     "variable": 0.3,
        #     "number": 0.7,
        # }

    # def generate_random_symbol(self) -> Dict[str, Any]:
    #     return random.choice(self.operator_set)

    def set_variables(self, new_variables: List[str]):
        """
        Updates the list of variables used in expression generation.

        Args:
            new_variables (List[str]): A list of variable names to be used in expressions.
        """
        self.variables = new_variables

    def set_max_depth(self, max_depth: int) -> None:
        """
        Sets the maximum depth for generated expression trees.

        Args:
            max_depth (int): The maximum depth of the expression tree.
        """
        self.max_depth = max_depth
    
    def generate_random_value(self) -> int:
        """
        Generates a random integer value within the predefined min and max range.

        Returns:
            int: A randomly generated integer value.
        """
        return random.randint(self.min_value, self.max_value)

    def generate_random_base(self) -> int:
        """
        Generates a random base for number representation within the allowed range.

        Returns:
            int: A randomly selected base for number representation.
        """
        return random.randint(2, self.max_base)
        # pass

    # def generate_atoms(self) -> ExpressionNode:
    #     # 生成变量或带进制信息的数字
    #     atoms_type = random.choices(
    #         ["variable", "number"],
    #         weights=[
    #             self.atoms_type_weights["variable"],
    #             self.atoms_type_weights["number"],
    #         ],
    #     )[0]
    #     atoms_node = None
    #     if atoms_type == "variable":
    #         # TODO: 是否需要为所有变量做有分布的采样？
    #         atoms_node = VariableNode(random.choices(self.variable_set)[0])
    #     elif atoms_type == "number":
    #         atoms_node = NumberNode(
    #             self.generate_random_value(), self.generate_random_base()
    #         )
    #     else:
    #         raise NotImplementedError("In ExpressionGenerator: generate_atoms")

    #     return atoms_node

    def generate_atoms(self, atom_choice: str) -> ExpressionNode:
        """
        Generates an atomic node based on the specified type.

        Args:
            atom_choice (str): Specifies the type of atomic element to generate. Options are 'variable', 'number', or 'variable_and_number'.

        Returns:
            ExpressionNode: An atomic node representing either a variable or a number.

        Raises:
            ValueError: If the provided atom_choice is not recognized.
        """
        atoms_node = None
        if atom_choice == "variable":
            # 只生成变量
            atoms_node = VariableNode(random.choice(self.variables))
        elif atom_choice == "number":
            # 只生成数字
            atoms_node = NumberNode(
                self.generate_random_value(), self.generate_random_base()
            )
        elif atom_choice == "variable_and_number":
            # 生成变量和数字的组合
            atoms_type = random.choices(
                ["variable", "number"],
                weights=[
                    self.atoms_type_weights["variable"],
                    self.atoms_type_weights["number"],
                ],
            )[0]
            if atoms_type == "variable":
                atoms_node = VariableNode(random.choice(self.variables))
            else:
                atoms_node = NumberNode(
                    self.generate_random_value(), self.generate_random_base()
                )
        else:
            raise ValueError(
                f"Unknown atom_choice value: {atom_choice}. Valid options are 'variable', 'number', or 'variable_and_number'."
            )
        return atoms_node

    def generate_expression(
        self, cur_depth, max_depth, atom_choice: str
    ) -> Dict[str, Any]:
        """
        Recursively generates a random expression tree up to a specified depth.

        Args:
            cur_depth (int): Current depth of recursion.
            max_depth (int): Maximum depth of the expression tree.
            atom_choice (str): Determines what type of atoms can be generated ('variable', 'number', 'variable_and_number').

        Returns:
            ExpressionNode: A node representing part of the expression tree.
        """
        if cur_depth >= max_depth:
            expr_node = self.generate_atoms(atom_choice)
            return expr_node

        expr_type = random.choices(
            ["binary", "unary_prefix", "unary_postfix", "atoms"],
            weights=[
                self.expr_type_weights["binary"],
                self.expr_type_weights["unary_prefix"],
                self.expr_type_weights["unary_postfix"],
                self.expr_type_weights["atoms"],
            ],
        )[0]

        if expr_type == "binary":
            # 检查 binary_ops 是否为空
            if not self.binary_ops:
                # 如果为空，则重新随机选择其他类别
                return self.generate_expression(cur_depth, max_depth, atom_choice)
            select_op = random.choice(self.binary_ops)
            expr_node = BinaryExpressionNode(select_op)
            # 这里需要记录位置的原因在于：转换成表达式字符串的时候需要考虑括号的添加，尤其考虑结合性
            # 如：表达式树：1+（2+3），在输出2+3后，递归的上层需要考虑是否添加括号
            expr_node.left_expr = self.generate_expression(
                cur_depth + 1, max_depth, atom_choice
            )
            expr_node.left_expr.position = "left"
            expr_node.right_expr = self.generate_expression(
                cur_depth + 1, max_depth, atom_choice
            )
            expr_node.right_expr.position = "right"
            return expr_node
        elif expr_type == "unary_prefix":
            # 检查 unary_prefix_ops 是否为空
            if not self.unary_prefix_ops:
                # 如果为空，则重新随机选择其他类别
                return self.generate_expression(cur_depth, max_depth, atom_choice)
            select_op = random.choice(self.unary_prefix_ops)
            if select_op.is_base:
                print("error")
                exit(1)
            expr_node = UnaryExpressionNode(select_op)
            expr_node.unary_expr = self.generate_expression(
                cur_depth + 1, max_depth, atom_choice
            )
            expr_node.unary_expr.position = "unary"
            return expr_node
        elif expr_type == "unary_postfix":
            # 检查 unary_postfix_ops 是否为空
            if not self.unary_postfix_ops:
                # 如果为空，则重新随机选择其他类别
                return self.generate_expression(cur_depth, max_depth, atom_choice)
            select_op = random.choice(self.unary_postfix_ops)
            expr_node = UnaryExpressionNode(select_op)
            expr_node.unary_expr = self.generate_expression(
                cur_depth + 1, max_depth, atom_choice
            )
            expr_node.unary_expr.position = "unary"
        elif expr_type == "atoms":
            expr_node = expr_node = self.generate_atoms(atom_choice)
            return expr_node

    def create_expression(self, atom_choice: str) -> Dict[str, Any]:
        """
        Creates a new expression, evaluates it, and records the used operators.

        Args:
            atom_choice (str): Determines the type of atoms that can be included in the expression.

        Returns:
            Dict[str, Any]: Properties of the evaluated expression, including used operators.
        """
        expression_tree = self.generate_expression(
            cur_depth=0, max_depth=self.max_depth, atom_choice=atom_choice
        )
        self.expr_evaluator.init_expr(expression_tree, self.cur_expr_id)

        properties = self.expr_evaluator.evaluate()
        # print(properties["used_operators"])
        for op_id in properties["used_operators"]:
            self.operators2expr[op_id].append(self.cur_expr_id)

        # return expression_tree
        self.cur_expr_id += 1

        return properties

    def create_expression_str(self, atom_choice: str) -> Dict[str, Any]:
        """
        Generates a string representation of an expression with all sub-expressions enclosed in brackets.

        This method creates a new expression tree and evaluates it to obtain a string representation,
        ensuring that all parts of the expression are fully parenthesized for clarity. It also updates
        the unary and binary operators before generating the expression.

        Args:
            atom_choice (str): Specifies the type of atomic elements to include in the expression ('variable', 'number', or 'variable_and_number').

        Returns:
            str: A fully parenthesized string representation of the generated expression.
        """
        self.unary_prefix_ops, self.unary_postfix_ops, self.binary_ops = (
            self.operator_manager.get_unary_and_binary_operators()
        )
        expression_tree = self.generate_expression(
            cur_depth=0, max_depth=self.max_depth, atom_choice=atom_choice
        )
        self.expr_evaluator.set_with_all_brackets(True)
        self.expr_evaluator.init_expr(expression_tree, self.cur_expr_id, op_mode=True)
        # evaluator = ExpressionEvaluator(expression_tree, self.operator_manager)
        # properties = self.expr_evaluator.evaluate()

        return self.expr_evaluator.expression_str

    def dump_op2expr(self, file_path):
        """
        Dumps the mapping of operator IDs to expression IDs into a JSON Lines file.

        Each line in the output file contains a JSON object representing the relationship between
        an operator ID and the list of expression IDs that use this operator.

        Args:
            file_path (str): The path to the output file where the operator-expression mappings will be saved.
        """
        with open(file_path, "w") as f:
            for op_id in self.operators2expr:
                data = {
                    "op_id": op_id,
                    "expr_id": self.operators2expr[op_id],
                }
                json.dump(data, f)
                f.write("\n")


# if __name__ == "__main__":
#     # from operatorplus.operator_manager import OperatorManager

#     test_depth = [3]
#     all_scale = [
#         10,
#     ]
#     result = {}
#     # manager = OperatorManager("data/operator/initial_operators.jsonl")

#     param_config = ParamConfig("config/default.yaml")
#     log_config = LogConfig(param_config.config)
#     op_manager = OperatorManager(
#         param_config=param_config,
#         logger=log_config,
#         config_file="data/operator/op_test_12_8_1000.jsonl",
#     )
#     generator = ExpressionGenerator(op_manager, param_config, log_config)
#     for depth in test_depth:
#         generator.set_max_depth(depth)
#         for num in all_scale:
#             start_time = time.time()  # 记录开始时间
#             with open("data/expression/expression_test.jsonl", "w") as f:
#                 for i in range(num):
#                     properties = generator.create_expression("number")
#                     json.dump(properties, f)
#                     f.write("\n")
#             generator.dump_op2expr("data/expression/op2expr.jsonl")
#             end_time = time.time()
#             print(f"test_depth:{depth}, num={num}, time={end_time-start_time}")
#             result[depth] = end_time - start_time

# print(result)
# with open("data/expression/efficiency_with_tree.json", "w") as f:
#     json.dump(result, f)


# if __name__ == "__main__":
#     # 初始化 ConditionGenerator 时使用单变量 'a'
#     variables = ["a"]
#     operator_manager = OperatorManager(
#         config_file="data/operator/initial_operators.jsonl"
#     )

#     expr_generator = ExpressionGenerator(
#         variables=variables, operator_manager=operator_manager
#     )

#     # 生成条件表达式
#     for _ in range(10):
#         expr = expr_generator.create_expression_str(atom_choice="variable_and_number")
#         print(f"生成的表达式（仅 'a' 变量）: {expr}")
#         print("-" * 50)

#     # 更新变量列表为 'a' 和 'b'
#     expr_generator.set_variables(["a", "b"])
#     for _ in range(10):
#         expr = expr_generator.create_expression_str(atom_choice="variable_and_number")
#         print(f"生成的表达式（'a' 和 'b' 变量）: {expr}")
#         print("-" * 50)
