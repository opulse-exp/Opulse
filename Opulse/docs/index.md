# ReadMe

<a id="readme-top"></a> 

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/opulse-exp/Opulse.git">
    <img src="docs\assets\images\logo.png" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Opulse</h3>

  <p align="center">
    Opulse is a dynamic operator generation system designed to create and manage mathematical operators, with 'pulse' reflecting its dynamic and impactful nature in the creation process!
    <br />
    <a href="https://github.com/opulse-exp/Opulse.git"><strong>Explore the docs »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <!-- <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#module structure">Module Structure</a></li>
      </ul>
    </li> -->
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <!-- <li><a href="#prerequisites">Prerequisites</a></li> -->
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <!-- <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<!-- ## About The Project

### Module Structure

```
opulse/
├── config
│   ├── __init__.py
│   ├── default.yaml
│   ├── log_config.py
│   └── param_config.py
├── data
│   ├── expression
│   ├── operator
│   └── dependency  
├── logs
├── expression
│   ├── __init__.py
│   ├── base_converter.py
│   ├── expression_base_converter.py
│   ├── expression_evaluator.py
│   ├── expression_expander.py
│   ├── expression_generator.py
│   ├── expression_info.py
│   ├── expression_node.py
├── operatorplus
│   ├── __init__.py
│   ├── condition_generator.py
│   ├── operator_definition_parser.py
│   ├── operator_dependency_graph.py
│   ├── operator_generator.py
│   ├── operator_info.py
│   ├── operator_manager.py
│   ├── operator_priority_manager.py
│   ├── operator_transformer_z3.py
│   ├── operator_transformer.py
│   ├── set_initial_operators.py
├── generate_operator_dependency_graph.py
├── generate_operator.py
├── generate_base_operator.py
├── assign_operator_priority.py
├── generate_operator_dependency_graph.py
├── delete_operators.py
├── generate_expression.py
├── assign_operator_priority.py
└── delete_operators.py
```
The overall project is divided into two parts: symbol generation (under the operatorplus directory) and expression generation (under the expression directory).

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- GETTING STARTED -->
## Getting Started


### Installation

```bash
git clone https://github.com/opulse-exp/Opulse.git
cd ./Opulse
pip install -r requirement.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### generate operator
```bash
python generate_operator.py \
  --config "$CONFIG_PATH" \
  --initial-operators-path "$INITIAL_OPERATORS_PATH" \
  --generated-operators-path "$GENERATED_OPERATORS_PATH" \
  --num "$NUM_OPERATORS"
```

### generate expression

```bash
python generate_expression.py \
    --config "$CONFIG_PATH" \
    --operators-path "$OPERATORS_PATH" \
    --generated-expression-path "$GENERATED_EXPRESSION_PATH" \
    --generated-opexpr-dependency-path "$GENERATED_OPEXPRESS_DEPENDENCY_PATH" \
    --num "$NUM" \
    --thread "$THREADS"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>






