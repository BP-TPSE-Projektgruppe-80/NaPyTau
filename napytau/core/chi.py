def get_second_order_polynomial() -> int:
    return 2

def get_statistical_error() -> float:
    return 1

def calculate_chi(doppler_shifted_intensities: list[float]) -> float:
    sum_total: float = 0
    for i in range(len(doppler_shifted_intensities) - 1):
        sum_total += ((doppler_shifted_intensities[i]
                       - get_second_order_polynomial())
                       / get_statistical_error()) ** 2
    return sum_total