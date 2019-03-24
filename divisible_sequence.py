from typing import TypeVar, Union, Generic
SequenceType = TypeVar('SequenceType')


class Divisible(Generic[SequenceType]):
    def __truediv__(self: SequenceType, value) -> SequenceType:
        return self // int(value)

    def __floordiv__(self: SequenceType, value):
        return tuple(
            self.__class__(
                self[int(i/value*len(self)):int((i+1)/value*len(self))]
            ) for i in range(value)
        )

    def __mul__(self: SequenceType, value) -> Union['Divisible[SequenceType]', SequenceType]:
        if isinstance(value, int):
            return self.__class__(super().__mul__(value))

        elif isinstance(value, float):
            div, mod = divmod(value, 1)
            return self.__class__(self*int(div) + self[:int(len(self)*mod)])


divisible_subtypes = {}


def divisible(sequence: SequenceType) -> Union[SequenceType, Divisible]:
    try:
        subtype = divisible_subtypes[sequence.__class__]

    except KeyError:
        subtype = type(
            f'Divisible{sequence.__class__.__name__.title()}',
            (Divisible, sequence.__class__),
            {}
        )

        divisible_subtypes[sequence.__class__] = subtype

    return subtype(sequence)
