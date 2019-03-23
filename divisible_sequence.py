from collections.abc import Sequence


class DivisibleSequence:
    def __truediv__(self, value):
        return self // int(value)

    def __floordiv__(self: Sequence, value):
        return tuple(
            self.__class__(
                self[int(i/value*len(self)):int((i+1)/value*len(self))]
            ) for i in range(value)
        )

    def __mul__(self: Sequence, value):
        if isinstance(value, int):
            return self.__class__(super().__mul__(value))

        elif isinstance(value, float):
            div, mod = divmod(value, 1)
            return self.__class__(self*int(div) + self[:int(len(self)*mod)])


divisible_subtypes = {}


def divisible(sequence):
    try:
        subtype = divisible_subtypes[sequence.__class__]

    except KeyError:
        subtype = type(
            f'Divisible{sequence.__class__.__name__.title()}',
            (DivisibleSequence, sequence.__class__),
            {}
        )

        divisible_subtypes[sequence.__class__] = subtype

    return subtype(sequence)
