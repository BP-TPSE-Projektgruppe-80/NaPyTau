from dataclasses import dataclass


@dataclass
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

    def set_coefficients(self, coefficients: list[float]) -> None:
        self.coefficients = coefficients
        self.degree = degree
