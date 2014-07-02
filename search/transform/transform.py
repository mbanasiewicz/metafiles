from scipy import array
from search.matrix_formatter import MatrixFormatter


class Transform:
    def __init__(self, matrix):
        self.matrix = array(matrix, dtype=float)

    def __repr__(self):
        MatrixFormatter(self.matrix).pretty_print
