from collections.abc import Iterable
from copy import deepcopy


class HashMixin:
    """Mixin for hash and eq implementation."""
    def __hash__(self):
        """Returns the sum of the matrix elements as a hash"""
        return int(sum(sum(row) for row in self._data))


    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return bool(self._data == other._data)


class Matrix(HashMixin):
    _cache = {}

    def __init__(self, data):
        # dummy validation
        if not isinstance(data, Iterable) or isinstance(data, (str, bytes)):
            raise ValueError(
                "Input must be an iterable structure, but not string or bytes"
            )

        processed_data = [list(row) for row in data]

        if not processed_data or not processed_data[0]:
            raise ValueError("Matrix must have at least one row and one column")

        cols = len(processed_data[0])
        if any(len(row) != cols for row in processed_data):
            raise ValueError("All rows must have the same length")

        self._data = processed_data
        self.rows = len(processed_data)
        self.cols = cols

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Addition allowed only between two Matrix objects")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")

        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]

        return self.__class__(result)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Multiplication allowed only between two Matrix objects")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrices must have the same dimensions for component-wise multiplication"
            )

        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]

        return self.__class__(result)

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError(
                "Matrix multiplication allowed only between two Matrix objects"
            )
        if self.cols != other.rows:
            raise ValueError(
                "Number of columns in first matrix must equal number of rows in second matrix"
            )

        result = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]

        # Add caching by (hash(m1), hash(m2))
        self.__class__._cache[(hash(self), hash(other))] = result

        return self.__class__(result)

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

    @property
    def data(self):
        return deepcopy(self._data)
