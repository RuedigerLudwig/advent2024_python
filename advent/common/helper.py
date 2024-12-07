from typing import Iterable, Iterator


def as_two_tuple[T](
    iterable: Iterable[T], *, default: T | None = None
) -> Iterator[tuple[T, T]]:
    """
    Converts a list of items into a list of tuples of items
    if the number of items odd, the default item is append
    as last item. If no default is given, the last item is dropped
    """
    iterator = iter(iterable)
    while True:
        try:
            first = next(iterator)
        except StopIteration:
            break

        try:
            yield first, next(iterator)
        except StopIteration:
            if default is not None:
                yield first, default
