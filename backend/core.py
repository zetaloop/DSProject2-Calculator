from preprocess import (
    preprocess_tokens,
    tokens_to_postfix,
    precedence,
    function_names,
    suffix_ops,
)
import math
import random
from fractions import Fraction


def evaluate_postfix(tokens, state):
    """计算后缀表达式的值"""
    stack = []

    for token in tokens:
        if (
            token not in precedence
            and token not in function_names
            and token not in ["Random", "Ans", "M"]
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
                elif token == "int":
                    result = int(x)
                elif token == "sqrt":
                    if x < 0:
                        raise ValueError("平方根的参数不能为负数")
                    result = math.sqrt(x)
                elif token == "cbrt":
                    result = math.copysign(abs(x) ** (1 / 3), x)  # 支持负数的立方根
                elif token == "log":
                    if x <= 0:
                        raise ValueError("对数的参数必须为正数")
                    result = math.log10(x)
                elif token == "ln":
                    if x <= 0:
                        raise ValueError("对数的参数必须为正数")
                    result = math.log(x)
                else:
                    raise ValueError(f"未知运算: {token}")

                stack.append(result)

            elif token == "Random":
                stack.append(random.random())

            elif token == "Ans":
                stack.append(state["_current_ans"])

            elif token == "M":
                stack.append(state.get("memory", 0))

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
                    try:
                        result = pow(a, b)
                    except OverflowError:
                        raise ValueError("结果过大")
                elif token == "nPr":
                    # 检查参数
                    if not (a >= 0 and b >= 0 and a.is_integer() and b.is_integer()):
                        raise ValueError("排列数的参数必须是非负整数")
                    if b > a:
                        raise ValueError("排列数的第二个参数不能大于第一个参数")
                    # 计算 P(n,r) = n!/(n-r)!
                    n, r = int(a), int(b)
                    result = math.factorial(n) // math.factorial(n - r)
                elif token == "nCr":
                    # 检查参数
                    if not (a >= 0 and b >= 0 and a.is_integer() and b.is_integer()):
                        raise ValueError("组合数的参数必须是非负整数")
                    if b > a:
                        raise ValueError("组合数的第二个参数不能大于第一个参数")
                    # 计算 C(n,r) = n!/((n-r)!r!)
                    n, r = int(a), int(b)
                    result = math.factorial(n) // (
                        math.factorial(n - r) * math.factorial(r)
                    )

                stack.append(result)

    if not stack:
        stack = [0]
    if len(stack) > 1:
        raise ValueError("操作符不足")

    return stack[0]


def handle_input(expression, state, key):
    """处理输入按键，维护 expression 数组，并将 '|' 视为光标位置。"""

    # 如果 expression 里没有光标，则默认加在末尾
    if "|" not in expression:
        expression.append("|")

    cursor_index = expression.index("|")

    # 处理 Ans 变量
    state["ans"] = state["_current_ans"]

    OP_MAPEX = {
        "": [],
        "MR": ["M"],
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
        # 答案状态
        state["showing_answer"] = False
        # 处理特殊按键
        match key:
            case "=" | "M+" | "M-" | "MC":
                state["showing_answer"] = True
                key_list = []
            case "SCI":
                # 切换科学计数法状态
                state["use_scientific"] = not state.get("use_scientific", False)
                state["use_fraction"] = False
                state["number_base"] = "Dec"
                key_list = []
            case "S⇔D":
                # 切换分数显示状态
                state["use_fraction"] = not state.get("use_fraction", False)
                state["use_scientific"] = False
                state["number_base"] = "Dec"
                key_list = []
            case "Dec" | "Bin" | "Oct" | "Hex":
                state["number_base"] = key
                state["use_scientific"] = False
                state["use_fraction"] = False
                key_list = []
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
                # 全部清空
                expression = ["|"]
                key_list = []
            case "MC":
                # 清除内存
                state["memory"] = 0
                key_list = []
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
            case "Ans":
                # 插入 Ans 变量
                key_list = ["Ans"]
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
        result = evaluate_postfix(postfix, state)

        # 更新预测结果
        state["_predicted_ans"] = result

        # 格式化结果
        str_result = format_result(result, state)
        return str_result, result
    except ValueError as e:
        return f"Error: {str(e)}", 0
    except Exception as e:
        import traceback

        print(f"错误: {str(e)}")
        print(traceback.format_exc())
        return f"Error: {str(e)}", 0


def decimal_to_fraction(decimal):
    """将小数转换为最简分数"""
    try:
        # 使用 Fraction 自动处理转换和化简
        frac = Fraction(decimal).limit_denominator()
        return f"{frac.numerator}/{frac.denominator}"
    except (ValueError, OverflowError):
        # 如果转换失败，返回原始数字
        return f"{decimal}/1"


def format_number_base(number, base):
    """根据进制格式化数字，包括整数和小数"""

    def convert_fractional_part(fraction, base):
        """将小数部分转换为指定进制"""
        result = []
        for _ in range(15):  # 限制精度为 15 位
            fraction *= base
            digit = int(fraction)
            result.append(digit)
            fraction -= digit
            if fraction == 0:
                break
        return "".join(str(d) for d in result)

    if base not in ["Bin", "Oct", "Hex"]:
        raise ValueError("Base must be 'Bin', 'Oct', or 'Hex'")
    base_map = {"Bin": 2, "Oct": 8, "Hex": 16}
    base_value = base_map[base]

    if isinstance(number, str):
        number = float(number)
    # 处理整数部分和小数部分
    integer_part = int(number)
    fractional_part = number - integer_part
    # 转换整数部分
    if base == "Bin":
        integer_str = bin(integer_part)[2:]
    elif base == "Oct":
        integer_str = oct(integer_part)[2:]
    elif base == "Hex":
        integer_str = hex(integer_part)[2:].upper()
    # 转换小数部分
    if fractional_part > 0:
        fractional_str = convert_fractional_part(fractional_part, base_value)
        return f"{integer_str}.{fractional_str}"
    else:
        return integer_str


def format_result(result, state):
    """格式化结果"""
    if state.get("use_scientific", False):
        str_result = f"{result:.30e}"
    elif state.get("use_fraction", False):
        str_result = decimal_to_fraction(result)
    elif state.get("number_base", "Dec") != "Dec":
        str_result = format_number_base(result, state.get("number_base", "Dec"))
    else:
        str_result = f"{result:.15g}"

    prefix = "Ans = " if state["showing_answer"] else "Ans (predicted) = "
    return f"{prefix}{str_result}"
