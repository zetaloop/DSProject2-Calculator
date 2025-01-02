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
    """处理输入按键，维护 expression 数组，并将 '|' 视为光标位置。"""

    # 如果 expression 里没有光标，则默认加在末尾
    if "|" not in expression:
        expression.append("|")

    cursor_index = expression.index("|")

    # 先做一些映射（与原先一样），比如 "x^2" -> ["^", "2"] 等
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

    # key 可能被映射为列表
    mapped_key = OP_MAPEX.get(key, None)

    if mapped_key is not None:
        key_list = mapped_key
    else:
        # 处理特殊按键
        match key:
            case "DEL":
                # 删除光标左侧的一个 token
                if cursor_index > 0:
                    expression.pop(cursor_index - 1)
                    cursor_index -= 1
                # 若左侧没有 token 了，就删除右侧
                elif cursor_index < len(expression) - 1:
                    expression.pop(cursor_index + 1)
                key_list = []
            case "AC":
                # 全部清空，并给一个初始“0”
                expression = ["|", "0"]
                return expression
            case "←":
                # 光标左移
                if cursor_index > 0:
                    expression[cursor_index], expression[cursor_index - 1] = (
                        expression[cursor_index - 1],
                        expression[cursor_index],
                    )
                    cursor_index -= 1
                key_list = []
            case "→":
                # 光标右移
                if cursor_index < len(expression) - 1:
                    expression[cursor_index], expression[cursor_index + 1] = (
                        expression[cursor_index + 1],
                        expression[cursor_index],
                    )
                    cursor_index += 1
                key_list = []
            case "Exit":
                import sys
                import webview

                for window in webview.windows:
                    window.destroy()
                sys.exit(0)
            case _:
                key_list = [key]

    # 将新的 key_list 插入到光标位置之前
    for k in key_list:
        expression.insert(cursor_index, k)
        cursor_index += 1

    return expression


def calculate(expression, state):
    """计算表达式的值"""
    processed = preprocess_tokens(expression)
    try:
        postfix = tokens_to_postfix(processed)
        result = evaluate_postfix(postfix)

        # 格式化输出
        if isinstance(result, complex):
            result_str = f"Ans = {result.real:.10g} + {result.imag:.10g}i"
        else:
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
    """生成表达式的显示形式（包含 '|' 光标）"""
    return " ".join(expression)

    # 然后再把光标插回原位置
    display_tokens = []
    idx = 0
    for t in expression:
        if t == "|":
            display_tokens.append("|")  # 暂时先用 '|'，前端去换成光标
        else:
            # 这里要与 processed_for_display 对应地往下取一个
            if idx < len(processed_for_display):
                display_tokens.append(processed_for_display[idx])
                idx += 1

    # 如果 processed_for_display 比 expression 少一些括号补全，也没关系，原则上不影响展示
    # 最后用空格拼接返回
    return " ".join(display_tokens)
