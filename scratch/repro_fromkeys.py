from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Iterable, TypeVar, overload

from typing_extensions import Self

_T = TypeVar("_T")
_S = TypeVar("_S")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class MyDict(dict[_KT, _VT]):
    @classmethod
    @overload
    def fromkeys(
        cls, iterable: Iterable[_T], value: None = None
    ) -> "MyDict[_T, Any | None]": ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> "MyDict[_T, _S]": ...
    @classmethod
    def fromkeys(cls: type[Self], iterable: Iterable[Any], value: Any = None) -> Self:
        return super().fromkeys(iterable, value)  # type: ignore[return-value]


class MyOrderedDict(OrderedDict[_KT, _VT]):
    @classmethod
    @overload
    def fromkeys(
        cls, iterable: Iterable[_T], value: None = None
    ) -> "MyOrderedDict[_T, Any | None]": ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> "MyOrderedDict[_T, _S]": ...
    @classmethod
    def fromkeys(cls: type[Self], iterable: Iterable[Any], value: Any = None) -> Self:
        return super().fromkeys(iterable, value)  # type: ignore[return-value]


def test_inference() -> None:
    # Current behavior check
    d = dict.fromkeys([1, 2, 3], "a")
    if TYPE_CHECKING:
        reveal_type(d)

    od = OrderedDict.fromkeys([1, 2, 3], "a")
    if TYPE_CHECKING:
        reveal_type(od)

    md = MyDict.fromkeys([1, 2, 3], "a")
    if TYPE_CHECKING:
        reveal_type(md)

    mod = MyOrderedDict.fromkeys([1, 2, 3], "a")
    if TYPE_CHECKING:
        reveal_type(mod)


if __name__ == "__main__":
    test_inference()
