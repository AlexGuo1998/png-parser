import collections.abc
import typing


# Debug decorator
def monitor_results(func):
    def wrapper(*func_args, **func_kwargs):
        print(f'function call {func.__name__}()')
        retval = func(*func_args, **func_kwargs)
        print('function {func.__name__}() returns {retval!r}')
        return retval
    wrapper.__name__ = func.__name__
    return wrapper


def pixel_type_to_length(color_type: int) -> int:
    if color_type == 0:  # Greyscale
        return 1
    if color_type == 2:  # RGB
        return 3
    if color_type == 3:  # Palette
        return 1
    if color_type == 4:  # Greyscale + alpha
        return 2
    if color_type == 6:  # RGB + Alpha
        return 4

    raise ValueError(f'Invalid color type {color_type}')


class BitArray(collections.abc.Iterable, collections.abc.Sized):
    def __init__(self, bytes_: typing.Union[bytes, bytearray], depth: int = 8):
        # print(f'Create BitArray with {bytes}, {depth}')
        self.bytes = bytes_
        self.depth = depth

        if depth == 16:
            self._iter = self._iter16bits
        elif depth == 8:
            self._iter = self._iter8bits
        elif depth == 4:
            self._iter = self._iter4bits
        elif depth == 2:
            self._iter = self._iter2bits
        elif depth == 1:
            self._iter = self._iter1bit
        else:
            raise ValueError(f'Depth must be 16, 8, 4, 2, 1 not {depth}')

    def _iter16bits(self) -> typing.Iterator[int]:
        it = iter(self.bytes)
        for a, b in zip(it, it):  # 2 bytes in a row
            yield a << 8 | b

    def _iter8bits(self) -> typing.Iterator[int]:
        yield from self.bytes

    def _iter4bits(self) -> typing.Iterator[int]:
        for x in self.bytes:
            yield x >> 4
            yield x & 15

    def _iter2bits(self) -> typing.Iterator[int]:
        for x in self.bytes:
            yield x >> 6
            yield x >> 4 & 3
            yield x >> 2 & 3
            yield x & 3

    def _iter1bit(self) -> typing.Iterator[int]:
        for x in self.bytes:
            yield x >> 7
            yield x >> 6 & 1
            yield x >> 5 & 1
            yield x >> 4 & 1
            yield x >> 3 & 1
            yield x >> 2 & 1
            yield x >> 1 & 1
            yield x & 1

    def __len__(self) -> int:
        return (len(self.bytes) * 8) // self.depth

    def __iter__(self):
        return self._iter()
