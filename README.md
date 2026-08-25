# Pendulum Gravity Analyzer

_[Leia em Português](README.pt-br.md)_

A command-line Python that analyzes real experimental data collected by hight scholl students measuring the local gravitational acceleration (_g_) using a simple pendulum. This was my capstone project for the Python Fundamentals phase of my self-study path into data science.

## About the data

The dataset (`data/pendulum_measurements.csv`) contains real measurements collected by my own students, in a physics class I taught in Juiz de Fora, Brazil. Each group timed the oscillation of a pendulum, calculated their own estimate of _g_ and compared it against the theoretical local value (9.78 m/s²) to compute a percente error. Group identifiers have been anonymized (`G01`, `G02`, ...).

The data is intentionally "real" and imperfect: it includes a row with a missing value and a wildly inaccurate outlier measurement, both of wich the script needs to handle gracefully instead of crashing.

### What the script does

1. **Reads** the CSV file and validates each row (skips malformed or missing values without stopping the whole program).
2. **Separates outliers**: any group with a percent error above the configurable threshold (10% by default) is excluded from the statistics, but still listed separately for transparence.
3. **Calculates statistics**: mean measured _g_, deviation from the theoretical value, most and least precise groups.
4. **Clasifies each group's precision** as `Excelent`, `Good`, or `Needs review`, based on its percent error.
5. **Generates a formatted report**, print to the console and saved as `pendulum_report.txt`.

## How to run

```bash
python3 pendulum_analyzer.py
```

No external dependencies — built entirely with Python's standard libarary (`csv`).

## Project structure

```
pendulum-gravity-analyzer/
├── pendulum_analyzer.py         # main script
├── data/
│   └── pendulum_measurements.csv
├── README.md
└── README.pt-br.md
```

## Sample output

```
==================================================
REPORT - GRAVITY MEASUREMENT WITH SIMPLE PENDULUM
==================================================
Theoretical reference value: 9.78 m/s²
Outlier error threshold: 10%
Total valid groups: 14
Total excluded groups (outliers): 13

Results per group (valid):
--------------------------------------------------
G02        g = 9.46 m/s²  error = 3.3%  -> Good
G07        g = 9.60 m/s²  error = 1.8%  -> Excellent
...

Overall statistics (valid groups only):
--------------------------------------------------
Mean measured g: 10.025 m/s²
Deviation of the mean from the theoretical value: +0.245 m/s²
Most precise group: G07 (error of 1.8%)
Least precise group: G09 (error of 9.9%)
==================================================
```

## What I learned building this

This project was the capstone for the first phase of my Python-for-data-science study plan, and it was designed to bring together everything from that phase in one working, real-world tool rather than isolated excercises:

- **Variables, data, types & operators** — working with floats for physical measurements and percentages
- **Control flow** (`if` / `elif` / `else`) — classifying each group's precision
- **Data structures** — representing each group as a dictionary, and the dataset as the list of dictionaries
- **Functions** — breaking the program into single-responsibility steps: read → validate → separate outliers → calculate statistics → format → save
- **List comprehensions** — filtering valid data vs. outliers in one line
- **String manipulation & f-strings** — build an aligned, readable report with formatted numbers (`.2f`, `+.3f`, padding)
- **Error handling (`try`, `except`)** — the dataset has a missing value and an extreme outlier; the script had to keep running and report clearly what happend instead of crashing
- **File reading/writing** — reading the CSV with `csv.DictReader`and writing the final report to a `.txt`file

Along the way I also debugged two subtle real bugs I introduced while writing the script: a misplaced `if __name__ == "__main__":`block accidentally nested _inside_ another function (wich silently prevented the whole script from ever running, with no error message at all), and a typo in the file encoding name. Both were good, humbling lessons in how Python can fail silently versus loudly — and why testing matter.

## What's next

This same dataset is coming back in a later phase of my study plan, where I'll redo this analysis using **pandas** instead of the standardy library — a deliberate comparison between the "manual" and library-based approches to the same real-world problem.

---

_Part of my self-study path into Python for Data Science. Feedback welcome!_
