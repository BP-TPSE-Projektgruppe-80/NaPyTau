from dataclasses import dataclass


@dataclass
class Polynomial:
    """
    A class to represent a polynomial.
    A polynomial is a mathematical expression consisting of variables and coefficients.
    """

    coefficients: list[float]

    def get_coefficients(self) -> list[float]:
        return self.coefficients

    def set_coefficients(self, coefficients: list[float]) -> None:
        self.coefficients = coefficients
