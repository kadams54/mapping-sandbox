from functools import reduce
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


def pipeline(
    initial: T,
    funcs: list[Callable[..., T]],
    curried_args: Optional[list[Any]] = None,
    curried_kwargs: Optional[dict[str, Any]] = None,
) -> T:
    args: list[Any] = curried_args or []
    kwargs: dict[str, Any] = curried_kwargs or {}
    return reduce(lambda out, f: f(out, *args, **kwargs), funcs, initial)
