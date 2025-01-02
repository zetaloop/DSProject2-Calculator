# 模块级常量定义
precedence = {
    # 后缀运算符
    "!": 2,
    "i": 2,
    "%": 2,
    # 幂
    "^": 3,
    # 一元 +、- 用特殊标记: '(+)' , '(-)'，同样用 precedence=4
    "(+)": 4,
    "(-)": 4,
    # 乘除 mod
    "*": 5,
    "/": 5,
    "mod": 5,
    # 函数：如 sin, cos, ...
    "FUNC": 6,
    # 二元 +、-
    "+": 7,
    "-": 7,
}

# 函数名集合
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
}

# 后缀运算符集合
suffix_ops = {"!", "i", "%"}


def preprocess_tokens(tokens):
    """
    预处理：
    1) 自动修正左右括号不平衡（如多出的右括号则在开头补左括号，最后若左括号多余则补右括号）。
    2) 在相邻需要隐式乘法的位置插入 '*'。
    返回修正后的 token 列表。
    """

    # --- 1) 修正多出的右括号：扫描时如果发现多出的 ')' 就在前面补 '(' ---
    corrected = []
    unpaired_left = 0  # 记录已经出现但未匹配的 '(' 数量
    for tk in tokens:
        if tk == ")":
            # 如果没有可匹配的左括号，就在前面补一个 '('
            if unpaired_left <= 0:
                corrected.append("(")
                unpaired_left += 1
            unpaired_left -= 1
            corrected.append(tk)
        elif tk == "(":
            unpaired_left += 1
            corrected.append(tk)
        else:
            corrected.append(tk)

    # --- 2) 若最后还有剩余没配对的 '('，则在末尾补齐 ')' ---
    while unpaired_left > 0:
        corrected.append(")")
        unpaired_left -= 1

    # --- 3) 插入隐式乘法 ---
    #   判断规则（简化思路）：当出现 [X, Y] 两个相邻token，
    #   如果 X 是“可做操作数”或右括号或后缀运算符，而 Y 是“可做操作数”或左括号或函数名，
    #   则在 X 与 Y 之间插入 '*'
    #
    #   这里的“可做操作数”包括数字、变量名、常量符号(M, Ans, e, π等)等
    #   后缀运算符：'!', 'i', '%'
    #   函数名：'sin', 'cos', ... (后面再去 shunting yard 处理)
    #
    #   例如：
    #     "3 e" -> "3 * e"
    #     ") x" -> ") * x"
    #     ") sin" -> ") * sin"
    #     "log )" 不常见(表达式有误)，但若已补括号变成 "( log )"? 具体看逻辑需求
    #
    #   注意：这里也会把数字和 '.'（被改为 '0.'）的并排情况变成乘法，如 "3 ."
    #        就会变为 "3 * 0."。
    #
    res = []

    def is_operand_or_rpar_or_suffix(t):
        # 是数字、变量名、常量，或者右括号)，或者后缀运算符
        # 简单判断：不是运算符(+, -, *, /, mod, ^, '(') 且 也不是函数名
        # 就暂且认为是“可做操作数”；或本身就是 ')'；或是后缀运算符
        if t in suffix_ops:
            return True
        if t == ")":
            return True
        if t in function_names:
            return False
        if t in (
            "+",
            "-",
            "*",
            "/",
            "mod",
            "^",
            "(",
        ):
            return False
        return True

    def is_operand_or_lpar_or_function(t):
        # 与上面相对：是可做操作数，或 '(' 或函数名
        if t in suffix_ops:
            return False  # 后缀运算符不属于这类
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
            next_tk = corrected[i + 1]
            # 判断是否需要插入 '*'
            if is_operand_or_rpar_or_suffix(tk) and is_operand_or_lpar_or_function(
                next_tk
            ):
                # 在 tk 与 next_tk 之间插入 '*'
                res.append("*")

    return res


def tokens_to_postfix(tokens):
    """
    在插入隐式乘法、修正括号后，再将自然顺序 tokens 转换为后缀表达式 tokens。
    注意区分一元 +/-, 并在输出时写成 '(+)' 或 '(-)'。
    """

    # 1) 定义运算符的优先级 (数值越小，优先级越高)
    #    并定义运算符的结合性(left / right)。
    associativity = {
        # 后缀运算符 => 左结合
        "!": "left",
        "i": "left",
        "%": "left",
        "^": "right",
        "(+)": "right",
        "(-)": "right",
        "*": "left",
        "/": "left",
        "mod": "left",
        # 函数视为右结合一元运算符
        "FUNC": "right",
        "+": "left",
        "-": "left",
    }

    # 2) 定义一个工具函数，用来获取运算符对应的优先级 / 结合性
    def get_precedence(op):
        # 如果是已知函数名，则返回 FUNC 的优先级
        if op in function_names:
            return precedence["FUNC"]
        return precedence.get(op, None)

    def get_associativity(op):
        if op in function_names:
            return associativity["FUNC"]
        return associativity.get(op, None)

    # 3) 辅助判断：某个 token 是否是数字或标识符(变量、M、Ans、Random、π、e 等)
    def is_number_or_var(tk):
        # 粗略判断：只要不在运算符/括号/函数集里，就视为数字或变量
        # 当然可根据需要改写成更严格的判断
        if tk in function_names:
            return False
        if tk in precedence or tk in ("(", ")"):
            return False
        # 否则就认为是数字(含小数点) 或 变量
        return True

    # 4) 判断该 token 是否为后缀运算符
    def is_suffix_op(tk):
        return tk in suffix_ops

    # 5) 准备输出队列、运算符栈
    output_queue = []
    op_stack = []

    # 用于判断一元 / 二元 加减
    # 如果前一个 token 能作为“表达式结尾”(数字、变量、右括号、后缀运算符) => 下一个 '+'/'-' 就是二元
    # 否则就是一元
    last_token_type = (
        None  # 可取 'operand' / 'operator' / 'lpar' / 'rpar' / 'function' / None
    )

    for tk in tokens:

        if is_number_or_var(tk):
            # 普通数字或变量，直接放到输出
            output_queue.append(tk)
            last_token_type = "operand"

        elif tk in function_names:
            # 函数名：当做一元运算符入栈
            op_stack.append(tk)
            last_token_type = "function"

        elif tk == "(":
            # 左括号直接入栈
            op_stack.append(tk)
            last_token_type = "lpar"

        elif tk == ")":
            # 弹栈直到遇到 '('
            while op_stack and op_stack[-1] != "(":
                output_queue.append(op_stack.pop())
            # 弹出 '('
            if op_stack and op_stack[-1] == "(":
                op_stack.pop()
            else:
                raise ValueError("括号不匹配：发现多余的 ')'")

            # 如果弹栈后栈顶是函数名，则再把函数弹出到输出
            if op_stack and op_stack[-1] in function_names:
                output_queue.append(op_stack.pop())

            last_token_type = "rpar"

        elif is_suffix_op(tk):
            # 后缀运算符
            prec_tk = get_precedence(tk)  # 2
            assoc_tk = get_associativity(tk)  # left
            # 弹栈条件： 栈顶也是运算符 且 ( (左结合 & top优先级 <= tk优先级) or (右结合 & <) )
            while op_stack:
                top = op_stack[-1]
                if top == "(":
                    break
                top_prec = get_precedence(top)
                top_assoc = get_associativity(top)
                if top_prec is None:
                    break  # 非运算符，比如异常？
                # 判断是否要弹出
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
            # 自己入栈
            op_stack.append(tk)
            last_token_type = "operator"

        elif tk in ("+", "-"):
            # 可能是一元也可能是二元
            # 判断前一个 token 是否是“能结尾的”operand（数字/变量/右括号/后缀）？
            if last_token_type in (None, "operator", "function", "lpar"):
                # 一元正号或负号
                # 输出时要记成 '(+)' 或 '(-)'
                unary_op = "(+)" if tk == "+" else "(-)"
                prec_tk = 4  # 一元 +/-
                assoc_tk = "right"
                # 弹栈
                while op_stack:
                    top = op_stack[-1]
                    if top == "(":
                        break
                    top_prec = get_precedence(top)
                    if top_prec is None:
                        break
                    top_assoc = get_associativity(top)
                    # 判断弹栈条件
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
                # 压入一元符号
                op_stack.append(unary_op)
                last_token_type = "operator"
            else:
                # 二元 +/-
                prec_tk = get_precedence(tk)  # 7
                assoc_tk = get_associativity(tk)  # left
                # 弹栈
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
            # 其它运算符: ^, *, /, mod
            # 也可能是我们未列出的东西，自己扩展
            prec_tk = get_precedence(tk)
            if prec_tk is None:
                raise ValueError(f"无法识别的符号: {tk}")
            assoc_tk = get_associativity(tk)

            # 按 Shunting Yard 规则弹栈
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
                    # 左结合：当 top优先级 <= 当前优先级 才弹
                    if top_prec <= prec_tk:
                        pop_condition = True
                else:
                    # 右结合：当 top优先级 < 当前优先级 才弹
                    if top_prec < prec_tk:
                        pop_condition = True

                if pop_condition:
                    output_queue.append(op_stack.pop())
                else:
                    break

            op_stack.append(tk)
            last_token_type = "operator"

    # 6) 遍历结束后，把栈全部弹出
    while op_stack:
        top = op_stack.pop()
        if top == "(" or top == ")":
            raise ValueError("括号不匹配：多出的括号")
        output_queue.append(top)

    return output_queue


# =============== 测试演示 ===============
if __name__ == "__main__":
    test_expressions = [
        # 1) 示例: +3!i^e.%
        #    原始token可能写成 ["+", "3", "!", "i", "^", "e", ".", "%"]
        #    目标:
        #    - 修正 '.' => '0.'
        #    - 在 e 和 '.' 之间插入 '*'
        #    => ["+", "3", "!", "i", "^", "e", "*", "0.", "%"]
        #    再变后缀时区分一元正号 => '(+)'
        ["+", "3", "!", "i", "^", "e", ".", "%"],
        # 2) 括号不匹配且带隐式乘法: "1 + 2 ) 4"
        #    => 补左括号 => "( 1 + 2 ) 4"
        #    => 隐式乘法 => "( 1 + 2 ) * 4"
        #    => 后缀 "1 2 + 4 *"
        ["1", "+", "2", ")", "4"],
        # 3) 一个常见的隐式乘法例子: "2 sin 3" => tokens ["2", "sin", "3"]
        #    => 插入 '*' => ["2", "*", "sin", "3"]
        #    => 后缀 "2 sin 3 *" 但实际上函数要吸收"3" => "2 3 sin *"
        ["2", "sin", "3"],
        # 4) 另一个试验:  ( - x ) ( y + 2 )
        #    => tokens ["(", "-", "x", ")", "(", "y", "+", "2", ")"]
        #    => 相邻 ) ( => 插入 '*' => ["(", "-", "x", ")", "*", "(", "y", "+", "2", ")"]
        ["(", "-", "x", ")", "(", "y", "+", "2", ")"],
        # 5) 测试含小数: "3 . 5" => tokens ["3", ".", "5"]
        #    => '.' -> '0.' => ["3", "0.", "5"]
        #    => 3 与 0. 相邻 => insert "*"； 0. 与 5 相邻 => insert "*"
        #    => => ["3", "*", "0.", "*", "5"]
        ["3", ".", "5"],
        # 6) 更复杂点: "((1)(2))" => tokens ["(", "(", "1", ")", "(", "2", ")", ")"]
        #    里头有相邻 ) ( => insert '*' => => ["(", "(", "1", ")", "*", "(", "2", ")", ")"]
        #    最终表示 ( (1) * (2) ) => 1 2 *
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
