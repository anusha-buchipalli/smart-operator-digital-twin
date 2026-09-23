import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# LOAD DATASET
# ============================================================

DATA_PATH = "data/raw/machine_telemetry.csv"

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["timestamp"]
)


print("\n" + "=" * 60)
print("DIGITAL TWIN DATASET ANALYSIS")
print("=" * 60)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("\nDataset shape:")
print(df.shape)


print("\nColumns:")
print(df.columns.tolist())


print("\nMissing values:")
print(
    df.isnull().sum()
)


# ============================================================
# SCENARIO DISTRIBUTION
# ============================================================

print("\nScenario distribution:")

scenario_counts = (
    df["scenario"]
    .value_counts()
)

print(
    scenario_counts
)


# ============================================================
# SCENARIO DISTRIBUTION GRAPH
# ============================================================

plt.figure(
    figsize=(10, 6)
)

scenario_counts.plot(
    kind="bar"
)

plt.title(
    "Machine Operating Scenario Distribution"
)

plt.xlabel(
    "Scenario"
)

plt.ylabel(
    "Number of Records"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.show()


# ============================================================
# MACHINE SENSOR SUMMARY
# ============================================================

sensor_columns = [

    "engine_rpm",

    "engine_temperature_c",

    "hydraulic_pressure_bar",

    "fuel_consumption_lph",

    "fuel_level_percent",

    "load_percentage",

    "idle_time_minutes",

    "machine_speed_kmh",

    "ambient_temperature_c",

    "humidity_percent",

    "machine_health_score"
]


print("\nSensor statistics:")

print(
    df[sensor_columns].describe()
)


# ============================================================
# NORMAL VS ANOMALOUS
# ============================================================

print("\nNormal vs anomalous records:")

print(
    df["anomaly_label"]
    .value_counts()
)


# ============================================================
# ENGINE TEMPERATURE OVER TIME
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    df["timestamp"],
    df["engine_temperature_c"]
)

plt.title(
    "Engine Temperature Over Time"
)

plt.xlabel(
    "Time"
)

plt.ylabel(
    "Temperature (°C)"
)

plt.tight_layout()

plt.show()


# ============================================================
# ENGINE RPM OVER TIME
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    df["timestamp"],
    df["engine_rpm"]
)

plt.title(
    "Engine RPM Over Time"
)

plt.xlabel(
    "Time"
)

plt.ylabel(
    "RPM"
)

plt.tight_layout()

plt.show()


# ============================================================
# LOAD VS ENGINE TEMPERATURE
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.scatter(
    df["load_percentage"],
    df["engine_temperature_c"],
    alpha=0.3
)

plt.title(
    "Machine Load vs Engine Temperature"
)

plt.xlabel(
    "Load (%)"
)

plt.ylabel(
    "Engine Temperature (°C)"
)

plt.tight_layout()

plt.show()


# ============================================================
# LOAD VS HYDRAULIC PRESSURE
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.scatter(
    df["load_percentage"],
    df["hydraulic_pressure_bar"],
    alpha=0.3
)

plt.title(
    "Machine Load vs Hydraulic Pressure"
)

plt.xlabel(
    "Load (%)"
)

plt.ylabel(
    "Hydraulic Pressure (bar)"
)

plt.tight_layout()

plt.show()


# ============================================================
# LOAD VS FUEL CONSUMPTION
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.scatter(
    df["load_percentage"],
    df["fuel_consumption_lph"],
    alpha=0.3
)

plt.title(
    "Machine Load vs Fuel Consumption"
)

plt.xlabel(
    "Load (%)"
)

plt.ylabel(
    "Fuel Consumption (L/h)"
)

plt.tight_layout()

plt.show()


# ============================================================
# HEALTH SCORE BY SCENARIO
# ============================================================

health_by_scenario = (

    df
    .groupby("scenario")[
        "machine_health_score"
    ]
    .mean()
    .sort_values()
)


print(
    "\nAverage machine health by scenario:"
)

print(
    health_by_scenario
)


plt.figure(
    figsize=(10, 6)
)

health_by_scenario.plot(
    kind="bar"
)

plt.title(
    "Average Machine Health by Operating Scenario"
)

plt.xlabel(
    "Scenario"
)

plt.ylabel(
    "Average Health Score"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.show()


# ============================================================
# SENSOR CORRELATION
# ============================================================

print(
    "\nSensor correlation matrix:"
)

correlation_matrix = (
    df[sensor_columns]
    .corr()
)

print(
    correlation_matrix.round(2)
)


plt.figure(
    figsize=(12, 10)
)

plt.imshow(
    correlation_matrix,
    aspect="auto"
)

plt.colorbar()

plt.xticks(
    range(len(sensor_columns)),
    sensor_columns,
    rotation=90
)

plt.yticks(
    range(len(sensor_columns)),
    sensor_columns
)

plt.title(
    "Machine Sensor Correlation Matrix"
)

plt.tight_layout()

plt.show()


print(
    "\n" + "=" * 60
)

print(
    "DATASET ANALYSIS COMPLETE"
)

print(
    "=" * 60
)