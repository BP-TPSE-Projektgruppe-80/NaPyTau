import numpy.linalg.lstsq
import numpy.poly1d


def get_sum_of_distances(distances: list[float], power: int) -> float:
    sum_total: float = 0
    for i in range(len(distances) - 1):
        sum_total += distances[i] ** power
    return sum_total


def get_sum_of_intensities(doppler_shifted_intensities: list[float],
                           distances: list[float], power: int) -> float:
    sum_total: float = 0
    for i in range(len(distances) - 1):
        sum_total += (distances[i] ** power) * doppler_shifted_intensities[i]
    return sum_total


def determine_coefficients(doppler_shifted_intensities: list[float],
                           distances: list[float]) -> [float, float, float]:
    distances_matrix: [float][float] = \
        [[get_sum_of_distances(distances, 4),
          get_sum_of_distances(distances, 3),
          get_sum_of_distances(distances, 2)],
         [get_sum_of_distances(distances, 3),
          get_sum_of_distances(distances, 2),
          get_sum_of_distances(distances, 1)],
         [get_sum_of_distances(distances, 2),
          get_sum_of_distances(distances, 1),
          len(distances)]]

    intensities_matrix: [float][float] = \
        [[get_sum_of_intensities(doppler_shifted_intensities,
                                 distances, 2)],
         [get_sum_of_intensities(doppler_shifted_intensities,
                                 distances, 1)],
         [get_sum_of_intensities(doppler_shifted_intensities,
                                 distances, 0)]]

    # coefficients
    a: float = 0
    b: float = 0
    c: float = 0
    coefficients, residuals, rank, s = numpy.linalg.lstsq(distances_matrix,
                                                          intensities_matrix,
                                                          rcond=None)
    a, b, c = coefficients
    return a, b, c


def get_polynomial(a: float, b: float, c: float) -> poly1d:
    return poly1d([a, b, c])