"""
Entry point for the Pendulum Gravity Analyser.
"""

from pendulum_analyzer import DataLoader, PendulumAnalysis, ReportGenerator

def main():
    input_path = "data/pendulum_measurements.csv"
    output_path = "pendulum_report.txt"

    loader = DataLoader(input_path)
    measurements = loader.load()

    if not measurements:
        print("No valid data found. Exiting.")
        return

    analysis = PendulumAnalysis(measurements)
    report = ReportGenerator(analysis)

    text = report.generate()
    print(text)
    report.save(output_path, text)
    print(f"\nReport saved to: {output_path}")

if __name__ == "__main__":
    main()