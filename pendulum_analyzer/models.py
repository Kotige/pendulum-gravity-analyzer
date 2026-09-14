"""
Data model for a single group's pendulum measurement.
"""

class Measurement:
    """
    Represents one group's gravitational acceleration measurement.

    Parameters
    ----------
    group: srt
        Name/identifier of the group that collected the measurement.
    measured_g: float
        Measured gravitational acceleration, in m/s^2.
    percent_error: float
        Percent error relative to the theoretical reference value.
    """

    def __init__(self, group, measured_g, percent_error):
        self.group = group
        self.measured_g = measured_g
        self.percent_error = percent_error

    def classify_precision(self):
        """
        Classifies the measurement's precision based on its percent error.

        Returns
        -------
        str
            "Excellent", "Good" or "Needs review".
        """
        if self.percent_error < 2:
            return "Excellent"
        elif self.percent_error <=5:
            return "Good"
        return "Needs review"

    def __repr__(self):
        return(
            f"Measurement(group={self.group!r}, measured_g={self.measured_g:.2f}, "
            f"percent_error={self.percent_error:.1f}%)"
        )
