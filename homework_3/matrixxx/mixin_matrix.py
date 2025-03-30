from numpy.lib.mixins import NDArrayOperatorsMixin
from collections.abc import Iterable
from copy import deepcopy


class NumpyNDArrayOperatorsMixin(NDArrayOperatorsMixin):
    """Mixin for numpy-style array operators"""

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """We need define this function for correct inheritance
        https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html"""
        out = kwargs.get("out", ())

        # Defer to the implementation of the ufunc
        # on unwrapped values.
        inputs = tuple(x.data if isinstance(x, Matrix) else x for x in inputs)
        if out:
            kwargs["out"] = tuple(x.data if isinstance(x, Matrix) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == "at":
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)


class FileIOMixin:
    """Mixin for formatted file output operations"""

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            col_widths = [
                max(len(str(row[i])) for row in self.data) for i in range(self.cols)
            ]

            for row in self.data:
                formatted_row = "  ".join(
                    f"{str(item):>{width}}" for item, width in zip(row, col_widths)
                )
                f.write(formatted_row + "\n")


class DisplayMixin:
    """Mixin for readable representations"""

    def __str__(self):
        matrix_representation = []
        col_widths = [
            max(len(str(row[i])) for row in self.data) for i in range(self.cols)
        ]

        for row in self.data:
            formatted_row = "  ".join(
                f"{str(item):>{width}}" for item, width in zip(row, col_widths)
            )
            matrix_representation.append(formatted_row)

        return "\n".join(matrix_representation) + "\n"


class PropertyMixin:
    """Mixin for data validation and shape properties"""

    @property
    def data(self):
        return deepcopy(self._data)

    @data.setter
    def data(self, value):
        # dummy validation
        if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
            raise ValueError(
                "Input must be an iterable structure, but not string or bytes"
            )

        processed_data = [list(row) for row in value]

        if not processed_data or not processed_data[0]:
            raise ValueError("Matrix must have at least one row and one column")

        if any(len(row) != len(processed_data[0]) for row in processed_data):
            raise ValueError("All rows must have the same length")

        self._data = processed_data

    @property
    def rows(self):
        return len(self._data)

    @property
    def cols(self):
        return len(self._data[0])


class Matrix(NumpyNDArrayOperatorsMixin, FileIOMixin, DisplayMixin, PropertyMixin):
    """Core matrix class combining all mixins"""

    def __init__(self, data):
        self.data = data
