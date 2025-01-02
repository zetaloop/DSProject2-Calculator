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
                raise ValueError(f"无法识别的token: {token}")
        else:
            # 运算符或函数
            if token in suffix_ops or token in function_names:
                if not stack:
                    raise ValueError("表达式错误：缺少操作数")
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

                stack.append(result)

            elif token == "Random":
                stack.append(random.random())

            elif token in ["(+)", "(-)"]:
                if not stack:
                    raise ValueError("表达式错误：缺少操作数")
                x = stack.pop()
                if token == "(-)":
                    x = -x
                stack.append(x)

            else:  # 二元运算符
                if len(stack) < 2:
                    raise ValueError("表达式错误：缺少操作数")
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
        raise ValueError("表达式为空")
    if len(stack) > 1:
        raise ValueError("表达式错误：操作符不足")

    return stack[0]


def handle_input(expression, key):
    OP_MAPEX = {
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
    if not key:  # 仅当初始化时传回空键
        expression = []
        key = "0"
    if key in OP_MAPEX:
        key = OP_MAPEX[key]
    else:
        key = [key]
    assert isinstance(key, list)
    return expression + key


def display(expression):
    """显示当前表达式"""
    try:
        processed = preprocess_tokens(expression)
        return " ".join(processed)
    except ValueError as e:
        return str(e)


def calculate(expression):
    """计算表达式的值"""
    try:
        processed = preprocess_tokens(expression)
        postfix = tokens_to_postfix(processed)
        result = evaluate_postfix(postfix)

        # 格式化输出
        if isinstance(result, complex):
            return f"Ans = {result.real:.10g} + {result.imag:.10g}i"
        else:
            # 去除不必要的小数点和零
            str_result = f"{result:.10g}"
            return f"Ans = {str_result}"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
