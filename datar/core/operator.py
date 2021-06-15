"""Operators for datar"""
from typing import Any, Optional, Tuple
from functools import partial
import operator

import numpy
from pandas import Series
from pipda import register_operator, Operator
from pipda.context import ContextBase

from .utils import length_of, recycle_value
from .collections import Collection, Inverted, Negated, Intersect
from .exceptions import DataUnrecyclable
from .types import BoolOrIter

@register_operator
class DatarOperator(Operator):
    """Operator class for datar"""

    def _arithmetize1(self, operand: Any, op: str) -> Any:
        """Operator for single operand"""
        op_func = getattr(operator, op)
        # Data length might be changed after evaluation
        # operand = recycle_value(operand, self.data.shape[0])
        return op_func(operand)

    def _arithmetize2(self, left: Any, right: Any, op: str) -> Any:
        """Operator for paired operands"""
        op_func = getattr(operator, op)
        left, right = _recycle_left_right(left, right)
        return op_func(left, right)

    def invert(self, operand: Any, _context: Optional[ContextBase]) -> Any:
        """Interpretation for ~x"""
        if isinstance(operand, (slice, str, list, tuple, Collection)):
            return Inverted(operand)
        return self._arithmetize1(operand, 'invert')

    def neg(self, operand: Any) -> Any:
        """Interpretation for -x"""
        if isinstance(operand, (slice, list)):
            return Negated(operand)
        return self._arithmetize1(operand, 'neg')

    def and_(self, left: Any, right: Any) -> Any:
        """Mimic the & operator in R.

        This has to have Expression objects to be involved to work

        Args:
            left: Left operand
            right: Right operand

        Returns:
            The intersect of the columns
        """
        if isinstance(left, list):
            # induce an intersect with Collection
            return Intersect(left, right)

        left, right = _recycle_left_right(left, right)
        left = Series(left).fillna(False)
        right = Series(right).fillna(False)
        return left & right

    def or_(self, left: Any, right: Any) -> Any:
        """Mimic the & operator in R.

        This has to have Expression objects to be involved to work

        Args:
            left: Left operand
            right: Right operand

        Returns:
            The intersect of the columns
        """
        if isinstance(left, list):
            return Collection(left, right)

        left, right = _recycle_left_right(left, right)
        left = Series(left).fillna(False)
        right = Series(right).fillna(False)
        return left | right

    # pylint: disable=invalid-name
    def ne(self, left: Any, right: Any) -> BoolOrIter:
        """Interpret for left != right"""
        out = self.eq(left, right)
        if isinstance(out, (numpy.ndarray, Series)):
            neout = ~out
            # neout[pandas.isna(out)] = numpy.nan
            return neout
        return not out

    def __getattr__(self, name: str) -> Any:
        """Other operators"""
        if not hasattr(operator, name):
            raise AttributeError
        attr = partial(self._arithmetize2, op=name)
        attr.__qualname__ = self._arithmetize2.__qualname__
        return attr

def _recycle_left_right(left: Any, right: Any) -> Tuple:
    """Recycle left right operands to each other"""
    try:
        left = recycle_value(left, length_of(right))
    except DataUnrecyclable:
        right = recycle_value(right, length_of(left))
    return left, right
