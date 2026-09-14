"""
Report generation and persistence.
"""

from .config import OUTLIER_ERROR_THRESHOLD, THEORETICAL_G

class ReportGenerator:
    """
    Builds and saves the formatted text report for a PendulumAnalysis result.

    Parameters
    ----------
    analysis: PendulumAnalysis
        The analysis result to report on.
    """

    def __init__(self, analysis):
        self.analysis = analysis

    def generate(self):
        """
        Builds the full report text using f-strings.

        Returns
        -------
        srt
        """
        lines = []
        lines.append("=" * 50)
        lines.append("Report - Gravity measurement with simple pendulum")
        lines.append("=" * 50)
        lines.append(f"Theoretical reference value: {THEORETICAL_G:.2f} m/s²")
        lines.append(f"Outlier error threshold: {OUTLIER_ERROR_THRESHOLD}%")
        lines.append(f"Total valid groups: {len(self.analysis.valid)}")
        lines.append(f"Total excluded groups: (outliers): {len(self.analysis.outliers)}")
        lines.append("")

        lines.append("Results per group (valid):")
        lines.append("-" * 50)
        for m in self.analysis.valid:
            lines.append(
                f"{m.group:<10} g = {m.measured_g:.2f} m/s² "
                f"error = {m.percent_error:.1f}% -> {m.classify_precision()}"
            )

        if self.analysis.outliers:
            lines.append("")
            lines.append(f"Groups excluded as outliers (error > {OUTLIER_ERROR_THRESHOLD:.0f}%):")
            lines.append("-" * 50)
            for m in self.analysis.outliers:
                lines.append(
                    f"{m.group:<10} g = {m.measured_g:.2f} m/s² "
                    f"error = {m.percent_error:.1f}%"
                )

        stats = self.analysis.statistics
        lines.append("")
        lines.append("Overall statistics (valid groups only):")
        lines.append("-" * 50)

        if stats:
            lines.append(f"Mean measured g: {stats['mean_g']:.3f} m/s²")
            lines.append(
                f"Deviation of the mean from the theoretical value: "
                f"{stats['deviation_from_theoretical']:+.3f} m/s²"
            )
            lines.append(
                f"Most precise grouop: {stats['most_precise'].group} "
                f"(error of {stats['most_precise'].percent_error:.1f}%)"
            )
            lines.append(
                f"Least precise grouop: {stats['least_precise'].group} "
                f"(error of {stats['least_precise'].percent_error:.1f}%)"
            )
        else:
            lines.append("No valid measurements to summarize.")

        lines.append("=" * 50)

        return "\n".join(lines)

    def save(self, output_path, text=None):
        """
        Writes the report to a .txt file.

        Parameters
        ----------
        output_path: str
            Destination file path.
        text: str, optional
            Report text to write. If omitted, `generate()` is called.
        """

        if text is None:
            text = self.generate()
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)