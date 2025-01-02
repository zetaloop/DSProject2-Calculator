from typing import Literal

precedence = {
    "!": 2,
    "i": 2,
    "%": 2,
    "^": 3,
    "(+)": 4,
    "(-)": 4,
    "*": 5,
    "/": 5,
    "mod": 5,
    "FUNC": 6,
    "+": 7,
    "-": 7,
}

function_names = {
    "sqrt",
    "cbrt",
    "log",
    "ln",
    "abs",
    "sin",
    "cos",
    "tan",
    "arcsin",
    "arccos",
    "arctan",
    "int",
}

suffix_ops = {"!", "%"}


def preprocess_tokens(tokens):
    """
    预处理：
      0) 去掉光标
      1) 自动合并相邻数字，形成单一数字 token。
      2) 修正不平衡的括号。
      3) 在相邻需要隐式乘法的地方插入 '*'
    """
    # 0) 去掉光标
    tokens = [t for t in tokens if t != "|"]

    # 1) 自动合并相邻数字
    merged = []
    number_buffer = []
    for tk in tokens:
        if all(c in ".0123456789" for c in tk):
            number_buffer.append(tk)
        else:
            if number_buffer:
                merged.append("".join(number_buffer))
                number_buffer.clear()
            merged.append(tk)
    if number_buffer:
        merged.append("".join(number_buffer))
    merged = [".0" if t == "." else t for t in merged]

    # 2) 修正括号
    corrected = []
    unpaired_left = 0
    unmatched_right = 0

    for tk in merged:
        if tk == "(":
            unpaired_left += 1
            corrected.append(tk)
        elif tk == ")":
            # 如果有匹配的 '(' 则与其配对。否则计为未匹配。
            if unpaired_left > 0:
                unpaired_left -= 1
                corrected.append(tk)
            else:
                unmatched_right += 1
                corrected.append(tk)
        else:
            corrected.append(tk)
    # 在开头插入与 unmatched_right 数量相等的 '('
    corrected = ["("] * unmatched_right + corrected
    # 如果还有未匹配的 '('，则在末尾添加对应的 ')'
    while unpaired_left > 0:
        corrected.append(")")
        unpaired_left -= 1

    # 3) 插入隐式乘法
    res = []

    def is_operand_or_rpar_or_suffix(t):
        if t in suffix_ops:
            return True
        if t == ")":
            return True
        if t in function_names:
            return False
        if t in ("+", "-", "*", "/", "mod", "^", "("):
            return False
        return True

    def is_operand_or_lpar_or_function(t):
        if t in suffix_ops:
            return False
        if t == "(":
            return True
        if t in function_names:
            return True
        if t in ("+", "-", "*", "/", "mod", "^", ")"):
            return False
        return True

    for i, tk in enumerate(corrected):
        res.append(tk)
        if i < len(corrected) - 1:
            nxt = corrected[i + 1]
            if is_operand_or_rpar_or_suffix(tk) and is_operand_or_lpar_or_function(nxt):
                res.append("*")

    return res


def tokens_to_postfix(tokens):
    """
    将修正和插入隐式乘法后的 token 转换为后缀表达式。
    注意一元 +/- 与后缀运算符。
    """
    associativity = {
        "!": "left",
        "i": "left",
        "%": "left",
        "^": "right",
        "(+)": "right",
        "(-)": "right",
        "*": "left",
        "/": "left",
        "mod": "left",
        "FUNC": "right",
        "+": "left",
        "-": "left",
    }

    def get_precedence(op):
        if op in function_names:
            return precedence["FUNC"]
        return precedence.get(op, None)

    def get_associativity(op):
        if op in function_names:
            return associativity["FUNC"]
        return associativity.get(op, None)

    def is_number_or_var(tk):
        if tk in function_names:
            return False
        if tk in precedence or tk in ("(", ")"):
            return False
        return True

    def is_suffix_op(tk):
        return tk in suffix_ops

    output_queue = []
    op_stack = []
    last_token_type = None

    for tk in tokens:
        if is_number_or_var(tk):
            output_queue.append(tk)
            last_token_type = "operand"
        elif tk in function_names:
            op_stack.append(tk)
            last_token_type = "function"
        elif tk == "(":
            op_stack.append(tk)
            last_token_type = "lpar"
        elif tk == ")":
            while op_stack and op_stack[-1] != "(":
                output_queue.append(op_stack.pop())
            if op_stack and op_stack[-1] == "(":
                op_stack.pop()
            else:
                raise ValueError("括号不匹配：多余的 ')'")
            if op_stack and op_stack[-1] in function_names:
                output_queue.append(op_stack.pop())
            last_token_type = "rpar"
        elif is_suffix_op(tk):
            prec_tk = get_precedence(tk)
            assoc_tk = get_associativity(tk)
            while op_stack:
                top = op_stack[-1]
                if top == "(":
                    break
                top_prec = get_precedence(top)
                top_assoc = get_associativity(top)
                if top_prec is None:
                    break
                if top_assoc == "left":
                    if top_prec <= prec_tk:
                        output_queue.append(op_stack.pop())
                    else:
                        break
                elif top_assoc == "right":
                    if top_prec < prec_tk:
                        output_queue.append(op_stack.pop())
                    else:
                        break
                else:
                    break
            op_stack.append(tk)
            last_token_type = "operator"
        elif tk in ("+", "-"):
            if last_token_type in (None, "operator", "function", "lpar"):
                unary_op = "(+)" if tk == "+" else "(-)"
                prec_tk = 4
                assoc_tk = "right"
                while op_stack:
                    top = op_stack[-1]
                    if top == "(":
                        break
                    top_prec = get_precedence(top)
                    if top_prec is None:
                        break
                    top_assoc = get_associativity(top)
                    if top_assoc == "left":
                        if top_prec <= prec_tk:
                            output_queue.append(op_stack.pop())
                        else:
                            break
                    elif top_assoc == "right":
                        if top_prec < prec_tk:
                            output_queue.append(op_stack.pop())
                        else:
                            break
                    else:
                        break
                op_stack.append(unary_op)
                last_token_type = "operator"
            else:
                prec_tk = get_precedence(tk)
                assoc_tk = get_associativity(tk)
                while op_stack:
                    top = op_stack[-1]
                    if top == "(":
                        break
                    top_prec = get_precedence(top)
                    if top_prec is None:
                        break
                    top_assoc = get_associativity(top)
                    if top_assoc == "left":
                        if top_prec <= prec_tk:
                            output_queue.append(op_stack.pop())
                        else:
                            break
                    elif top_assoc == "right":
                        if top_prec < prec_tk:
                            output_queue.append(op_stack.pop())
                        else:
                            break
                    else:
                        break
                op_stack.append(tk)
                last_token_type = "operator"
        else:
            prec_tk = get_precedence(tk)
            if prec_tk is None:
                raise ValueError(f"无法识别的符号: {tk}")
            assoc_tk = get_associativity(tk)
            while op_stack:
                top = op_stack[-1]
                if top == "(":
                    break
                top_prec = get_precedence(top)
                if top_prec is None:
                    break
                top_assoc = get_associativity(top)
                pop_condition = False
                if assoc_tk == "left":
                    if top_prec <= prec_tk:
                        pop_condition = True
                else:
                    if top_prec < prec_tk:
                        pop_condition = True
                if pop_condition:
                    output_queue.append(op_stack.pop())
                else:
                    break
            op_stack.append(tk)
            last_token_type = "operator"

    while op_stack:
        top = op_stack.pop()
        if top == "(" or top == ")":
            raise ValueError("括号不匹配：多余的括号")
        output_queue.append(top)

    return output_queue


if __name__ == "__main__":
    test_expressions = [
        ["+", "3", "!", "i", "^", "e", ".", "%"],
        ["1", "+", "2", ")", "4"],
        ["2", "sin", "3"],
        ["(", "-", "x", ")", "(", "y", "+", "2", ")"],
        ["3", "(", ".", "5"],
        ["(", "(", "1", ")", "(", "2", ")", ")"],
    ]

    for idx, tklist in enumerate(test_expressions, 1):
        try:
            pre = preprocess_tokens(tklist)
            rpn = tokens_to_postfix(pre)
            print(f"Test {idx} =>")
            print(f"  Original: {tklist}")
            print(f"  PreProc : {pre}")
            print(f"  Postfix : {rpn}\n")
        except ValueError as e:
            print(f"Test {idx} 出错: {e}\n")
