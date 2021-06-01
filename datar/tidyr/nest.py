"""Nest and unnest

https://github.com/tidyverse/tidyr/blob/master/R/nest.R
"""
from typing import Mapping, Optional, Union, Iterable, List
import re

import pandas
from pandas import DataFrame
from pipda import register_verb

from ..core.utils import vars_select, align_value
from ..core.grouped import DataFrameGroupBy
from ..core.contexts import Context

from ..base import setdiff, intersect
from ..dplyr import distinct, bind_cols, group_vars, group_by_drop_default

from .chop import _vec_split

@register_verb(DataFrame, context=Context.SELECT)
def nest(
        _data: DataFrame,
        _names_sep: Optional[str] = None,
        _base0: Optional[bool] = None,
        **cols: Union[str, int]
) -> DataFrame:
    """Nesting creates a list-column of data frames

    Args:
        _data: A data frame
        **cols: Columns to nest
        _names_sep: If `None`, the default, the names will be left as is.
            Inner names will come from the former outer names
            If a string, the inner and outer names will be used together.
            The names of the new outer columns will be formed by pasting
            together the outer and the inner column names, separated by
            `_names_sep`.
        _base0: Whether `**cols` are 0-based
            if not provided, will use `datar.base.getOption('index.base.0')`

    Returns:
        Nested data frame.
    """
    if not cols:
        raise ValueError("`**cols` must not be empty.")

    all_columns = _data.columns
    colgroups = {}
    usedcols = set()
    for group, columns in cols.items():
        oldcols = all_columns[vars_select(all_columns, columns, base0=_base0)]
        usedcols = usedcols.union(oldcols)
        newcols = (
            oldcols if _names_sep is None else
            _strip_names(oldcols, group, _names_sep)
        )
        colgroups[group] = dict(zip(newcols, oldcols))

    asis = setdiff(_data.columns, usedcols)
    keys = _data[asis]
    u_keys = distinct(keys)

    nested = []
    for group, columns in colgroups.items():
        if _names_sep is None: # names as is
            # out <- map(cols, ~ vec_split(.data[.x], keys)$val)
            val = _vec_split(_data[list(columns)], keys).val
        else:
            # out <- map(
            #   cols,
            #   ~ vec_split(set_names(.data[.x], names(.x)), keys)$val
            # )
            to_split = _data[list(columns.values())]
            to_split.columns = list(columns)
            val = _vec_split(to_split, keys).val

        nested.append(val)

    out = pandas.concat(nested, ignore_index=True, axis=1)
    out.columns = list(colgroups)
    if u_keys.shape[1] == 0:
        return out if isinstance(out, DataFrame) else out.to_frame()
    return bind_cols(u_keys, align_value(out, u_keys))

@nest.register(DataFrameGroupBy, context=Context.SELECT)
def _(
        _data: DataFrameGroupBy,
        _names_sep: Optional[str] = None,
        _base0: Optional[bool] = None,
        **cols: Mapping[str, Union[str, int]]
) -> DataFrameGroupBy:
    """Nesting grouped dataframe"""
    if not cols:
        cols = {'data': setdiff(_data.columns, group_vars(_data))}
    out = nest.dispatch(DataFrame)(
        _data, **cols, _names_sep=_names_sep, _base0=_base0
    )
    gvars = intersect(out.columns, group_vars(_data))
    return _data.__class__(
        out,
        _group_vars=gvars,
        _drop=group_by_drop_default(_data)
    )

# @register_verb(DataFrame, context=Context.SELECT)
# def unnest(
#         data: DataFrame,
#         *cols: Union[str, int],
#         keep_empty: bool = False,
#         dtypes: Optional[Union[DTypeType, Mapping[str, DTypeType]]] = None,
#         names_sep: Optional[str] = None,
#         names_repair: Union[str, Callable] = 'check_unique',
#         _base0: Optional[bool] = None
# ) -> DataFrame:
#     """Flattens list-column of data frames back out into regular columns.

#     Args:
#         data: A data frame to flatten.
#         *cols: Columns to unnest.
#         keep_empty: By default, you get one row of output for each element
#             of the list your unchopping/unnesting.
#             This means that if there's a size-0 element
#             (like NULL or an empty data frame), that entire row will be
#             dropped from the output.
#             If you want to preserve all rows, use `keep_empty` = `True` to
#             replace size-0 elements with a single row of missing values.
#         dtypes: NOT `ptype`. Providing the dtypes for the output columns.
#             Could be a single dtype, which will be applied to all columns, or
#             a dictionary of dtypes with keys for the columns and values the
#             dtypes.
#         names_sep: If `None`, the default, the names will be left as is.
#             Inner names will come from the former outer names
#             If a string, the inner and outer names will be used together.
#             The names of the new outer columns will be formed by pasting
#             together the outer and the inner column names, separated by
#             `names_sep`.
#         names_repair: treatment of problematic column names:
#             - "minimal": No name repair or checks, beyond basic existence,
#             - "unique": Make sure names are unique and not empty,
#             - "check_unique": (default value), no name repair,
#                 but check they are unique,
#             - "universal": Make the names unique and syntactic
#             - a function: apply custom name repair
#         _base0: Whether `cols` are 0-based
#             if not provided, will use `datar.base.getOption('index.base.0')`

#     Returns:
#         Data frame with selected columns unnested.
#     """
#     if not cols:
#         raise ValueError("`*cols` is required when using unnest().")

#     all_columns = data.columns
#     cols = vars_select(all_columns, cols, base0=_base0)
#     cols = all_columns[cols]

#     out = {}
#     for col in cols:
#         out[col] = _as_df(data[col])

#     out = unchop(
#         data, cols,
#         keep_empty=keep_empty, dtypes=dtypes, _base0=_base0
#     )
#     return unpack(
#         data, cols,
#         names_sep=names_sep, names_repair=names_repair
#     )

def _strip_names(names: Iterable[str], base: str, sep: str) -> List[str]:
    """Strip the base names with sep"""
    out = []
    for name in names:
        if not sep:
            out.append(name[len(base):] if name.startswith(base) else name)
        else:
            parts = re.split(re.escape(sep), name, maxsplit=1)
            out.append(parts[1] if parts[0] == base else name)
    return out

# def _as_df(*args, **kwargs): ...
# def unpack(*args, **kwargs): ...
