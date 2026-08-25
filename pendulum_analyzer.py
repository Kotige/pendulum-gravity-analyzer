"""
Pendulum Gravity Analyzer

Reads gravitational acceleration (g) measurements collected by students using a simple pendulum
experiment, calculates statistics, classifies each group's precision, flgas outliers and generates
a formatted .txt report.
"""

import csv

THEORETICAL_G = 9.78 # Local reference value for gravitational acceleration (m/s²) in Juiz de Fora, Brazil.
OUTLIER_ERROR_THRESHOLD = 10.0 # Percent error above this value is treated as an outlier and excluded from statistics.

def read_data(file_path): 
    """
    Reads the CSV file with columns: group, measured_g, percent_error.
    Return a list of dictionaries, one per group.
    Rows with invalid or missing values are skipped, with a warning printed to the console.
    """

    data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for line_number, row in enumerate(reader, start=2): #starts at 2 since line 1 is the header
                try:
                    group = row['group'].strip()
                    measured_g = float(row['measured_g'])
                    percent_error = float(row['percent_error'])

                    if measured_g <= 0:
                        raise ValueError("measured_g must be positive")
                    data.append({
                        "group": group,
                        "measured_g": measured_g,
                        "percent_error": percent_error
                    })
                except ValueError as error:
                    print(f"Warning: line {line_number} skipped due to invalid data: {error}")
    except FileNotFoundError:
                    print(f"Error: file '{file_path}' not found.")
                    return []
    return data

def separate_outliers(data, threshold=OUTLIER_ERROR_THRESHOLD):
    """
    Splits the data into two groups: valid (percent_error <= threshold)
    and outliers (percent_error > threshold).
    """
    valid = [item for item in data if item['percent_error'] <= threshold]
    outliers = [item for item in data if item['percent_error'] > threshold]
    return valid, outliers

def calculate_statistics(data):
    """
    Calculates statistics for the valid data points.
    Returns a dictionary with the calculated statistics.
    """
    if not data:
        return {}

    g_values = [item['measured_g'] for item in data]
    mean_g = sum(g_values) / len(g_values)
    deviation_from_theoretical = mean_g - THEORETICAL_G

    most_precise_group = min(data, key=lambda item: item['percent_error'])
    least_precise_group = max(data, key=lambda item: item['percent_error'])

    return {
        "mean_g": mean_g,
        "deviation_from_theoretical": deviation_from_theoretical,
        "most_precise_group": most_precise_group,
        "least_precise_group": least_precise_group
    }

def classify_precision(percent_error):
    """
    Classifies the measurement based on the given percent error.
    """

    if percent_error < 2:
        return "Excellent"
    elif percent_error <= 5:
        return "Good"
    else:
        return "Needs review"

def generate_report(data, outliers, statistics):
    """
    Builds the full report text using f-strings.
    """

    lines = []
    lines.append("=" *50)
    lines.append("Report - Gravity measurement with simple pendulum")
    lines.append("=" *50)
    lines.append(f"Theoretical reference value: {THEORETICAL_G:.2f} m/s²")
    lines.append(f"Outlier error threshold: {OUTLIER_ERROR_THRESHOLD:.0f}%")
    lines.append(f"Total valid groups: {len(data)}")
    lines.append(f"Total excluded groups (outliers): {len(outliers)}")
    lines.append("")

    lines.append("Results per group (valid):")
    lines.append("-" *50)
    for item in data:
        classification = classify_precision(item["percent_error"])
        lines.append(
            f"{item['group']:<10} g = {item['measured_g']:.2f} m/s²"
            f"error = {item['percent_error']:.1f}% -> {classification}"
        )

    if outliers:
        lines.append("")
        lines.append(f"Groups excluded as outliers (error > {OUTLIER_ERROR_THRESHOLD:.0f}%):")
        lines.append("-" *50)
        for item in outliers:
            lines.append(
                f"{item['group']:<10} g = {item['measured_g']:.2f} m/s² "
                f"error = {item['percent_error']:.1f}%"
            )
    lines.append("")
    lines.append("Overall statistics (valid groups only):")
    lines.append("-" * 50)
    lines.append(f"Mean measured g: {statistics['mean_g']:.3f} m/s²")
    lines.append(
        f"Deviation of the mean from the theoretical value: "
        f"{statistics['deviation_from_theoretical']:+.3f} m/s²"
    )

    most_precise = statistics['most_precise_group']
    least_precise = statistics['least_precise_group']
    lines.append(
        f"Most precise group: {most_precise['group']} "
        f"(error of {most_precise['percent_error']:.1f}%)"
    )
    lines.append(
        f"Least precise group: {least_precise['group']} "
        f"(error of {least_precise['percent_error']:.1f}%)"
    )
    lines.append("=" *50)

    return "\n".join(lines)

def save_report(text, output_path):
    """Writes the report to a .txt file."""
    with open(output_path, "w", encoding='utf-8') as file:
        file.write(text)

def main():
    input_path = "data/pendulum_measurements.csv"
    output_path = "pendulum_report.txt"

    data = read_data(input_path)

    if not data:
        print("No valid data found. Exiting.")
        return

    valid_data, outliers = separate_outliers(data)
    
    statistics = calculate_statistics(valid_data)
    report = generate_report(valid_data, outliers, statistics)

    print(report)
    save_report(report, output_path)
    print(f"\nReport saved to: {output_path}")

if __name__ == "__main__":
    main()