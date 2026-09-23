import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

np.random.seed(SEED)

NUMBER_OF_RECORDS = 10_000

TIME_INTERVAL_MINUTES = 1

MACHINE_ID = "CAT-SIM-EXC-001"

START_TIME = "2026-01-01 08:00:00"

OUTPUT_PATH = Path(
    "data/raw/machine_telemetry.csv"
)


# ============================================================
# SCENARIO DISTRIBUTION
# ============================================================

SCENARIO_COUNTS = {

    "NORMAL": 7000,

    "HEAVY_LOAD": 1000,

    "EXCESSIVE_IDLE": 500,

    "OVERHEATING": 400,

    "HYDRAULIC_ANOMALY": 400,

    "FUEL_INEFFICIENCY": 300,

    "SAFETY_VIOLATION": 200,

    "SENSOR_ANOMALY": 200
}


# ============================================================
# GENERATE TIMESTAMPS
# ============================================================

def generate_timestamps():

    return pd.date_range(

        start=START_TIME,

        periods=NUMBER_OF_RECORDS,

        freq=f"{TIME_INTERVAL_MINUTES}min"
    )


# ============================================================
# GENERATE SCENARIO BLOCKS
# ============================================================

def get_block_size(scenario):

    if scenario == "NORMAL":

        return np.random.randint(
            100,
            400
        )

    if scenario == "HEAVY_LOAD":

        return np.random.randint(
            30,
            120
        )

    if scenario == "EXCESSIVE_IDLE":

        return np.random.randint(
            20,
            80
        )

    if scenario == "OVERHEATING":

        return np.random.randint(
            15,
            50
        )

    if scenario == "HYDRAULIC_ANOMALY":

        return np.random.randint(
            10,
            40
        )

    if scenario == "FUEL_INEFFICIENCY":

        return np.random.randint(
            20,
            60
        )

    if scenario == "SAFETY_VIOLATION":

        return np.random.randint(
            5,
            30
        )

    # SENSOR_ANOMALY

    return np.random.randint(
        5,
        25
    )


def generate_scenario_sequence():

    scenario_blocks = []


    for scenario, total_records in SCENARIO_COUNTS.items():

        remaining = total_records


        while remaining > 0:

            block_size = get_block_size(
                scenario
            )

            block_size = min(
                block_size,
                remaining
            )


            scenario_blocks.append(
                (
                    scenario,
                    block_size
                )
            )


            remaining -= block_size


    # Shuffle the blocks, not individual records.
    # This preserves temporal persistence.

    np.random.shuffle(
        scenario_blocks
    )


    scenario_sequence = []


    for scenario, block_size in scenario_blocks:

        scenario_sequence.extend(
            [scenario] * block_size
        )


    if len(scenario_sequence) != NUMBER_OF_RECORDS:

        raise ValueError(
            "Scenario sequence length does not "
            "match NUMBER_OF_RECORDS."
        )


    return scenario_sequence


# ============================================================
# GENERATE OPERATING CONDITIONS
# ============================================================

def generate_operating_conditions(
    scenario
):

    # --------------------------------------------------------
    # Default values
    # --------------------------------------------------------

    load = np.random.uniform(
        30,
        70
    )

    rpm = np.random.normal(
        1700 + load * 5,
        50
    )

    hydraulic_pressure = np.random.normal(
        220 + load * 0.8,
        10
    )

    idle_time = np.random.exponential(
        3
    )

    machine_speed = np.random.uniform(
        0,
        8
    )

    seatbelt_fastened = 1


    # ========================================================
    # NORMAL
    # ========================================================

    if scenario == "NORMAL":

        load = np.random.uniform(
            30,
            70
        )

        rpm = np.random.normal(
            1600 + load * 5,
            40
        )

        hydraulic_pressure = np.random.normal(
            220 + load * 0.7,
            8
        )

        idle_time = np.random.exponential(
            3
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 1


    # ========================================================
    # HEAVY LOAD
    # ========================================================

    elif scenario == "HEAVY_LOAD":

        load = np.random.uniform(
            80,
            100
        )

        rpm = np.random.normal(
            2100,
            60
        )

        hydraulic_pressure = np.random.normal(
            310,
            12
        )

        idle_time = np.random.uniform(
            0,
            2
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 1


    # ========================================================
    # EXCESSIVE IDLE
    # ========================================================

    elif scenario == "EXCESSIVE_IDLE":

        load = np.random.uniform(
            5,
            15
        )

        rpm = np.random.normal(
            850,
            30
        )

        hydraulic_pressure = np.random.normal(
            120,
            8
        )

        idle_time = np.random.uniform(
            15,
            35
        )

        machine_speed = 0

        seatbelt_fastened = 1


    # ========================================================
    # OVERHEATING
    # ========================================================

    elif scenario == "OVERHEATING":

        load = np.random.uniform(
            75,
            100
        )

        rpm = np.random.normal(
            2100,
            50
        )

        hydraulic_pressure = np.random.normal(
            300,
            10
        )

        idle_time = np.random.uniform(
            0,
            2
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 1


    # ========================================================
    # HYDRAULIC ANOMALY
    # ========================================================

    elif scenario == "HYDRAULIC_ANOMALY":

        load = np.random.uniform(
            60,
            95
        )

        rpm = np.random.normal(
            1900,
            60
        )

        # Two abnormal hydraulic modes:
        #
        # Low pressure
        # High pressure

        if np.random.random() < 0.45:

            hydraulic_pressure = np.random.uniform(
                60,
                100
            )

        else:

            hydraulic_pressure = np.random.uniform(
                350,
                400
            )

        idle_time = np.random.uniform(
            0,
            5
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 1


    # ========================================================
    # FUEL INEFFICIENCY
    # ========================================================

    elif scenario == "FUEL_INEFFICIENCY":

        load = np.random.uniform(
            50,
            85
        )

        rpm = np.random.normal(
            2000,
            80
        )

        hydraulic_pressure = np.random.normal(
            270,
            15
        )

        idle_time = np.random.uniform(
            8,
            20
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 1


    # ========================================================
    # SAFETY VIOLATION
    # ========================================================

    elif scenario == "SAFETY_VIOLATION":

        load = np.random.uniform(
            30,
            70
        )

        rpm = np.random.normal(
            1750,
            50
        )

        hydraulic_pressure = np.random.normal(
            230,
            10
        )

        idle_time = np.random.uniform(
            0,
            5
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 0


    # ========================================================
    # SENSOR ANOMALY
    # ========================================================

    elif scenario == "SENSOR_ANOMALY":

        load = np.random.uniform(
            30,
            80
        )

        rpm = np.random.normal(
            1700,
            50
        )

        hydraulic_pressure = np.random.normal(
            230,
            10
        )

        idle_time = np.random.uniform(
            0,
            5
        )

        machine_speed = np.random.uniform(
            0,
            8
        )

        seatbelt_fastened = 1


    return {

        "load": load,

        "rpm": rpm,

        "hydraulic_pressure": hydraulic_pressure,

        "idle_time": idle_time,

        "machine_speed": machine_speed,

        "seatbelt_fastened": seatbelt_fastened
    }


# ============================================================
# TEMPERATURE MODEL
# ============================================================

def update_engine_temperature(
    previous_temperature,
    load,
    ambient_temperature,
    scenario
):
    """
    Generate realistic engine temperature with thermal inertia.

    Temperature remains continuous between records, while
    scenario transitions are handled so abnormal conditions
    do not unrealistically bleed into normal operation.
    """

    # --------------------------------------------------------
    # Base target temperature
    # --------------------------------------------------------

    target_temperature = (

        68

        + (load * 0.24)

        + (ambient_temperature - 30) * 0.15

        + np.random.normal(
            0,
            1.2
        )
    )


    # ========================================================
    # SCENARIO-SPECIFIC THERMAL BEHAVIOR
    # ========================================================

    if scenario == "HEAVY_LOAD":

        target_temperature += np.random.uniform(
            5,
            10
        )

        target_temperature = np.clip(
            target_temperature,
            80,
            105
        )


    elif scenario == "OVERHEATING":

        # Force overheating toward a genuinely
        # abnormal thermal range.

        target_temperature = np.random.uniform(
            120,
            135
        )


    elif scenario == "EXCESSIVE_IDLE":

        target_temperature -= np.random.uniform(
            2,
            5
        )

        target_temperature = np.clip(
            target_temperature,
            65,
            90
        )


    elif scenario == "NORMAL":

        # Normal operating temperature should remain
        # within a realistic range.

        target_temperature = np.clip(
            target_temperature,
            70,
            95
        )


    # ========================================================
    # SENSOR ANOMALY
    # ========================================================

    if scenario == "SENSOR_ANOMALY":

        # 50% chance of an abnormal temperature reading.

        if np.random.random() < 0.50:

            return np.random.uniform(
                120,
                150
            )

        # Otherwise behave normally.

        if target_temperature > previous_temperature:

            response_rate = 0.25

        else:

            response_rate = 0.15


    # ========================================================
    # THERMAL RESPONSE
    # ========================================================

    elif scenario == "OVERHEATING":

        # Rapid temperature increase during
        # an overheating event.

        response_rate = 0.65


    elif scenario == "NORMAL":

        # If recovering from overheating, cool faster.

        if previous_temperature > 110:

            response_rate = 0.65

        elif previous_temperature > 100:

            response_rate = 0.55

        else:

            response_rate = 0.20


    else:

        # Normal thermal inertia for other scenarios.

        if target_temperature > previous_temperature:

            response_rate = 0.25

        else:

            response_rate = 0.15


    # ========================================================
    # APPLY THERMAL INERTIA
    # ========================================================

    engine_temperature = (

        previous_temperature
        * (1 - response_rate)

        + target_temperature
        * response_rate
    )


    # Small sensor noise

    engine_temperature += np.random.normal(
        0,
        0.3
    )


    # ========================================================
    # FINAL SCENARIO BOUNDS
    # ========================================================

    if scenario == "NORMAL":

        engine_temperature = np.clip(
            engine_temperature,
            65,
            100
        )


    elif scenario == "OVERHEATING":

        engine_temperature = np.clip(
            engine_temperature,
            105,
            145
        )


    return engine_temperature


# ============================================================
# FUEL CONSUMPTION MODEL
# ============================================================

def calculate_fuel_consumption(
    load,
    rpm,
    idle_time,
    scenario
):

    fuel_consumption = (

        3

        + (load * 0.07)

        + (rpm * 0.001)

        + np.random.normal(
            0,
            0.15
        )
    )


    # --------------------------------------------------------
    # Fuel inefficiency
    # --------------------------------------------------------

    if scenario == "FUEL_INEFFICIENCY":

        fuel_consumption += np.random.uniform(
            3,
            6
        )


    # --------------------------------------------------------
    # Excessive idle
    # --------------------------------------------------------

    elif scenario == "EXCESSIVE_IDLE":

        fuel_consumption += np.random.uniform(
            1,
            2
        )


    return max(
        0,
        fuel_consumption
    )


# ============================================================
# FUEL LEVEL MODEL
# ============================================================

def update_fuel_level(
    fuel_level,
    fuel_consumption
):

    # Assume a synthetic 600-liter fuel tank.

    TANK_CAPACITY_LITERS = 600


    # Fuel consumption is L/hour.
    #
    # Convert to liters consumed in one minute.

    liters_used = (

        fuel_consumption
        * TIME_INTERVAL_MINUTES
        / 60
    )


    # Convert consumption to percentage.

    percentage_used = (

        liters_used
        / TANK_CAPACITY_LITERS
        * 100
    )


    # --------------------------------------------------------
    # Fuel gauge
    # --------------------------------------------------------

    fuel_level -= percentage_used


    # Small measurement noise

    fuel_level += np.random.normal(
        0,
        0.01
    )


    # --------------------------------------------------------
    # Synthetic refueling event
    # --------------------------------------------------------

    refueled = False


    if fuel_level <= 15:

        fuel_level = np.random.uniform(
            85,
            98
        )

        refueled = True


    fuel_level = max(
        0,
        min(
            100,
            fuel_level
        )
    )


    return fuel_level, refueled


# ============================================================
# MACHINE HEALTH MODEL
# ============================================================

def calculate_machine_health(
    engine_temperature,
    hydraulic_pressure,
    fuel_consumption,
    load,
    idle_time,
    seatbelt_fastened
):

    # Start from a healthy machine.

    health = 100


    # ========================================================
    # TEMPERATURE PENALTY
    # ========================================================

    if engine_temperature <= 95:

        temperature_penalty = 0

    elif engine_temperature <= 105:

        temperature_penalty = (

            engine_temperature - 95
        ) * 1.5

    else:

        temperature_penalty = (

            10 * 1.5

            + (engine_temperature - 105)
            * 2.0
        )


    # ========================================================
    # HYDRAULIC PENALTY
    # ========================================================

    if 150 <= hydraulic_pressure <= 330:

        hydraulic_penalty = 0

    elif hydraulic_pressure < 150:

        hydraulic_penalty = min(
            25,
            (150 - hydraulic_pressure)
            * 0.15
        )

    else:

        hydraulic_penalty = min(
            30,
            (hydraulic_pressure - 330)
            * 0.15
        )


    # ========================================================
    # HIGH LOAD PENALTY
    # ========================================================

    if load <= 80:

        load_penalty = 0

    else:

        load_penalty = (

            load - 80
        ) * 0.15


    # ========================================================
    # EXCESSIVE IDLE PENALTY
    # ========================================================

    if idle_time <= 10:

        idle_penalty = 0

    else:

        idle_penalty = min(
            8,
            (idle_time - 10)
            * 0.25
        )


    # ========================================================
    # SAFETY PENALTY
    # ========================================================

    if seatbelt_fastened == 1:

        safety_penalty = 0

    else:

        safety_penalty = 8


    # ========================================================
    # FUEL EFFICIENCY PENALTY
    # ========================================================

    if fuel_consumption <= 12:

        fuel_penalty = 0

    else:

        fuel_penalty = min(
            10,
            (fuel_consumption - 12)
            * 1.2
        )


    # ========================================================
    # TOTAL HEALTH
    # ========================================================

    health = (

        100

        - temperature_penalty

        - hydraulic_penalty

        - load_penalty

        - idle_penalty

        - safety_penalty

        - fuel_penalty
    )


    # Small measurement variation

    health += np.random.normal(
        0,
        1.0
    )


    # Keep health within valid range.

    health = max(
        0,
        min(
            100,
            health
        )
    )


    return health


# ============================================================
# GENERATE ONE TELEMETRY RECORD
# ============================================================

def generate_record(
    timestamp,
    scenario,
    previous_temperature,
    fuel_level
):

    # --------------------------------------------------------
    # Ambient conditions
    # --------------------------------------------------------

    minute_of_day = (

        timestamp.hour * 60
        + timestamp.minute
    )


    ambient_temperature = (

        30

        + 5
        * np.sin(
            2
            * np.pi
            * minute_of_day
            / 1440
        )

        + np.random.normal(
            0,
            0.8
        )
    )


    humidity = np.random.uniform(
        45,
        85
    )


    # --------------------------------------------------------
    # Operating conditions
    # --------------------------------------------------------

    operating = generate_operating_conditions(
        scenario
    )


    load = operating["load"]

    rpm = operating["rpm"]

    hydraulic_pressure = operating[
        "hydraulic_pressure"
    ]

    idle_time = operating[
        "idle_time"
    ]

    machine_speed = operating[
        "machine_speed"
    ]

    seatbelt_fastened = operating[
        "seatbelt_fastened"
    ]


    # --------------------------------------------------------
    # Engine temperature
    # --------------------------------------------------------

    engine_temperature = update_engine_temperature(

        previous_temperature,

        load,

        ambient_temperature,

        scenario
    )


    # --------------------------------------------------------
    # Sensor anomaly: abnormal hydraulic reading
    # --------------------------------------------------------

    if scenario == "SENSOR_ANOMALY":

        if np.random.random() < 0.50:

            hydraulic_pressure = np.random.uniform(
                450,
                550
            )


    # --------------------------------------------------------
    # Fuel consumption
    # --------------------------------------------------------

    fuel_consumption = calculate_fuel_consumption(

        load,

        rpm,

        idle_time,

        scenario
    )


    # --------------------------------------------------------
    # Fuel level
    # --------------------------------------------------------

    fuel_level, refueled = update_fuel_level(

        fuel_level,

        fuel_consumption
    )


    # --------------------------------------------------------
    # Machine health
    # --------------------------------------------------------

    health_score = calculate_machine_health(

        engine_temperature,

        hydraulic_pressure,

        fuel_consumption,

        load,

        idle_time,

        seatbelt_fastened
    )


    # --------------------------------------------------------
    # Anomaly label
    # --------------------------------------------------------

    if scenario == "NORMAL":

        anomaly_label = 0

    else:

        anomaly_label = 1


    # --------------------------------------------------------
    # Operator
    # --------------------------------------------------------

    operator_present = 1


    # --------------------------------------------------------
    # Create record
    # --------------------------------------------------------

    record = {

        "machine_id": MACHINE_ID,

        "timestamp": timestamp,

        "scenario": scenario,

        "engine_rpm": round(
            rpm,
            2
        ),

        "engine_temperature_c": round(
            engine_temperature,
            2
        ),

        "hydraulic_pressure_bar": round(
            hydraulic_pressure,
            2
        ),

        "fuel_consumption_lph": round(
            fuel_consumption,
            2
        ),

        "fuel_level_percent": round(
            fuel_level,
            2
        ),

        "load_percentage": round(
            load,
            2
        ),

        "idle_time_minutes": round(
            idle_time,
            2
        ),

        "machine_speed_kmh": round(
            machine_speed,
            2
        ),

        "seatbelt_fastened": seatbelt_fastened,

        "operator_present": operator_present,

        "ambient_temperature_c": round(
            ambient_temperature,
            2
        ),

        "humidity_percent": round(
            humidity,
            2
        ),

        "machine_health_score": round(
            health_score,
            2
        ),

        "anomaly_label": anomaly_label,

        "refueled": int(
            refueled
        )
    }


    return record


# ============================================================
# DATASET VALIDATION
# ============================================================

def validate_dataset(df):

    print(
        "\n"
        + "=" * 60
    )

    print(
        "VALIDATING DATASET"
    )

    print(
        "=" * 60
    )


    # --------------------------------------------------------
    # Record count
    # --------------------------------------------------------

    assert len(df) == NUMBER_OF_RECORDS, (

        "Incorrect number of records."
    )


    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    missing_values = (
        df.isnull().sum().sum()
    )


    assert missing_values == 0, (

        "Dataset contains missing values."
    )


    # --------------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------------

    duplicate_rows = (
        df.duplicated().sum()
    )


    assert duplicate_rows == 0, (

        "Duplicate rows detected."
    )


    # --------------------------------------------------------
    # Timestamp validation
    # --------------------------------------------------------

    timestamps = df["timestamp"]


    assert timestamps.is_monotonic_increasing, (

        "Timestamps are not ordered."
    )


    assert timestamps.is_unique, (

        "Duplicate timestamps detected."
    )


    # --------------------------------------------------------
    # Scenario validation
    # --------------------------------------------------------

    actual_counts = (
        df["scenario"]
        .value_counts()
        .to_dict()
    )


    assert actual_counts == SCENARIO_COUNTS, (

        f"Scenario distribution incorrect:\n"
        f"{actual_counts}"
    )


    # --------------------------------------------------------
    # Percentage validation
    # --------------------------------------------------------

    assert df[
        "load_percentage"
    ].between(
        0,
        100
    ).all()


    assert df[
        "fuel_level_percent"
    ].between(
        0,
        100
    ).all()


    assert df[
        "humidity_percent"
    ].between(
        0,
        100
    ).all()


    assert df[
        "machine_health_score"
    ].between(
        0,
        100
    ).all()


    # --------------------------------------------------------
    # RPM
    # --------------------------------------------------------

    assert (
        df["engine_rpm"] >= 0
    ).all()


    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    assert (
        df["engine_temperature_c"] > 0
    ).all()


    # --------------------------------------------------------
    # Fuel
    # --------------------------------------------------------

    assert (
        df["fuel_consumption_lph"] >= 0
    ).all()


    # --------------------------------------------------------
    # Seatbelt
    # --------------------------------------------------------

    assert set(
        df["seatbelt_fastened"].unique()
    ).issubset(
        {0, 1}
    )


    # --------------------------------------------------------
    # Operator
    # --------------------------------------------------------

    assert set(
        df["operator_present"].unique()
    ) == {1}


    # --------------------------------------------------------
    # Anomaly labels
    # --------------------------------------------------------

    assert set(
        df["anomaly_label"].unique()
    ) == {0, 1}


    # --------------------------------------------------------
    # Safety scenario validation
    # --------------------------------------------------------

    safety_records = df[
        df["scenario"] == "SAFETY_VIOLATION"
    ]


    assert (
        safety_records[
            "seatbelt_fastened"
        ] == 0
    ).all()


    # --------------------------------------------------------
    # Excessive idle validation
    # --------------------------------------------------------

    idle_records = df[
        df["scenario"] == "EXCESSIVE_IDLE"
    ]


    assert (
        idle_records[
            "machine_speed_kmh"
        ] == 0
    ).all()


    # --------------------------------------------------------
    # Fuel level validation
    # --------------------------------------------------------

    refuel_count = (
        df["refueled"].sum()
    )


    assert refuel_count > 0, (

        "No refueling events were generated."
    )


    print(
        "\nAll validation checks passed."
    )


# ============================================================
# GENERATE DATASET
# ============================================================

def generate_dataset():

    print(
        "\n"
        + "=" * 60
    )

    print(
        "GENERATING SYNTHETIC MACHINE DATASET"
    )

    print(
        "=" * 60
    )


    timestamps = generate_timestamps()


    scenario_sequence = (
        generate_scenario_sequence()
    )


    rows = []


    # --------------------------------------------------------
    # Initial machine state
    # --------------------------------------------------------

    previous_temperature = 80.0

    fuel_level = 100.0


    # ========================================================
    # SIMULATION LOOP
    # ========================================================

    for i in range(
        NUMBER_OF_RECORDS
    ):

        timestamp = timestamps[i]

        scenario = scenario_sequence[i]


        record = generate_record(

            timestamp,

            scenario,

            previous_temperature,

            fuel_level
        )


        rows.append(
            record
        )


        # ----------------------------------------------------
        # Carry machine state forward
        # ----------------------------------------------------

        previous_temperature = record[
            "engine_temperature_c"
        ]

        fuel_level = record[
            "fuel_level_percent"
        ]


    # ========================================================
    # DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        rows
    )


    # ========================================================
    # VALIDATE
    # ========================================================

    validate_dataset(
        df
    )


    # ========================================================
    # CREATE OUTPUT DIRECTORY
    # ========================================================

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # SAVE
    # ========================================================

    df.to_csv(

        OUTPUT_PATH,

        index=False
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "SYNTHETIC MACHINE DATASET GENERATED"
    )

    print(
        "=" * 60
    )


    print(
        f"\nMachine ID: {MACHINE_ID}"
    )


    print(
        f"Number of records: {len(df):,}"
    )


    print(
        f"Number of features: {len(df.columns)}"
    )


    print(
        f"\nSaved to: {OUTPUT_PATH}"
    )


    print(
        "\nDataset shape:"
    )

    print(
        df.shape
    )


    # --------------------------------------------------------
    # Scenario distribution
    # --------------------------------------------------------

    print(
        "\nScenario distribution:"
    )

    print(
        df[
            "scenario"
        ].value_counts()
    )


    # --------------------------------------------------------
    # Anomaly distribution
    # --------------------------------------------------------

    print(
        "\nAnomaly distribution:"
    )

    print(
        df[
            "anomaly_label"
        ].value_counts()
    )


    # --------------------------------------------------------
    # Refueling events
    # --------------------------------------------------------

    print(
        "\nRefueling events:"
    )

    print(
        df[
            "refueled"
        ].sum()
    )


    # --------------------------------------------------------
    # Health statistics
    # --------------------------------------------------------

    print(
        "\nAverage machine health by scenario:"
    )

    print(
        df.groupby(
            "scenario"
        )[
            "machine_health_score"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .round(2)
    )


    # --------------------------------------------------------
    # Sensor summary
    # --------------------------------------------------------

    print(
        "\nSensor summary:"
    )

    print(
        df[
            [
                "engine_rpm",

                "engine_temperature_c",

                "hydraulic_pressure_bar",

                "fuel_consumption_lph",

                "fuel_level_percent",

                "load_percentage",

                "idle_time_minutes",

                "machine_health_score"
            ]
        ].describe().round(2)
    )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "DATASET VALIDATION PASSED"
    )

    print(
        "=" * 60
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    generate_dataset()