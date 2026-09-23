from typing import Dict, Any, Optional

from digital_twin.machine_state import MachineState


def compare_states(
    previous: Optional[MachineState],
    current: MachineState
) -> Dict[str, Any]:
    """
    Compare two Digital Twin states and identify
    important changes between them.
    """

    # No previous state means there is nothing to compare.
    if previous is None:
        return {
            "comparison_available": False,
            "message": "No previous state available."
        }

    temperature_change = (
        current.engine.temperature_c
        - previous.engine.temperature_c
    )

    rpm_change = (
        current.engine.rpm
        - previous.engine.rpm
    )

    pressure_change = (
        current.hydraulics.pressure_bar
        - previous.hydraulics.pressure_bar
    )

    fuel_level_change = (
        current.fuel.level_percent
        - previous.fuel.level_percent
    )

    load_change = (
        current.operation.load_percentage
        - previous.operation.load_percentage
    )

    speed_change = (
        current.operation.speed_kmh
        - previous.operation.speed_kmh
    )

    health_change = (
        current.machine_health_score
        - previous.machine_health_score
    )

    status_changed = (
        previous.overall_status
        != current.overall_status
    )

    engine_status_changed = (
        previous.engine.status
        != current.engine.status
    )

    hydraulic_status_changed = (
        previous.hydraulics.status
        != current.hydraulics.status
    )

    fuel_status_changed = (
        previous.fuel.status
        != current.fuel.status
    )

    operation_status_changed = (
        previous.operation.status
        != current.operation.status
    )

    safety_status_changed = (
        previous.safety.status
        != current.safety.status
    )

    return {
        "comparison_available": True,

        "previous_timestamp": previous.timestamp,
        "current_timestamp": current.timestamp,

        "changes": {
            "engine_temperature_c": round(
                temperature_change, 2
            ),

            "engine_rpm": round(
                rpm_change, 2
            ),

            "hydraulic_pressure_bar": round(
                pressure_change, 2
            ),

            "fuel_level_percent": round(
                fuel_level_change, 2
            ),

            "load_percentage": round(
                load_change, 2
            ),

            "speed_kmh": round(
                speed_change, 2
            ),

            "machine_health_score": round(
                health_change, 2
            ),
        },

        "status_changes": {
            "overall": status_changed,
            "engine": engine_status_changed,
            "hydraulics": hydraulic_status_changed,
            "fuel": fuel_status_changed,
            "operation": operation_status_changed,
            "safety": safety_status_changed,
        },

        "states": {
            "overall": {
                "previous": previous.overall_status,
                "current": current.overall_status,
            },

            "engine": {
                "previous": previous.engine.status,
                "current": current.engine.status,
            },

            "hydraulics": {
                "previous": previous.hydraulics.status,
                "current": current.hydraulics.status,
            },

            "fuel": {
                "previous": previous.fuel.status,
                "current": current.fuel.status,
            },

            "operation": {
                "previous": previous.operation.status,
                "current": current.operation.status,
            },

            "safety": {
                "previous": previous.safety.status,
                "current": current.safety.status,
            },
        }
    }