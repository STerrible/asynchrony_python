from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Simple Calculator API")


@dataclass
class ExpressionState:
    expression: str | None = None


state = ExpressionState()


class BinaryExpressionRequest(BaseModel):
    a: float
    op: Literal["+", "-", "*", "/"]
    b: float


class FullExpressionRequest(BaseModel):
    expression: str = Field(..., min_length=1)


class ValueResponse(BaseModel):
    value: float


class ExpressionResponse(BaseModel):
    expression: str | None


class EvalError(ValueError):
    """Raised when the expression is invalid."""


def _eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise EvalError("Division by zero")
            return left / right

        raise EvalError("Unsupported operator")

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        operand = _eval_ast(node.operand)
        return -operand if isinstance(node.op, ast.USub) else operand

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    raise EvalError("Unsupported syntax in expression")


def evaluate_expression(expression: str) -> float:
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise EvalError("Invalid expression syntax") from exc

    return _eval_ast(parsed.body)


def _binary_operation(a: float, op: str, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise EvalError("Division by zero")
        return a / b
    raise EvalError("Unsupported operator")


@app.get("/")
def root() -> dict[str, Any]:
    return {"message": "Calculator API is running"}


@app.post("/calculate/binary", response_model=ValueResponse)
def calculate_binary(payload: BinaryExpressionRequest) -> ValueResponse:
    try:
        result = _binary_operation(payload.a, payload.op, payload.b)
    except EvalError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    state.expression = f"({payload.a}{payload.op}{payload.b})"
    return ValueResponse(value=result)


@app.post("/expression", response_model=ExpressionResponse)
def set_expression(payload: FullExpressionRequest) -> ExpressionResponse:
    state.expression = payload.expression.strip()
    return ExpressionResponse(expression=state.expression)


@app.get("/expression", response_model=ExpressionResponse)
def get_expression() -> ExpressionResponse:
    return ExpressionResponse(expression=state.expression)


@app.post("/expression/execute", response_model=ValueResponse)
def execute_expression() -> ValueResponse:
    if not state.expression:
        raise HTTPException(status_code=400, detail="Expression is not set")

    try:
        result = evaluate_expression(state.expression)
    except EvalError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ValueResponse(value=result)


@app.post("/calculate/expression", response_model=ValueResponse)
def calculate_expression(payload: FullExpressionRequest) -> ValueResponse:
    expression = payload.expression.strip()
    try:
        result = evaluate_expression(expression)
    except EvalError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    state.expression = expression
    return ValueResponse(value=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)