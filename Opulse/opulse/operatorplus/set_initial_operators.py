import json

def op_1(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN'
    return a + b
    
def op_count_1(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN'
    return 1


def op_2(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN'
    return a - b

def op_count_2(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN'
    return 1

def op_3(a):
    if a == 'NaN':
        return 'NaN'
    return -a

def op_count_3(a):
    if a == 'NaN':
        return 'NaN'
    return 1

def op_4(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN'
    return a * b

def op_count_4(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN'
    return min(abs(a), abs(b))


def op_5(a, b):   
    if a == 'NaN' or b == 'NaN':
        return 'NaN' 
    if b == 0:
        return 'NaN'
    return a // b

def op_count_5(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN' 
    if b == 0:
        return 'NaN'    
    return abs(a) // abs(b)

def op_6(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN' 
    if b == 0:
        return 'NaN'
    return a % b

def op_count_6(a, b):
    if a == 'NaN' or b == 'NaN':
        return 'NaN' 
    if b == 0:
        return 'NaN'  
    return abs(a) // abs(b)


{
  "op_compute_func": {
    "op_1": "def op_1(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a + b",
    "op_2": "def op_2(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a - b",
    "op_3": "def op_3(a):\n    if a == 'NaN':\n        return 'NaN'\n    return -a",
    "op_4": "def op_4(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a * b",
    "op_5": "def op_5(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return a // b",
    "op_6": "def op_6(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return a % b"
  },
  "op_count_func": {
    "op_count_1": "def op_count_1(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return 1",
    "op_count_2": "def op_count_2(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return 1",
    "op_count_3": "def op_count_3(a):\n    if a == 'NaN':\n        return 'NaN'\n    return 1",
    "op_count_4": "def op_count_4(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return min(abs(a), abs(b))",
    "op_count_5": "def op_count_5(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return abs(a) // abs(b)",
    "op_count_6": "def op_count_6(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return abs(a) // abs(b)"
  }
}

# operator1 = {
#     "id": 1,
#     "symbol": "+",
#     "n_ary": 2,
#     "unary_position": None,
#     "is_base": None,
#     "definition": None,
#     "definition_type": None,
#     # 'compute_complexity':None,
#     "priority": 1,
#     "associativity_direction": "left",
#     "n_order": 1,
#     "op_compute_func": "def op_1(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a + b",
#     "op_count_func": "def op_count_1(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return 1",
    
#     "properties": {
#         "commutativity": True,
#         "associativity": True,
#         "absorption": False,
#         "idempotency": False,
#     },
#     "dependencies": []
# }


# operator2 = {
#     "id": 2,
#     "symbol": "-",
#     "n_ary": 2,
#     "unary_position": None,
#     "is_base": None,
#     "definition": None,
#     "definition_type": None,
#     # 'compute_complexity':None,
#     "priority": 1,
#     "associativity_direction": "left",
#     "n_order": 1,
#     "op_compute_func": "def op_2(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a - b",
#     "op_count_func": "def op_count_2(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return 1",
#     "properties": {
#         "commutativity": False,
#         "associativity": False,
#         "absorption": False,
#         "idempotency": False,
#     },
#     "dependencies": []
# }


# operator3 = {
#     "id": 3,
#     "symbol": "-",
#     "n_ary": 1,
#     "unary_position": "prefix",
#     "is_base": None,
#     "definition": None,
#     "definition_type": None,
#     # 'compute_complexity':None,
#     "priority": 3,
#     "associativity_direction": "right",
#     "n_order": 1,
#     "op_compute_func": "def op_3(a):\n    if a == 'NaN':\n        return 'NaN'\n    return -a",
#     "op_count_func": "def op_count_3(a):\n    if a == 'NaN':\n        return 'NaN'\n    return 1",
#     "properties": {
#         "idempotency": False,
#     },
#     "dependencies": []
# }


# operator4 = {
#     "id": 4,
#     "symbol": "*",
#     "n_ary": 2,
#     "unary_position": None,
#     "is_base": None,
#     "definition": None,
#     "definition_type": None,
#     # 'compute_complexity':None,
#     "priority": 2,
#     "associativity_direction": "left",
#     "n_order": 2,
#     "op_compute_func": "def op_4(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a * b",
#     "op_count_func": "def op_count_4(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return min(abs(a), abs(b))",
#     "properties": {
#         "commutativity": True,
#         "associativity": True,
#         "absorption": False,
#         "idempotency": False,
#     },
#     "dependencies": [1]
# }

# #定义成了整除哦
# operator5 = {
#     "id": 5,
#     "symbol": "/",
#     "n_ary": 2,
#     "unary_position": None,
#     "is_base": None,
#     "definition": None,
#     "definition_type": None,
#     # 'compute_complexity':None,
#     "priority": 2,
#     "associativity_direction": "left",
#     "n_order": 2,
#     "op_compute_func": "def op_5(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return a // b",
#     "op_count_func": "def op_count_5(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return abs(a) // abs(b)",
#     "properties": {
#         "commutativity": False,
#         "associativity": False,
#         "absorption": False,
#         "idempotency": False,
#     },
#     "dependencies": [2]
# }

# operator6 = {
#     "id": 6,
#     "symbol": "%",
#     "n_ary": 2,
#     "unary_position": None,
#     "is_base": None,
#     "definition": None,
#     "definition_type": None,
#     # 'compute_complexity':None,
#     "priority": 2,
#     "associativity_direction": "left",
#     "n_order": 2,
#     "op_compute_func": "def op_6(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return a % b",
#     "op_count_func": "def op_count_6(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return abs(a) // abs(b)",
#     "properties": {
#         "commutativity": False,
#         "associativity": False,
#         "absorption": False,
#         "idempotency": False,
#     },
#     "dependencies": [2]
# }

operator1 = {
    "id": 1,
    "symbol": "+",
    "n_ary": 2,
    "unary_position": None,
    "is_base": None,
    "definition": None,
    "definition_type": None,
    "priority": 1,
    "associativity_direction": "left",
    "n_order": 1,
    "op_compute_func": "def op_1(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a + b",
    "op_count_func": "def op_count_1(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return 1",
    "z3_compute_func": "def op_1_z3(a, b):\n    return If(Or(a == NaN, b == NaN), NaN, a + b)",  # Added Z3 compute function
    "properties": {
        "commutativity": True,
        "associativity": True,
        "absorption": False,
        "idempotency": False,
    },
    "dependencies": []
}

operator2 = {
    "id": 2,
    "symbol": "-",
    "n_ary": 2,
    "unary_position": None,
    "is_base": None,
    "definition": None,
    "definition_type": None,
    "priority": 1,
    "associativity_direction": "left",
    "n_order": 1,
    "op_compute_func": "def op_2(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a - b",
    "op_count_func": "def op_count_2(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return 1",
    "z3_compute_func": "def op_2_z3(a, b):\n    return If(Or(a == NaN, b == NaN), NaN, a - b)",  # Added Z3 compute function
    "properties": {
        "commutativity": False,
        "associativity": False,
        "absorption": False,
        "idempotency": False,
    },
    "dependencies": []
}

operator3 = {
    "id": 3,
    "symbol": "-",
    "n_ary": 1,
    "unary_position": "prefix",
    "is_base": None,
    "definition": None,
    "definition_type": None,
    "priority": 3,
    "associativity_direction": "right",
    "n_order": 1,
    "op_compute_func": "def op_3(a):\n    if a == 'NaN':\n        return 'NaN'\n    return -a",
    "op_count_func": "def op_count_3(a):\n    if a == 'NaN':\n        return 'NaN'\n    return 1",
    "z3_compute_func": "def op_3_z3(a):\n    return If(a == NaN, NaN, -a)",  # Added Z3 compute function
    "properties": {
        "idempotency": False,
    },
    "dependencies": []
}

operator4 = {
    "id": 4,
    "symbol": "*",
    "n_ary": 2,
    "unary_position": None,
    "is_base": None,
    "definition": None,
    "definition_type": None,
    "priority": 2,
    "associativity_direction": "left",
    "n_order": 2,
    "op_compute_func": "def op_4(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return a * b",
    "op_count_func": "def op_count_4(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    return min(abs(a), abs(b))",
    "z3_compute_func": "def op_4_z3(a, b):\n    return If(Or(a == NaN, b == NaN), NaN, a * b)",  # Added Z3 compute function
    "properties": {
        "commutativity": True,
        "associativity": True,
        "absorption": False,
        "idempotency": False,
    },
    "dependencies": [1]
}

operator5 = {
    "id": 5,
    "symbol": "/",
    "n_ary": 2,
    "unary_position": None,
    "is_base": None,
    "definition": None,
    "definition_type": None,
    "priority": 2,
    "associativity_direction": "left",
    "n_order": 2,
    "op_compute_func": "def op_5(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return a // b",
    "op_count_func": "def op_count_5(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return abs(a) // abs(b)",
    "z3_compute_func": "def op_5_z3(a, b):\n    return If(Or(a == NaN, b == NaN, b == 0), NaN, a // b)",  # Added Z3 compute function
    "properties": {
        "commutativity": False,
        "associativity": False,
        "absorption": False,
        "idempotency": False,
    },
    "dependencies": [2]
}

operator6 = {
    "id": 6,
    "symbol": "%",
    "n_ary": 2,
    "unary_position": None,
    "is_base": None,
    "definition": None,
    "definition_type": None,
    "priority": 2,
    "associativity_direction": "left",
    "n_order": 2,
    "op_compute_func": "def op_6(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return a % b",
    "op_count_func": "def op_count_6(a, b):\n    if a == 'NaN' or b == 'NaN':\n        return 'NaN'\n    if b == 0:\n        return 'NaN'\n    return abs(a) // abs(b)",
    "z3_compute_func": "def op_6_z3(a, b):\n    return If(Or(a == NaN, b == NaN, b == 0), NaN, a % b)",  # Added Z3 compute function
    "properties": {
        "commutativity": False,
        "associativity": False,
        "absorption": False,
        "idempotency": False,
    },
    "dependencies": [2]
}

operators = [operator1, operator2, operator3, operator4, operator5, operator6]

# 将运算符写入 JSONL 文件的函数
def write_operator_to_jsonl(operators, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as file:  # 使用'a'模式追加到文件
            for operator in operators:  # 遍历每个运算符
                json_line = json.dumps(operator, ensure_ascii=False)  # 转换为 JSON 字符串
                file.write(json_line + '\n')  # 每个运算符写入一行
        print(f"Operators written to {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 调用函数，将运算符写入文件
write_operator_to_jsonl(operators, '/map-vepfs/kaijing/exp_mechanicalinterpretability/Opulse/opulse/data/operator/initial_operators.jsonl')

# 将运算符数据写入 JSON 文件的函数
def write_operators_to_json(operators, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:  # 使用'w'模式来创建或覆盖文件
            json.dump(operators, file, ensure_ascii=False, indent=4)  # 使用json.dump写入JSON文件
        print(f"Operators written to {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 调用函数，写入数据到 JSON 文件
write_operators_to_json(operators, '/map-vepfs/kaijing/exp_mechanicalinterpretability/Opulse/opulse/data/operator/initial_operators.json')