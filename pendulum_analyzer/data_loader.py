"""
CSV loading and validation for pendulum measurements.
"""

import csv

from .models import Measurement

class DataLoader:
    """
    Loads and validates pendulum measurement data from a CSV file.

    Parameters
    ----------
    file_path: str
        Path to the CSV file with columns: group, measured_g, percent_error
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        """
        Reads the CSV file and returns a list of valid Measurement objects.
        
        Rows with invalid or missing values are skipped, with a warning printed to the console.
        Returns an empty list if the file is not found.

        Returns
        -------
        list[Measurements]
        """

        measurements = []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                #starts at 2 since line 1 is the header
                for line_number, row in enumerate(reader, start=2):
                    try:
                        measurements.append(self._parse_row(row))
                    except ValueError as error:
                        print(f"Warning: line {line_number} skipped due to invalid data: {error}")
        except FileNotFoundError:
            print(f"Error: file '{self.file_path}' not found.")
            return []
        return measurements

    @staticmethod
    def _parse_row(row):
        """
        Parses and validates a single CSV row into a Measurement.

        Raises
        -----
        ValueError
            If a required field is missing, non-numeric, or measured_g is not positive.
        """ 

        group = row["group"].strip()
        measured_g = float(row["measured_g"])
        percent_error = float(row["percent_error"])

        if measured_g <= 0:
            raise ValueError("measured_g must be positive")

        return Measurement(group, measured_g, percent_error)