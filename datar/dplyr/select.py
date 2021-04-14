"""Subset columns using their names and types

See source https://github.com/tidyverse/dplyr/blob/master/R/select.R
"""
from typing import Any, Iterable, List, Mapping, Tuple, Union

from pandas import DataFrame, Index
from pipda import register_verb

from ..core.contexts import Context
from ..core.types import StringOrIter
from ..core.utils import vars_select, logger
from ..core.middlewares import Inverted
from ..core.grouped import DataFrameGroupBy
from ..core.exceptions import ColumnNotExistingError
from ..base.funcs import setdiff, union
from .group_by import group_by_drop_default
from .group_data import group_data, group_vars

@register_verb(DataFrame, context=Context.SELECT)
def select(
        _data: DataFrame,
        *args: Union[StringOrIter, Inverted],
        **kwargs: Mapping[str, str]
) -> DataFrame:
    """Select (and optionally rename) variables in a data frame

    Args:
        *columns: The columns to select
        **renamings: The columns to rename and select in new => old column way.

    Returns:
        The dataframe with select columns
    """
    all_columns = _data.columns
    gvars = group_vars(_data)
    selected, new_names = eval_select(
        all_columns,
        *args,
        **kwargs,
        _group_vars=gvars
    )
    out = _data.iloc[:, selected].copy()

    if new_names:
        out.rename(columns=new_names, inplace=True)

    if isinstance(_data, DataFrameGroupBy):
        gvars = [new_names.get(gvar, gvar) for gvar in gvars]
        gdata = group_data(_data)
        gdata.columns = gvars + ['_rows']
        return DataFrameGroupBy(
            out,
            _group_vars=gvars,
            _drop=group_by_drop_default(_data),
            _group_data=gdata
        )
    return out

def eval_select(
        _all_columns: Index,
        *args: Any,
        _group_vars: Iterable[str],
        **kwargs: Any
) -> Tuple[List[int], Mapping[str, str]]:
    """Evaluate selections to get locations

    Returns:
        A tuple of (selected columns, dict of old-to-new renaming columns)
    """
    selected = vars_select(_all_columns, *args, *kwargs.values())
    missing = setdiff(_group_vars, _all_columns[selected])
    if missing:
        logger.info(
            "Adding missing grouping variables: %s",
            missing
        )

    selected = union(_all_columns.get_indexer_for(_group_vars), selected)

    # dplyr takes new -> old
    # we transform it to old -> new for better access
    new_names = {}
    for key, val in kwargs.items():
        # key: new name
        # val: old name
        if isinstance(val, str):
            idx = _all_columns.get_indexer_for([val])
            if len(idx) > 1:
                raise ValueError(
                    'Names must be unique. '
                    f'Name "{val}" found at locations {list(idx)}.'
                )
        else: # int
            try:
                val = _all_columns[val]
            except IndexError:
                raise ColumnNotExistingError(
                    f'Location {val} does not exist.'
                ) from None
        new_names[val] = key
    return selected, new_names