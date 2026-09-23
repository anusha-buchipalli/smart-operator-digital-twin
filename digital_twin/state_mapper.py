from typing import Dict, Any

from digital_twin.machine_state import (
    MachineState,
    EngineState,
    HydraulicState,
    FuelState,
    OperationState,
    SafetyState,
)


# ---------------------------------------------------------
# Thresholds
# ---------------------------------------------------------

ENGINE_TEMP_WARNING = 100.0
ENGINE_TEMP_CRITICAL = 120.0

HYDRAULIC_PRESSURE_LOW = 100.0
HYDRAULIC_PRESSURE_HIGH = 350.0

FUEL_LEVEL_LOW = 20.0
FUEL_LEVEL_CRITICAL = 10.0

LOAD_WARNING = 80.0
LOAD_CRITICAL = 95.0

IDLE_WARNING = 15.0


# ---------------------------------------------------------
# Engine status
# ---------------------------------------------------------

def get_engine_status(
    temperature_c: float,
    rpm: float
) -> str:

    if temperature_c >= ENGINE_TEMP_CRITICAL:
        return "CRITICAL_OVERHEATING"

    if temperature_c >= ENGINE_TEMP_WARNING:
        return "OVERHEATING"

    if rpm > 2200:
        return "HIGH_RPM"

    return "NORMAL"


# ---------------------------------------------------------
# Hydraulic status
# ---------------------------------------------------------

def get_hydraulic_status(pressure_bar: float) -> str:

    if pressure_bar < HYDRAULIC_PRESSURE_LOW:
        return "LOW_PRESSURE"

    if pressure_bar > HYDRAULIC_PRESSURE_HIGH:
        return "HIGH_PRESSURE"

    return "NORMAL"


# ---------------------------------------------------------
# Fuel status
# ---------------------------------------------------------

def get_fuel_status(level_percent: float) -> str:

    if level_percent <= FUEL_LEVEL_CRITICAL:
        return "CRITICAL_LOW"

    if level_percent <= FUEL_LEVEL_LOW:
        return "LOW"

    return "NORMAL"


# ---------------------------------------------------------
# Operation status
# ---------------------------------------------------------

def get_operation_status(
    load_percentage: float,
    idle_time_minutes: float,
    speed_kmh: float
) -> str:

    if idle_time_minutes >= IDLE_WARNING and speed_kmh == 0:
        return "EXCESSIVE_IDLE"

    if load_percentage >= LOAD_CRITICAL:
        return "CRITICAL_LOAD"

    if load_percentage >= LOAD_WARNING:
        return "HEAVY_LOAD"

    return "NORMAL"


# ---------------------------------------------------------
# Safety status
# ---------------------------------------------------------

def get_safety_status(
    seatbelt_fastened: bool,
    operator_present: bool
) -> str:

    if operator_present and not seatbelt_fastened:
        return "SEATBELT_VIOLATION"

    if not operator_present:
        return "NO_OPERATOR"

    return "SAFE"


# ---------------------------------------------------------
# Overall machine status
# ---------------------------------------------------------

def calculate_overall_status(
    engine_status: str,
    hydraulic_status: str,
    fuel_status: str,
    operation_status: str,
    safety_status: str,
    health_score: float,
    anomaly_detected: bool
) -> str:

    critical_conditions = [
        "CRITICAL_OVERHEATING",
        "LOW_PRESSURE",
        "HIGH_PRESSURE",
        "CRITICAL_LOW",
        "CRITICAL_LOAD",
        "SEATBELT_VIOLATION",
    ]

    warning_conditions = [
        "OVERHEATING",
        "HEAVY_LOAD",
        "EXCESSIVE_IDLE",
        "LOW",
        "NO_OPERATOR",
    ]

    statuses = [
        engine_status,
        hydraulic_status,
        fuel_status,
        operation_status,
        safety_status,
    ]

    if any(status in critical_conditions for status in statuses):
        return "CRITICAL"

    if health_score < 50:
        return "CRITICAL"

    if any(status in warning_conditions for status in statuses):
        return "WARNING"

    if health_score < 80:
        return "WARNING"

    return "NORMAL"


# ---------------------------------------------------------
# Main mapper
# ---------------------------------------------------------

def map_telemetry_to_state(
    telemetry: Dict[str, Any]
) -> MachineState:

    engine_rpm = float(telemetry["engine_rpm"])
    engine_temperature = float(telemetry["engine_temperature_c"])

    hydraulic_pressure = float(
        telemetry["hydraulic_pressure_bar"]
    )

    fuel_level = float(
        telemetry["fuel_level_percent"]
    )

    fuel_consumption = float(
        telemetry["fuel_consumption_lph"]
    )

    load_percentage = float(
        telemetry["load_percentage"]
    )

    speed_kmh = float(
        telemetry["machine_speed_kmh"]
    )

    idle_time = float(
        telemetry["idle_time_minutes"]
    )

    seatbelt_fastened = bool(
        telemetry["seatbelt_fastened"]
    )

    operator_present = bool(
        telemetry["operator_present"]
    )

    health_score = float(
        telemetry["machine_health_score"]
    )

    anomaly_detected = bool(
        telemetry["anomaly_label"]
    )

    scenario = str(
        telemetry["scenario"]
    )

    # Determine subsystem states
    engine_status = get_engine_status(
        engine_temperature,
        engine_rpm
    )

    hydraulic_status = get_hydraulic_status(
        hydraulic_pressure
    )

    fuel_status = get_fuel_status(
        fuel_level
    )

    operation_status = get_operation_status(
        load_percentage,
        idle_time,
        speed_kmh
    )

    safety_status = get_safety_status(
        seatbelt_fastened,
        operator_present
    )

    overall_status = calculate_overall_status(
        engine_status,
        hydraulic_status,
        fuel_status,
        operation_status,
        safety_status,
        health_score,
        anomaly_detected
    )

    # Construct Digital Twin state
    machine_state = MachineState(
        machine_id=str(
            telemetry["machine_id"]
        ),

        timestamp=str(
            telemetry["timestamp"]
        ),

        overall_status=overall_status,

        engine=EngineState(
            rpm=engine_rpm,
            temperature_c=engine_temperature,
            status=engine_status,
        ),

        hydraulics=HydraulicState(
            pressure_bar=hydraulic_pressure,
            status=hydraulic_status,
        ),

        fuel=FuelState(
            level_percent=fuel_level,
            consumption_lph=fuel_consumption,
            status=fuel_status,
        ),

        operation=OperationState(
            load_percentage=load_percentage,
            speed_kmh=speed_kmh,
            idle_time_minutes=idle_time,
            status=operation_status,
        ),

        safety=SafetyState(
            seatbelt_fastened=seatbelt_fastened,
            operator_present=operator_present,
            status=safety_status,
        ),

        machine_health_score=health_score,

        anomaly_detected=anomaly_detected,

        scenario=scenario,
    )

    return machine_state