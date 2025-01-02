from preprocess import (
    preprocess_tokens,
    tokens_to_postfix,
    precedence,
    function_names,
    suffix_ops,
)
import math
import random


def evaluate_postfix(tokens):
    """计算后缀表达式的值"""
    stack = []

    for token in tokens:
        if (
            token not in precedence
            and token not in function_names
            and token not in ["Random"]
        ):
            # 数字或变量
            try:
                if token == "π":
                    value = math.pi
                elif token == "e":
                    value = math.e
                else:
                    value = float(token)
                stack.append(value)
            except ValueError:
                raise ValueError(f"语法错误: {token}")
        else:
            # 运算符或函数
            if token in suffix_ops or token in function_names:
                if not stack:
                    raise ValueError("缺少操作数")
                x = stack.pop()

                if token == "!":
                    if x < 0 or not x.is_integer():
                        raise ValueError("阶乘只能用于非负整数")
                    result = math.factorial(int(x))
                elif token == "i":
                    result = complex(0, x)
                elif token == "%":
                    result = x / 100
                elif token == "abs":
                    result = abs(x)
                elif token == "sin":
                    result = math.sin(x)
                elif token == "cos":
                    result = math.cos(x)
                elif token == "tan":
                    result = math.tan(x)
                elif token == "arcsin":
                    result = math.asin(x)
                elif token == "arccos":
                    result = math.acos(x)
                elif token == "arctan":
                    result = math.atan(x)
                else:
                    raise ValueError(f"未知运算: {token}")

                stack.append(result)

            elif token == "Random":
                stack.append(random.random())

            elif token in ["(+)", "(-)"]:
                if not stack:
                    raise ValueError("缺少操作数")
                x = stack.pop()
                if token == "(-)":
                    x = -x
                stack.append(x)

            else:  # 二元运算符
                if len(stack) < 2:
                    raise ValueError("缺少操作数")
                b = stack.pop()
                a = stack.pop()

                if token == "+":
                    result = a + b
                elif token == "-":
                    result = a - b
                elif token == "*":
                    result = a * b
                elif token == "/":
                    if b == 0:
                        raise ValueError("除数不能为零")
                    result = a / b
                elif token == "mod":
                    if b == 0:
                        raise ValueError("除数不能为零")
                    result = a % b
                elif token == "^":
                    result = pow(a, b)

                stack.append(result)

    if not stack:
        stack = [0]
    if len(stack) > 1:
        raise ValueError("操作符不足")

    return stack[0]


def handle_input(expression, key):
    OP_MAPEX = {
        "": [],
        "MC": ["M"],
        "x^2": ["^", "2"],
        "x^3": ["^", "3"],
        "x^y": ["^"],
        "x^-1": ["^", "-1"],
        "10^x": ["10", "^"],
        "e^x": ["e", "^"],
        "x!": ["!"],
        "|x|": ["abs"],
        "sin^-1": ["arcsin"],
        "cos^-1": ["arccos"],
        "tan^-1": ["arctan"],
        "Mod": ["mod"],
        "Ran#": ["Random"],
        "*10^n": ["*", "10", "^"],
    }
    if key in OP_MAPEX:
        key = OP_MAPEX[key]
    else:
        match key:
            case "DEL":
                if expression:
                    expression.pop()
                key = []
            case "AC":
                expression = []
                key = ["0"]
            case "←":
                if len(expression) > 1:
                    # 将最后一个元素移到开头
                    last = expression.pop()
                    expression.insert(0, last)
                key = []
            case "→":
                if len(expression) > 1:
                    # 将第一个元素移到末尾
                    first = expression.pop(0)
                    expression.append(first)
                key = []
            case "Exit":
                import sys
                import webview

                for window in webview.windows:
                    window.destroy()
                sys.exit(0)
            case _:
                key = [key]

    assert isinstance(key, list)
    return expression + key


def calculate(expression, state):
    """计算表达式的值"""
    processed = preprocess_tokens(expression, mode="full")
    try:
        postfix = tokens_to_postfix(processed)
        result = evaluate_postfix(postfix)

        # 格式化输出
        if isinstance(result, complex):
            result_str = f"Ans = {result.real:.10g} + {result.imag:.10g}i"
        else:
            # 去除不必要的小数点和零
            str_result = f"{result:.10g}"
            return f"Ans = {str_result}"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        import traceback

        print(f"错误: {str(e)}")
        print(traceback.format_exc())
        return f"Error: {str(e)}"


def display(expression, state):
    """生成表达式的显示形式"""
    processed = preprocess_tokens(expression, mode="full")
    return " ".join(processed)
