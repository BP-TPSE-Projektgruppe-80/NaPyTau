class Polynomial:
    """
    A class to represent a polynomial.
    A polynomial is a mathematical expression consisting of variables and coefficients.
    """

    coefficients: list[float]
    degree: int

    def __init__(self, coefficients: list[float], degree: int = 2):
        if len(coefficients) != degree + 1:
            raise ValueError(
                "Number of coefficients must match the degree of the polynomial."
            )

        self.coefficients = coefficients
        self.degree = degree

    def get_coefficients(self) -> list[float]:
        return self.coefficients

    def get_degree(self) -> int:
        return self.degree

    def update(self, coefficients: list[float], degree: int = 2) -> None:
        if len(coefficients) != degree + 1:
            raise ValueError(
                "Number of coefficients must match the degree of the polynomial."
            )

        self.coefficients = coefficients
        self.degree = degree
