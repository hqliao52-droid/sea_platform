import re
import time
from typing import List, Tuple, Optional, Dict, Any
from pylatexenc.latexwalker import LatexWalker
from functools import wraps
from loguru import logger

# KaTeX 已知不支持的 LaTeX 命令（部分列举）
KATEX_UNSUPPORTED = {
    r"\begin{alignat}",
    r"\begin{alignedat}",
    r"\begin{matrix*}[r]",  # 某些矩阵变体
    r"\cancel",
    r"\bcancel",
    r"\xcancel",  # 需要 cancel 包
    r"\colorbox",
    r"\fcolorbox",  # 需要 xcolor 包
    r"\underbrace",
    r"\overbrace",  # 支持但可能样式不同
    r"\boldsymbol",  # 可用 \mathbf 或 \bm（需bm包）
    # 更多可自行扩展
}

# 实际上 KaTeX 支持大部分 amsmath，但有些宏包不支持，检查是否使用了这些宏包命令
KATEX_UNSAFE_PACKAGES = {"mathtools", "cancel", "xcolor", "bm", "tikz"}

# 将文本中直接出现的（如：α、β...）等符号，转为对应的 LaTeX 命令
UNICODE_SYMBOLS = {
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "ε": r"\varepsilon",
    "θ": r"\theta",
    "π": r"\pi",
    "σ": r"\sigma",
    "τ": r"\tau",
    "φ": r"\phi",
    "ω": r"\omega",
    "Δ": r"\Delta",
    "Θ": r"\Theta",
    "Π": r"\Pi",
    "Σ": r"\Sigma",
    "Φ": r"\Phi",
    "Ψ": r"\Psi",
    "Ω": r"\Omega",
    "°": r"^{\circ}",
    "∠": r"\angle",
    "⊥": r"\perp",
    "∥": r"\parallel",
    "≅": r"\cong",
    "≈": r"\approx",
    "≠": r"\neq",
    "≤": r"\leq",
    "≥": r"\geq",
    "×": r"\times",
    "÷": r"\div",
    "±": r"\pm",
    "∓": r"\mp",
    "∞": r"\infty",
    "∂": r"\partial",
    "∇": r"\nabla",
    "∑": r"\sum",
    "∏": r"\prod",
    "∫": r"\int",
    "√": r"\sqrt",
    "△": r"\triangle",
    "⇒": r"\Rightarrow",
}

# 将裸英文单词映射为带反斜杠的 LaTeX 命令（包括希腊字母和常用数学函数,如 alpha、beta）->（如 \alpha、\beta）
GLATEX_ALIAS_MAP = {
    # 希腊字母小写
    "alpha": r"\alpha",
    "beta": r"\beta",
    "gamma": r"\gamma",
    "delta": r"\delta",
    "epsilon": r"\epsilon",
    "varepsilon": r"\varepsilon",
    "zeta": r"\zeta",
    "eta": r"\eta",
    "theta": r"\theta",
    "vartheta": r"\vartheta",
    "iota": r"\iota",
    "kappa": r"\kappa",
    "lambda": r"\lambda",
    "mu": r"\mu",
    "nu": r"\nu",
    "xi": r"\xi",
    # omicron 通常直接用 o，此处不映射
    "pi": r"\pi",
    "varpi": r"\varpi",
    "rho": r"\rho",
    "varrho": r"\varrho",
    "sigma": r"\sigma",
    "varsigma": r"\varsigma",
    "tau": r"\tau",
    "upsilon": r"\upsilon",
    "phi": r"\phi",
    "varphi": r"\varphi",
    "chi": r"\chi",
    "psi": r"\psi",
    "omega": r"\omega",
    # 希腊字母大写（仅标准 LaTeX 命令存在的大写）
    "Gamma": r"\Gamma",
    "Delta": r"\Delta",
    "Theta": r"\Theta",
    "Lambda": r"\Lambda",
    "Xi": r"\Xi",
    "Pi": r"\Pi",
    "Sigma": r"\Sigma",
    "Upsilon": r"\Upsilon",
    "Phi": r"\Phi",
    "Psi": r"\Psi",
    "Omega": r"\Omega",
    # 常见数学函数/运算符
    "div": r"\div",
    "sin": r"\sin",
    "cos": r"\cos",
    "tan": r"\tan",
    "cot": r"\cot",
    "sec": r"\sec",
    "csc": r"\csc",
    "arcsin": r"\arcsin",
    "arccos": r"\arccos",
    "arctan": r"\arctan",
    "sinh": r"\sinh",
    "cosh": r"\cosh",
    "tanh": r"\tanh",
    "coth": r"\coth",
    "log": r"\log",
    "ln": r"\ln",
    "lg": r"\lg",
    "exp": r"\exp",
    "max": r"\max",
    "min": r"\min",
    "gcd": r"\gcd",
    "lcm": r"\lcm",
    "deg": r"\deg",
    "arg": r"\arg",
    "det": r"\det",
    "lim": r"\lim",
    "sup": r"\sup",
    "inf": r"\inf",
}

# 映射LLM输出中常见的因手误产生的表达式错误（误伤可能性：极低；只在 fix_latex_content 中使用）
TYPO_MAP = {
    r"\\begine": r"\\begin",
    r"\\ende": r"\\end",
    r"\\fracc": r"\\frac",
    r"\\sqrtt": r"\\sqrt",
    r"\\sumn": r"\\sum",
    r"\\intt": r"\\int",
    r"\\limitt": r"\\limit",
    r"\\textt": r"\\text",
    r"\\mathrrm": r"\\mathrm",
    r"\\mathbff": r"\\mathbf",
    r"\\mathcall": r"\\mathcal",
    r"\\ngle": r"\\angle",
}

# 在 auto_wrap_bare_latex 函数中使用：扫描非数学模式中的命令，根据上下文决定是否在两侧添加 $ 定界符，确保命令能被 katex 成功渲染
# 误伤可能性：极低；
# 原因：
# 1、它只匹配反斜杠开头的命令（如 \frac、\sin），不会匹配普通英文单词。
# 2、只在非数学区域自动包裹，已有的 $...$ 内部的命令不会被重复包裹。
# 3、典型 LLM 输出中，\frac、\sin 这类字符串出现在普通文本里几乎都是为了表达数学，加 $ 正是我们期望的修复。
COMPLEX_CMD_PATTERN = (
    r"\\(?:"
    + "|".join(
        [
            # 常用数学命令
            "frac",
            "sqrt",
            "sum",
            "int",
            "lim",
            "log",
            "sin",
            "cos",
            "tan",
            "cot",
            "sec",
            "csc",
            "arcsin",
            "arccos",
            "arctan",
            "sinh",
            "cosh",
            "tanh",
            "coth",
            "max",
            "min",
            "sup",
            "inf",
            "prod",
            "coprod",
            "because",
            # 希腊字母
            "alpha",
            "beta",
            "gamma",
            "theta",
            "pi",
            "eta",
            # 集合与运算符
            "bigcup",
            "bigcap",
            "bigvee",
            "bigwedge",
            "bigoplus",
            "bigotimes",
            "bigodot",
            "triangle",
            "therefore",
            # 箭头
            "Rightarrow",
            "Leftarrow",
            "Leftrightarrow",
            "rightarrow",
            "leftarrow",
            "leftrightarrow",
            "longrightarrow",
            "longleftarrow",
            "longleftrightarrow",
            "xrightarrow",
            "xleftarrow",
            "overrightarrow",
            "overleftarrow",
            "underrightarrow",
            "underleftarrow",
            # 关系符
            "le",
            "ge",
            "ll",
            "gg",
            "neq",
            "equiv",
            "approx",
            "sim",
            "cong",
            "propto",
            "parallel",
            "perp",
            "models",
            # 括号和装饰
            "binom",
            "choose",
            "atop",
            "stackrel",
            "overset",
            "underset",
            "widehat",
            "widetilde",
            "overline",
            "underline",
            "overbrace",
            "underbrace",
            # 特殊符号
            "pm",
            "mp",
            "times",
            "div",
            "cdot",
            "circ",
            "degree",
            "angle",
            "infty",
            "nabla",
            "partial",
            "forall",
            "exists",
            "emptyset",
            "Re",
            "Im",
            "ImaginaryPart",
            "RealPart",
            # 文本
            "text",
        ]
    )
    + r")\b"
)


#  工具函数（耗时测试）
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        if isinstance(result, dict):
            result["elapsed_time_ms"] = elapsed * 1000
        print(f"⏱️ {func.__name__} 耗时: {elapsed:.4f}s")
        return result

    return wrapper


def apply_greek_replacements(latex_str: str) -> Tuple[str, bool]:
    """
    在数学模式内将希腊字母英文单词替换为相应的 LaTeX 命令; eg: alpha -> \alpha
    返回 (替换后的字符串, 是否发生替换)
    """
    # 严格按单词长度降序，保证先匹配长单词
    sorted_keys = sorted(GLATEX_ALIAS_MAP.keys(), key=len, reverse=True)
    pattern = r"(?<!\\)(" + "|".join(re.escape(k) for k in sorted_keys) + r")\b"

    def repl(match):
        word = match.group(1)
        return GLATEX_ALIAS_MAP[word]

    fixed = re.sub(pattern, repl, latex_str)
    replaced = fixed != latex_str
    return fixed, replaced


#  清理与规范化
def clean_llm_artifacts(text: str) -> str:
    """移除 LLM 常见的非 LaTeX 污染（安全模式）"""

    escapes_fix = {
        "\triangle": r"\triangle",
        "\times": r"\times",
        "\text": r"\text",
        "\therefore": r"\therefore",
        "\theta": r"\theta",
        "\tan": r"\tan",
        "\x08ecause": r"\because",
        "\x08eta": r"\beta",
        "\x07ngle": r"\angle",
        "\x07lpha": r"\alpha",
        "\x0crac": r"\frac",
    }
    for k, v in escapes_fix.items():
        text = text.replace(k, v)

    # 针对大模型输出丢失斜杠（少斜杠）的常见符号进行补全
    math_keywords = [
        "triangle",
        "angle",
        "circ",
        "times",
        "perp",
        "cdot",
        "equiv",
        "simeq",
        "le",
        "ge",
        "neq",
        "approx",
    ]
    for w in math_keywords:
        text = re.sub(r"(?<![\\a-zA-Z])" + w + r"(?![a-zA-Z])", "\\\\" + w, text)

    # 移除常见的 HTML 标签（白名单，避免误删 <...> 占位符）
    safe_html_pattern = r"</?(?:p|br|div|span|img|a|b|i|em|strong|h[1-6]|ul|ol|li|table|tr|td|th|code|pre)\b[^>]*>"
    text = re.sub(safe_html_pattern, "", text, flags=re.IGNORECASE)

    # 不删除 Markdown 代码块标记，保留原始格式
    # text = re.sub(r'```[a-zA-Z]*\s*', '', text)
    # text = re.sub(r'```\s*', '', text)

    # 全角转半角（仅标点符号）
    full_to_half = str.maketrans(
        {
            "（": "(",
            "）": ")",
            "【": "[",
            "】": "]",
            "；": ";",
            "：": ":",
            "！": "!",
            "？": "?",
            "，": ",",
            "。": ".",
            "、": ",",
            "＝": "=",
            "＋": "+",
            "－": "-",
            "＊": "*",
            "／": "/",
            "＜": "<",
            "＞": ">",
            "～": "~",
        }
    )
    text = text.translate(full_to_half)
    # 清理零宽字符
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # 合并多余空格
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    # Unicode 符号转 LaTeX
    for uni, latex_cmd in UNICODE_SYMBOLS.items():
        text = text.replace(uni, latex_cmd)

    return text


def normalize_delimiters(text: str) -> str:
    """统一各类 LaTeX 定界符为 $...$ 和 $$...$$"""
    # 块级
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)
    text = re.sub(
        r"\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}",
        r"$$\1$$",
        text,
        flags=re.DOTALL,
    )
    # 行内
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)
    return text


#  公式提取
def extract_command_with_args(text: str, pos: int) -> Tuple[str, int]:
    """
    从 pos 位置开始提取一个 LaTeX 命令及其所有参数
    返回 (命令内容, 结束位置)
    """
    # 匹配 \command
    cmd_match = re.match(r"\\([a-zA-Z]+)", text[pos:])
    if not cmd_match:
        return "", pos

    end = pos + cmd_match.end()

    # 循环提取花括号参数
    while end < len(text) and text[end] == "{":
        brace_count = 1
        end_brace = end + 1
        while end_brace < len(text) and brace_count > 0:
            if text[end_brace] == "{":
                brace_count += 1
            elif text[end_brace] == "}":
                brace_count -= 1
            end_brace += 1
        end = end_brace

    # 也支持可选参数 [option]
    while end < len(text) and text[end] == "[":
        bracket_count = 1
        end_bracket = end + 1
        while end_bracket < len(text) and bracket_count > 0:
            if text[end_bracket] == "[":
                bracket_count += 1
            elif text[end_bracket] == "]":
                bracket_count -= 1
            end_bracket += 1
        end = end_bracket

    return text[pos:end], end


def extract_latex_formulas(text: str) -> List[Tuple[str, str, str, int, int]]:
    """
    提取公式，返回 [(内容, 完整匹配, 类型, start, end), ...]
    """
    # 先找到所有未转义的 $
    dollar_positions = [m.start() for m in re.finditer(r"(?<!\\)\$", text)]

    # 如果 $ 数量为奇数，尝试配对
    if len(dollar_positions) % 2 == 1:
        # 找到孤立的 $（没有配对的）
        # 检查每个 $ 后面是否紧跟数学内容（数字、字母或 \ 开头的命令）
        for pos in dollar_positions:
            # 检查这个 $ 是否已经有配对
            # 简单策略：从 pos+1 开始找下一个 $
            next_dollar = text.find("$", pos + 1)
            if next_dollar != -1:
                # 如果有下一个 $，检查它们之间是否有合理的数学内容
                between = text[pos + 1 : next_dollar]
                # 如果中间包含数字、字母或反斜杠，说明是合法的公式
                if re.search(r"[a-zA-Z0-9\\]", between):
                    continue  # 已经有配对，跳过

            # 找到孤立的 $
            after = text[pos + 1 :]

            # 检查 $ 后面是否紧跟数学内容
            if after and after[0] not in [" ", "\n", "\t", "\r"]:
                # 找到这个公式的结束位置
                # 策略：从 pos+1 开始，找到第一个分隔符（空格、换行、中文标点等）
                end_pos = pos + 1
                while end_pos < len(text):
                    char = text[end_pos]
                    # 如果是空格、换行、中文标点，停止
                    if char in [
                        " ",
                        "\n",
                        "\t",
                        "\r",
                        "，",
                        "。",
                        "、",
                        "；",
                        "：",
                        "！",
                        "？",
                    ]:
                        break
                    # 如果是中文汉字，也停止
                    if "\u4e00" <= char <= "\u9fff":
                        break
                    end_pos += 1

                # 如果找到了结束位置，插入配对的 $
                if end_pos > pos + 1:
                    text = text[:end_pos] + "$" + text[end_pos:]
                    break  # 修复后跳出循环

    # 再次规范化定界符
    text = normalize_delimiters(text)
    formulas = []
    matched_spans = []

    # 块级公式 $$
    for match in re.finditer(r"\$\$(.*?)\$\$", text, re.DOTALL):
        content = match.group(1).strip()
        if content:
            formulas.append((content, match.group(0), "display_dollar", *match.span()))
            matched_spans.append(match.span())

    # 行内公式：成对匹配
    # 使用更宽松的模式匹配 $...$
    inline_pattern = r"(?<!\\)\$(?!\s)(.+?)(?<!\\)\$"
    for match in re.finditer(inline_pattern, text, re.DOTALL):
        start, end = match.span()
        # 检查是否与块级公式重叠
        if any(s <= start < e or s < end <= e for s, e in matched_spans):
            continue
        content = match.group(1).strip()
        # 跳过纯数字（单独的数字可能不是公式）
        if re.match(r"^[\d.,]+$", content):
            continue
        formulas.append((content, match.group(0), "inline_dollar", start, end))
        matched_spans.append((start, end))

    formulas.sort(key=lambda x: x[3])
    return formulas


def fix_isolated_dollar_signs(text: str) -> str:
    """修复孤立的 $ 符号，防止跨越中文字符错误配对"""
    dollar_matches = list(re.finditer(r"(?<!\\)\$", text))
    if not dollar_matches:
        return text

    # 将相邻的 $ 合并为 $$ token
    tokens = []
    i = 0
    while i < len(dollar_matches):
        start = dollar_matches[i].start()
        if i + 1 < len(dollar_matches) and dollar_matches[i + 1].start() == start + 1:
            tokens.append(
                {"type": "$$", "start": start, "end": dollar_matches[i + 1].end()}
            )
            i += 2
        else:
            tokens.append({"type": "$", "start": start, "end": dollar_matches[i].end()})
            i += 1

    stack = []
    inserts = []

    def get_math_end(pos):
        """从给定的 pos 位置向后探测，找到合理的数学表达式边界"""
        end_pos = pos
        while end_pos < len(text):
            ch = text[end_pos]
            if ch == "\\":
                # 如果遇到反斜杠，说明是 LaTeX 命令，跳过命令主体及其后的花括号/方括号参数
                end_pos += 1
                while end_pos < len(text) and text[end_pos].isalpha():
                    end_pos += 1
                # 跳过可选参数 [...]
                if end_pos < len(text) and text[end_pos] == "[":
                    bracket_count = 1
                    end_pos += 1
                    while end_pos < len(text) and bracket_count > 0:
                        if text[end_pos] == "[":
                            bracket_count += 1
                        elif text[end_pos] == "]":
                            bracket_count -= 1
                        end_pos += 1
                # 跳过必选参数 {...}
                while end_pos < len(text) and text[end_pos] == "{":
                    brace_count = 1
                    end_pos += 1
                    while end_pos < len(text) and brace_count > 0:
                        if text[end_pos] == "{":
                            brace_count += 1
                        elif text[end_pos] == "}":
                            brace_count -= 1
                        end_pos += 1
                continue
            elif ch.isdigit() or ch.isalpha() or ch in "+-*/=<>()[]^{}_|.'":
                # 常规数学字符，继续向后探索
                end_pos += 1
            else:
                # 遇到空格、中文或其他标点，视为公式结束
                break
        return end_pos

    for token in tokens:
        if not stack:
            stack.append(token)
            continue

        top = stack[-1]
        # 当遇到同类型的 token，准备进行配对闭合
        if top["type"] == token["type"]:
            if top["type"] == "$":
                between = text[top["end"] : token["start"]]
                # --- 新增：跨中文防误判逻辑 ---
                # 如果成对的 $ 之间存在中文字符（且不是包在 \text{} 里的），
                # 说明这两者大概率属于不同短语里的独立变量，不应被强制配对成一个大公式。
                # 例："延长 $AE 交 $BC" -> 这里 $ 应该被视为独立的缺失定界符的节点。
                if re.search(r"[\u4e00-\u9fff]", between) and "\\text" not in between:
                    math_end = get_math_end(top["end"])
                    if math_end > top["end"]:
                        inserts.append((math_end, "$"))  # 原地修复栈顶的独立 $
                    stack.pop()
                    stack.append(token)  # 将当前无法配对的 $ 作为新的起点入栈
                    continue
            stack.pop()  # 配对成功，出栈
        else:
            # 升级修复：比如栈顶是 $$，当前是 $，则给当前补齐成 $$
            if top["type"] == "$$" and token["type"] == "$":
                inserts.append((token["end"], "$"))
                stack.pop()
            elif top["type"] == "$" and token["type"] == "$$":
                inserts.append((top["start"], "$"))
                stack.pop()
            else:
                stack.append(token)

    # 遍历栈中剩余的未闭合 token，利用 get_math_end 原地补齐
    for token in stack:
        if token["type"] == "$$":
            inserts.append((token["end"], "$$"))
        else:
            math_end = get_math_end(token["end"])
            if math_end > token["end"]:
                inserts.append((math_end, "$"))

    # 从后往前插入，防止前面的插入操作改变后续字符的索引偏移量
    inserts.sort(key=lambda x: x[0], reverse=True)
    for pos, ins in inserts:
        text = text[:pos] + ins + text[pos:]

    return text


#  语法校验
def validate_latex_syntax(latex_str: str) -> Tuple[bool, Optional[str]]:
    """使用 pylatexenc 校验语法，同时检查是否包含危险命令"""
    if not latex_str.strip():
        return False, "空公式"
    try:
        LatexWalker(latex_str).get_latex_nodes()
        return True, None
    except Exception as e:
        return False, str(e)


def is_katex_compatible(latex_str: str) -> Tuple[bool, List[str]]:
    warnings = []
    for cmd in KATEX_UNSUPPORTED:
        # 转义命令中的反斜杠等特殊字符，再添加单词边界
        pattern = re.escape(cmd) + r"\b"
        if re.search(pattern, latex_str):
            warnings.append(f"可能使用了KaTeX不支持的命令: {cmd}")
    # 其他检查保持不变
    if re.search(r"\\usepackage\s*\{", latex_str):
        warnings.append("公式中不应包含 \\usepackage 命令")
    if re.search(r"\\input\s*\{", latex_str) or re.search(r"\\include\s*\{", latex_str):
        warnings.append("检测到危险命令（input/include），已阻止")
        return False, warnings
    return True, warnings


#  智能修复（分等级）
def fix_latex_content(
    content: str, repair_level: str = "conservative"
) -> Tuple[str, List[str]]:
    """
    修复公式，返回 (修复后内容, 修复日志)
    repair_level: 'conservative' | 'moderate' | 'aggressive'
    """
    original = content
    fixed = content
    logs = []

    for old, new in TYPO_MAP.items():
        if old in fixed:
            fixed = re.sub(old, new, fixed)
            logs.append(f"拼写修正: {old} -> {new}")

    # 修正全角反斜杠
    fixed = fixed.replace("＼", "\\").replace("¥", "\\")

    # 括号平衡（不改变内容，仅补全/删除多余的）
    open_braces = fixed.count("{")
    close_braces = fixed.count("}")
    if close_braces > open_braces:
        # 删除末尾多余的右括号
        while close_braces > open_braces and fixed.endswith("}"):
            fixed = fixed[:-1]
            close_braces -= 1
            logs.append("移除多余的右括号 }")
    elif open_braces > close_braces:
        # 补全右括号（在末尾）
        fixed += "}" * (open_braces - close_braces)
        logs.append(f"补全 {open_braces - close_braces} 个右括号")

    # 方括号平衡
    open_brack = fixed.count("[")
    close_brack = fixed.count("]")
    if open_brack > close_brack:
        fixed += "]" * (open_brack - close_brack)
        logs.append(f"补全 {open_brack - close_brack} 个 ]")

    #  2. 中度修复（moderate / aggressive）
    if repair_level in ("moderate", "aggressive"):
        # 处理常见的不规范命令（保留语义但转为文本）
        # 例如：\quadrilateral -> \text{quadrilateral}（不改变含义）
        unknown_cmds = re.findall(r"\\([a-zA-Z]+)(?![a-zA-Z])", fixed)
        for cmd in unknown_cmds:
            # 如果该命令不在 LaTeX 常用命令列表中（此处用白名单简化）
            # 实际上我们只替换那些明显是英文单词且不是标准命令的
            if cmd not in {
                "frac",
                "sqrt",
                "sum",
                "int",
                "lim",
                "log",
                "sin",
                "cos",
                "tan",
                "text",
                "mathrm",
                "mathbf",
                "mathcal",
                "boldsymbol",
                "begin",
                "end",
                "left",
                "right",
                "big",
                "Big",
                "bigg",
                "Bigg",
                "qquad",
                "quad",
                "hspace",
                "vspace",
            }:
                # 替换为 \text{cmd}
                old_pattern = r"\\" + cmd + r"\b"
                new_text = r"\\text{" + cmd + r"}"
                fixed = re.sub(old_pattern, new_text, fixed)
                logs.append(f"未知命令 \\{cmd} -> \\text{{{cmd}}}（保留语义）")

        # 修复明显的 \xrightarrow 等，如果缺失参数则补
        fixed = re.sub(r"\\xrightarrow\s*\{", r"\\xrightarrow{}", fixed)  # 确保有参数

    #  3. 激进修复（aggressive）
    if repair_level == "aggressive":
        # 尝试转换一些非标准符号为 KaTeX 支持的等价物（可能改变语义，慎用）
        # 例如：\Delta 保持不变，但 \varDelta 可能不支持，转换为 \Delta
        # 这里不列举，因为容易改变语义，故默认不开启
        pass

    # 最后，如果修复后内容为空，则返回原内容并警告
    if not fixed.strip():
        fixed = original
        logs.append("修复导致内容为空，保留原始内容")

    return fixed, logs


def auto_wrap_bare_latex(text: str) -> str:
    """自动探测未被 $ 包裹的 LaTeX 公式主体，向左右延展后将其包裹（针对 case9）"""
    math_spans = []

    # 记录已经包裹在 $$...$$ 内的区间
    for match in re.finditer(r"\$\$(.*?)\$\$", text, re.DOTALL):
        math_spans.append(match.span())

    occupied = [False] * len(text)
    for s, e in math_spans:
        for i in range(s, e):
            occupied[i] = True

    # 记录已经包裹在 $...$ 内的区间
    dollar_positions = [m.start() for m in re.finditer(r"(?<!\\)\$", text)]
    i = 0
    while i < len(dollar_positions) - 1:
        start = dollar_positions[i]
        end = dollar_positions[i + 1]
        if not occupied[start] and not occupied[end]:
            if "$" not in text[start + 1 : end]:
                math_spans.append((start, end + 1))
        i += 2

    # 区间合并去重
    math_spans.sort()
    merged = []
    for s, e in math_spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))

    def is_in_math(pos):
        """检查特定位置是否已经处于已被 $ 包裹的公式内部"""
        return any(s <= pos < e for s, e in merged)

    def get_wrap_type(s, e):
        """判断需要包裹的类型：左右都需要补，还是只需补左/补右"""
        has_left = s > 0 and text[s - 1] == "$"
        has_right = e < len(text) and text[e] == "$"
        if has_left and has_right:
            return "none"
        elif has_left and not has_right:
            return "wrap_right"
        elif not has_left and has_right:
            return "wrap_left"
        else:
            return "wrap_both"

    def _expand_math_span(txt, l, r):
        """
        当探测到 \frac 时，前面的 a_{n+1} = 也应该属于公式。
        以探测到的命令为基准，向左/右吞噬相关的数学符号和变量，直到遇到中文或无关英文单词停下。
        """
        # 向左拓展
        while l > 0:
            c = txt[l - 1]
            if c in " \t_{}[]()=+-*/<>,.!|\\'\"":  # 允许的数学与标点符号
                l -= 1
            elif c.isdigit():
                l -= 1
            elif c.isalpha():
                # 若遇到字母，回溯确认整个单词
                word_start = l - 1
                while word_start > 0 and txt[word_start - 1].isalpha():
                    word_start -= 1
                word = txt[word_start:l]
                # 排除普通的英文长单词（非 LaTeX 命令）以防止将整句英文文本吞噬进公式
                if (
                    len(word) >= 3
                    and not word.isupper()
                    and not (word_start > 0 and txt[word_start - 1] == "\\")
                ):
                    break
                l = word_start
            else:
                break  # 遇到中文或其他不可延展字符时阻断

        # 向右拓展（逻辑与向左类似）
        while r < len(txt):
            c = txt[r]
            if c in " \t_{}[]()=+-*/<>,.!|\\'\"":
                r += 1
            elif c.isdigit():
                r += 1
            elif c.isalpha():
                word_end = r + 1
                while word_end < len(txt) and txt[word_end].isalpha():
                    word_end += 1
                word = txt[r:word_end]
                if (
                    len(word) >= 3
                    and not word.isupper()
                    and not (r > 0 and txt[r - 1] == "\\")
                ):
                    break
                r = word_end
            else:
                break

        # 收缩两端多余的空格，保证美观
        while l < r and txt[l].isspace():
            l += 1
        while r > l and txt[r - 1].isspace():
            r -= 1
        return l, r

    matches = []
    # 扫描文本，寻找孤立的复合并未被包裹的命令（如 \frac, \triangle）
    for match in re.finditer(COMPLEX_CMD_PATTERN, text):
        start = match.start()
        end = match.end()

        # 将命令后附带的括号参数 [xxx] 和 {xxx} 纳入基准范围
        pos = end
        while pos < len(text) and text[pos] == "[":
            bracket_count = 1
            pos += 1
            while pos < len(text) and bracket_count > 0:
                if text[pos] == "[":
                    bracket_count += 1
                elif text[pos] == "]":
                    bracket_count -= 1
                pos += 1
        while pos < len(text) and text[pos] == "{":
            brace_count = 1
            pos += 1
            while pos < len(text) and brace_count > 0:
                if text[pos] == "{":
                    brace_count += 1
                elif text[pos] == "}":
                    brace_count -= 1
                pos += 1

        # 执行新增的双向延展，捕获公式全貌
        start, pos = _expand_math_span(text, start, pos)

        # 如果延展后的区间本身已经在合法的 $$ 内了，则跳过
        if is_in_math(start):
            continue

        wrap_type = get_wrap_type(start, pos)
        if wrap_type != "none":
            matches.append((start, pos, wrap_type))

    # 若多次延展产生相互重叠的区间，进行融合，以免在公式中间硬插入 $ 破坏结构
    merged_matches = []
    for start, end, wtype in sorted(matches):
        if merged_matches and start < merged_matches[-1][1]:
            merged_matches[-1] = (
                merged_matches[-1][0],
                max(merged_matches[-1][1], end),
                merged_matches[-1][2],
            )
        else:
            merged_matches.append((start, end, wtype))

    # 逆序应用补全操作，避免由于字符串长度改变带来的索引越界
    for start, end, wtype in reversed(merged_matches):
        token = text[start:end]
        if "$" not in token:
            if wtype == "wrap_both":
                text = text[:start] + f"${token}$" + text[end:]
            elif wtype == "wrap_left":
                text = text[:start] + f"${token}" + text[end:]
            elif wtype == "wrap_right":
                text = text[:start] + f"{token}$" + text[end:]

    return text


# @timer_decorator
def validate_and_repair_llm_latex(
    text: str,
    auto_repair: bool = True,
    repair_level: str = "conservative",
    strict_mode: bool = False,
) -> Dict[str, Any]:
    """
    综合校验并修复 LLM 输出的 LaTeX
    Args:
        text: 原始文本
        auto_repair: 是否自动修复
        repair_level: 'conservative' | 'moderate' | 'aggressive' -> 保守/适中/激进
        strict_mode: 若为 True，则任何未修复的公式都视为错误
    """
    result = {
        "has_formula": False,
        "formula_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "repaired_count": 0,
        "pass_rate": 1.0,
        "is_valid": True,
        "repaired_text": text,
        "details": [],
        "errors": [],
        "warnings": [],
        "original_text": text,
        "repair_logs": [],
    }

    # 1. 清理
    cleaned = clean_llm_artifacts(text)
    cleaned = fix_isolated_dollar_signs(cleaned)
    cleaned = normalize_delimiters(cleaned)  # 提前统一
    cleaned = auto_wrap_bare_latex(cleaned)  # 现在只处理 $ 和 $$
    result["cleaned_text"] = cleaned
    if not cleaned.strip():
        result["warnings"].append("清理后文本为空")
        return result

    # 2. 提取公式
    formulas = extract_latex_formulas(cleaned)
    if not formulas:
        result["warnings"].append("未检测到 LaTeX 公式")
        return result

    result["has_formula"] = True
    result["formula_count"] = len(formulas)

    # 3. 逐个处理
    repaired_parts = []
    last_idx = 0

    for content, full_match, ftype, start, end in formulas:
        content, greek_replaced = apply_greek_replacements(content)
        if greek_replaced:
            result["repair_logs"].append("公式中希腊字母英文已修复")
        is_valid = False
        was_repaired = False
        repaired_content = content
        error_msg = None
        warnings = []

        # 安全检测（危险命令）
        if re.search(r"\\input\s*\{|\\include\s*\{|\\write\s*\{", content):
            result["errors"].append(f"公式包含危险命令，已跳过: {content[:50]}")
            if strict_mode:
                result["invalid_count"] += 1
                # 不添加到修复文本，继续
                continue

        # 语法校验
        valid_syntax, syntax_err = validate_latex_syntax(content)
        # KaTeX 兼容性检查
        katex_ok, katex_warns = is_katex_compatible(content)
        if katex_warns:
            warnings.extend(katex_warns)

        # 决策
        if valid_syntax and katex_ok:
            is_valid = True
        else:
            # 尝试修复
            if auto_repair:
                fixed_content, logs = fix_latex_content(content, repair_level)
                if logs:
                    result["repair_logs"].extend(logs)
                # 重新验证修复后
                valid_syntax2, _ = validate_latex_syntax(fixed_content)
                katex_ok2, katex_warns2 = is_katex_compatible(fixed_content)
                if valid_syntax2 and katex_ok2:
                    is_valid = True
                    was_repaired = True
                    repaired_content = fixed_content
                    warnings.extend(katex_warns2)
                else:
                    # 修复失败
                    if strict_mode:
                        is_valid = False
                        error_msg = f"修复后仍不兼容: {syntax_err or 'KaTeX不兼容'}"
                    else:
                        # 即使不兼容，我们仍使用原内容，但标记为不合法
                        is_valid = False
                        error_msg = f"无法修复: {syntax_err or 'KaTeX不兼容'}"
            else:
                # 不自动修复
                is_valid = False
                error_msg = (
                    f"语法错误: {syntax_err}" if not valid_syntax else "KaTeX不兼容"
                )

        # 记录详情
        detail = {
            "original": content,
            "repaired": repaired_content,
            "type": ftype,
            "is_valid": is_valid,
            "was_repaired": was_repaired,
            "error": error_msg,
            "warnings": warnings,
        }
        result["details"].append(detail)

        # 拼接修复后的文本
        repaired_parts.append(cleaned[last_idx:start])
        if ftype == "display_dollar":
            new_match = f"$${repaired_content}$$"
        else:  # inline_dollar
            new_match = f"${repaired_content}$"
        repaired_parts.append(new_match)
        last_idx = end

        # 统计
        if is_valid:
            result["valid_count"] += 1
            if was_repaired:
                result["repaired_count"] += 1
        else:
            result["invalid_count"] += 1
            if error_msg:
                result["errors"].append(f"公式 '{content[:30]}...' 错误: {error_msg}")

    # 补全尾部
    repaired_parts.append(cleaned[last_idx:])
    result["repaired_text"] = "".join(repaired_parts)

    # 最终统计
    result["pass_rate"] = (
        result["valid_count"] / result["formula_count"]
        if result["formula_count"] > 0
        else 1.0
    )
    result["is_valid"] = result["invalid_count"] == 0

    return result


def repair_latex(text: str, auto_repair=True, repair_level="moderate") -> str:
    """对大模型输出包含 latex 表达式的自然语言进行修复

    args:
        text (str): 待修复/核验的 latex 文本
    """
    try:
        res = validate_and_repair_llm_latex(
            text, auto_repair=auto_repair, repair_level=repair_level
        )
        return res["repaired_text"]
    except Exception as e:
        logger.warning(f"修复 latex 表达式失败: {e}")
        return text


#  测试
if __name__ == "__main__":
    # # 版本：1.1
    # # 通过的测试

    # # case1(原本正确的输入  得到  正确的输出):
    case1 = "证明：\n1. 将 $\\triangle ABE$ 绕点 $A$ 逆时针旋转 $90^\\circ$ 得到 $\\triangle ADG$，则 $\\triangle ABE \\\\cong \\\\triangle ADG$。\n   由此可得：$AE = AG$，$BE = DG$，$\\angle BAE = \\angle DAG$，$\\angle ADG = \\angle B = 90^\\circ$。\n2. 因为四边形 $ABCD$ 是正方形，所以 $\\angle ADC = 90^\\circ$。\n   所以 $\\angle FDG = \\angle ADC + \\angle ADG = 90^\\circ + 90^\\circ = 180^\\circ$，即点 $F, D, G$ 共线。\n3. 因为 $\\angle BAD = 90^\\circ$，$\\angle EAF = 45^\\circ$，\n   所以 $\\angle BAE + \\angle DAF = 90^\\circ - 45^\\circ = 45^\\circ$。\n   所以 $\\angle GAF = \\angle DAG + \\angle DAF = \\angle BAE + \\angle DAF = 45^\\circ$。\n   即 $\\angle EAF = \\angle GAF$。\n4. 在 $\\triangle AEF$ 和 $\\triangle AGF$ 中，\n   $$ \\\\begin{cases} AE = AG \\\\ \\angle EAF = \\angle GAF \\\\ AF = AF \\end{cases} $$\n   所以 $\\triangle AEF \\\\cong \\\\triangle AGF$ (SAS)。\n   所以 $EF = GF$。\n5. 因为 $GF = GD + DF = BE + DF$，\n   所以 $EF = BE + DF$。\n6. $\\triangle CEF$ 的周长 $= CE + CF + EF$\n   $= CE + CF + BE + DF$\n   $= (CE + BE) + (CF + DF)$\n   $= BC + CD$\n   $= a + a$\n   $= 2a$。\n从而得证。"

    # # case2（原本正确的输入  得到  正确的输出）:
    case2 = "解：\n1. 由题意知 $\\frac{1}{5} \u003c \\frac{a}{b} \u003c \\frac{1}{4}$，即 $0.2b \u003c a \u003c 0.25b$。且 $b \\le 19$，$\\frac{a}{b}$ 为最简分数。\n2. 遍历 $b$ 从 1 到 19 的整数，寻找满足条件的整数 $a$：\n   - 当 $b=9$ 时，$1.8 \u003c a \u003c 2.25$，得 $a=2$，$\\frac{2}{9}$ 是最简分数，$a+b=11$；\n   - 当 $b=13$ 时，$2.6 \u003c a \u003c 3.25$，得 $a=3$，$\\frac{3}{13}$ 是最简分数，$a+b=16$；\n   - 当 $b=14$ 时，$2.8 \u003c a \u003c 3.5$，得 $a=3$，$\\frac{3}{14}$ 是最简分数，$a+b=17$；\n   - 当 $b=17$ 时，$3.4 \u003c a \u003c 4.25$，得 $a=4$，$\\frac{4}{17}$ 是最简分数，$a+b=21$；\n   - 当 $b=18$ 时，$3.6 \u003c a \u003c 4.5$，得 $a=4$，但 $\\frac{4}{18}=\\frac{2}{9}$ 不是最简分数，舍去；\n   - 当 $b=19$ 时，$3.8 \u003c a \u003c 4.75$，得 $a=4$，$\\frac{4}{19}$ 是最简分数，$a+b=23$。\n   其余 $b$ 值均无满足条件的整数 $a$ 或所得分数非最简。\n3. 比较上述结果，$a+b$ 的最大值为 23，最小值为 11。\n4. 计算积：$23 \\times 11 = 253$。\n答：$a+b$ 的最大可能值与最小可能值之积为 253。"

    # # case3（缺失的$符号  得到  正确的输出）:
    case3 = "第1空：3\\frac{1}{2}\n第2空：50\n第3空：1\n第4空：2\n第5空：0.5"

    # # case4(原本正确的输入  得到  正确的输出):
    case4 = "证明：\n1. 在$BD$上截取$BF=AD$，连接$AF$。\n2. $\\because \\triangle ABC$是等边三角形，\n   $\\therefore AB=AC$，$\\angle BAC=60^\\circ$。\n   由作图及旋转性质可知 $\\triangle ABF \\cong \\triangle ACD$（需先证共线或利用角度推导，此处采用更严谨的角度推导路径）。\n   \n   **修正推导路径以符合标准书写逻辑：**\n   \n   证明：\n   1. $\\because \\triangle ABC$是等边三角形，\n      $\\therefore AB=AC$，$\\angle BAC=\\angle ACB=60^\\circ$。\n   2. $\\because \\angle ADB=60^\\circ$，\n      $\\therefore \\angle ADB=\\angle ACB$。\n      $\\therefore A, B, C, D$ 四点共圆。\n   3. $\\therefore \\angle ABD=\\angle ACD$（同弧$AD$所对的圆周角相等）。\n   4. 在$BD$上截取$BF=CD$，连接$AF$。\n      在$\\triangle ABF$和$\\triangle ACD$中，\n      $$ \\begin{cases} AB=AC \\\\ \\angle ABF=\\angle ACD \\\\ BF=CD \\end{cases} $$\n      $\\therefore \\triangle ABF \\cong \\triangle ACD$ (SAS)。\n   5. $\\therefore AF=AD$，$\\angle BAF=\\angle CAD$。\n   6. $\\therefore \\angle FAD = \\angle FAB + \\angle BAD = \\angle CAD + \\angle BAD = \\angle BAC = 60^\\circ$。\n   7. $\\because AF=AD$ 且 $\\angle FAD=60^\\circ$，\n      $\\therefore \\triangle ADF$ 是等边三角形。\n   8. $\\therefore DF=AD$。\n   9. $\\because BD = BF + DF$，\n      且 $BF=CD$，$DF=AD$，\n      $\\therefore BD = CD + AD$。\n从而得证。"

    # # case5(缺失$  得到  正确的输出):
    case5 = "解:\n1. 延长 $AE 交 $BC$ 的延长线于点 $F$.\n2. $\\because AD \\parallel BC$,$\\therefore \\angle D = \\angle ECF$,$\\angle DAE = \\angle F$.\n 又 $\\because E$ 是 $CD$ 的中点,$\\therefore DE = CE$.\n 在 $\\triangle ADE$ 和 $\\triangle FCE$ 中,\n $$\\begin{cases} \\angle D = \\angle ECF \\ \\ngle DAE = \\angle F \\ DE = CE \\end{cases}$$\n $\\therefore \\triangle ADE \\cong \\triangle FCE (AAS)$.\n $\\therefore S_{\\triangle ADE} = S_{\\triangle FCE}$,且 $AE = EF$.\n3. $\\because AE = 5$,$\\therefore AF = AE + EF = 10$.\n $\\because AB \\perp AE$,$\\therefore \\angle BAF = 90^\\circ$.\n $\\therefore S_{\\text{四边形}ABCD} = S_{\\triangle ABF} = \\frac{1}{2} AB \\cdot AF = \\frac{1}{2} \\times 4 \\times 10 = 20$.\n答:四边形 $ABCD$ 的面积为 20."

    # # case6(没有斜杠的希腊字符表):
    case6 = "这是$alpha$，这是$beta$,这是$eta$"

    # # case7(含有html和md格式的文本):
    case7 = "这是xxx题目的答案，<p>latex公式：$$(y + 20x) - (y + 15x) = 100 - 90$$</p> \n```text$$ \\text{抽水机数量} \\times \\text{时间} = y + x \\times \\text{时间} $```"

    # # case8(少斜杠)
    case8 = "题目考查平行四边形的性质、勾股定理及面积计算。解题思路如下：\n1. **分析几何关系**：在平行四边形ABCD中，已知$AC \\perp BC$，说明$\triangle ABC$是一个直角三角形，且$angle ACB = 90^circ$。\n2. **计算直角边AC**：在Rt$\triangle ABC$中，斜边$AB=10$，直角边$BC=6$。根据勾股定理 $AC^2 + BC^2 = AB^2$，可得 $AC = \\sqrt{AB^2 - BC^2} = \\sqrt{10^2 - 6^2} = \\sqrt{100 - 36} = \\sqrt{64} = 8$。\n3. **计算面积**：平行四边形的面积公式为“底 $\times$ 高”。若以$BC$为底，由于$AC \\perp BC$，则$AC$即为该底边上的高。因此，面积 $S = BC \times AC = 6 \times 8 = 48$。\n\n学生提交的“图片1: 题干”仅包含题目描述，并未给出具体的数值答案，属于未作答或无效作答，故判定为错误。"

    # # case9
    case9 = "(I) a_{n+1} = \\frac{a_n + 1}{3a_n}"

    case10 = "第1空：$3\\frac{1}{2}\n第2空：50\n第3空：1\n第4空：2\n第5空：0.5"

    test_list = []
    test_list.append(case1)
    test_list.append(case2)
    test_list.append(case3)
    test_list.append(case4)
    test_list.append(case5)
    test_list.append(case6)
    test_list.append(case7)
    test_list.append(case8)
    test_list.append(case9)
    test_list.append(case10)
    for i, test in enumerate(test_list):
        # if i == 7:
        res = validate_and_repair_llm_latex(
            test, auto_repair=True, repair_level="moderate"
        )
        print(f"这是case{i + 1}:\n", repr(res["repaired_text"]))
        print(
            "========================================================================\n"
        )
