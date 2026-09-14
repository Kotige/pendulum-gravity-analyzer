"""
Statistical Analysis of pendulum measurements.
"""

from .config import OUTLIER_ERROR_THRESHOLD, THEORETICAL_G

class PendulumAnalysis:
    """
    Separates outliers and computes summary statistics for a set of measurements.

    Parameters
    ----------
    measurements: list[Measurements]
        All measurements loaded from the data source.
    threshold: float, opitional
        Percent error above witch a measurement is treated as an outlier.
        Defaults to config.OUTLIER_ERROR_THRESHOLD.

    Attributes
    ----------
    valid: list[Measurement]
        Measurements within the error threshold.
    outliers: list[Measurement]
        Measurements above the error threshold.
    statistics: dict
        Summary statistics computed over `valid` (empty dict if there are no valid measurements).
    """

    def __init__(self, measurements, threshold=OUTLIER_ERROR_THRESHOLD):
        self.threshold = threshold
        self.valid, self.outliers = self._separate_outliers(measurements)
        self.statistics = self._calculate_statistics(self.valid)

    def _separate_outliers(self, measurements):
        valid = [m for m in measurements if m.percent_error <= self.threshold]
        outliers = [m for m in measurements if m.percent_error > self.threshold]
        return valid, outliers

    @staticmethod
    def _calculate_statistics(valid_measurements):
        if not valid_measurements:
            return {}

        g_values = [m.measured_g for m in valid_measurements]
        mean_g = sum(g_values) / len(g_values)
        deviation_from_theoretical = mean_g - THEORETICAL_G

        most_precise = min(valid_measurements, key=lambda m: m.percent_error)
        least_precise = max(valid_measurements, key=lambda m: m.percent_error)

        return {
            "mean_g": mean_g,
            "deviation_from_theoretical": deviation_from_theoretical,
            "most_precise": most_precise,
            "least_precise": least_precise
        }