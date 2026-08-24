import ast
import math
import operator

from langchain_core.tools import tool

from src.core.logger import get_logger
from src.utils.exceptions import ToolExecutionError

logger = get_logger(__name__)

_ALLOWED_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "log": math.log,
    "log10": math.log10,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "floor": math.floor,
    "ceil": math.ceil,
    "min": min,
    "max": max,
}

_ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def _safe_eval(node: ast.AST):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"İzin verilmeyen sabit değer: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINARY_OPS:
            raise ValueError(f"İzin verilmeyen operatör: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_BINARY_OPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPS:
            raise ValueError(f"İzin verilmeyen tekli operatör: {op_type.__name__}")
        return _ALLOWED_UNARY_OPS[op_type](_safe_eval(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
            raise ValueError("İzin verilmeyen fonksiyon çağrısı.")
        args = [_safe_eval(arg) for arg in node.args]
        return _ALLOWED_FUNCTIONS[node.func.id](*args)

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"İzin verilmeyen isim: {node.id}")

    raise ValueError(f"İzin verilmeyen ifade türü: {type(node).__name__}")


@tool("calculator")
def calculator(expression: str) -> str:
    """
    Matematiksel bir ifadeyi güvenli şekilde hesaplar (dört işlem, üs, kök,
    trigonometri, logaritma vb.). eval/exec kullanılmaz.

    Args:
        expression: Hesaplanacak matematiksel ifade, örn. "sqrt(144) + 3 * 2".

    Returns:
        Hesaplama sonucunu içeren metin.
    """
    try:
        logger.info(f"Hesaplama yapılıyor: '{expression}'")
        parsed = ast.parse(expression, mode="eval")
        result = _safe_eval(parsed)
        return f"Sonuç: {result}"
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Hesaplama hatası: {exc}")
        raise ToolExecutionError(f"İfade hesaplanamadı: {exc}") from exc
