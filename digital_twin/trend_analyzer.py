from typing import List, Dict, Any

from digital_twin.machine_state import MachineState


def calculate_trend(values: List[float]) -> str:
    """
    Determine whether a sequence of values is rising,
    falling, or stable.
    """

    if len(values) < 2:
        return "INSUFFICIENT_DATA"

    differences = [
        values[i] - values[i - 1]
        for i in range(1, len(values))
    ]

    average_change = sum(differences) / len(differences)

    # Small changes are treated as stable.
    threshold = 0.5

    if average_change > threshold:
        return "RISING"

    if average_change < -threshold:
        return "FALLING"

    return "STABLE"


def analyze_trends(
    history: List[MachineState]
) -> Dict[str, Any]:
    """
    Analyze recent Digital Twin history and identify
    trends in important machine parameters.
    """

    if len(history) < 2:
        return {
            "trend_analysis_available": False,
            "message": "At least two states are required."
        }

    temperatures = [
        state.engine.temperature_c
        for state in history
    ]

    rpm_values = [
        state.engine.rpm
        for state in history
    ]

    hydraulic_pressures = [
        state.hydraulics.pressure_bar
        for state in history
    ]

    fuel_levels = [
        state.fuel.level_percent
        for state in history
    ]

    load_values = [
        state.operation.load_percentage
        for state in history
    ]

    health_values = [
        state.machine_health_score
        for state in history
    ]

    return {
        "trend_analysis_available": True,

        "states_analyzed": len(history),

        "trends": {
            "engine_temperature": calculate_trend(
                temperatures
            ),

            "engine_rpm": calculate_trend(
                rpm_values
            ),

            "hydraulic_pressure": calculate_trend(
                hydraulic_pressures
            ),

            "fuel_level": calculate_trend(
                fuel_levels
            ),

            "load": calculate_trend(
                load_values
            ),

            "machine_health": calculate_trend(
                health_values
            ),
        }
    }