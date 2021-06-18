"""Public APIs from this submodule"""
# pylint: disable=unused-import,redefined-builtin
from .constants import (
    pi, Inf, letters, LETTERS, month_abb, month_name
)
from ..core.options import options, getOption, options_context
from .verbs import (
    colnames, rownames, dim, nrow, ncol, diag, t, names,
    intersect, union, setdiff, setequal, duplicated, cov
)
from .funs import (
    cut, identity, expandgrid, data_context
)
from .arithmetic import (
    sum, mean, median, min, max, pmin, pmax, var,
    abs, ceiling, floor, round, sqrt,
)
from .bessel import bessel_i, bessel_j, bessel_k, bessel_y
from .casting import as_integer, as_double, as_int, as_numeric
from .complex import re, im, is_complex, as_complex
from .cum import cumsum, cumprod, cummin, cummax
from .date import as_date
from .factor import (
    factor, droplevels, levels,
    is_factor, is_categorical, as_factor, as_categorical
)
from .logical import (
    TRUE, FALSE,
    is_true, is_false,
    is_bool, is_logical,
    as_bool, as_logical
)
from .na import NA, NaN, is_na, any_na
from .null import NULL, is_null, as_null
from .random import set_seed
from .seq import (
    c, seq, seq_len, seq_along, rev, rep, lengths, unique, sample, length
)

from .special import (
    beta, lbeta, gamma, lgamma, digamma, trigamma, psigamma,
    choose, lchoose, factorial, lfactorial
)
from .string import (
    is_str, is_string, is_character, as_str, as_string, as_character
)
from .table import table
from .testing import (
    is_double, is_float, is_int, is_integer, is_numeric,
    is_atomic, is_element, is_in, all, any
)
from .trig_hb import (
    cos, sin, tan, acos, asin, atan, atan2, cospi, sinpi, tanpi,
    cosh, sinh, tanh, acosh, asinh, atanh
)
from .which import which, which_min, which_max
