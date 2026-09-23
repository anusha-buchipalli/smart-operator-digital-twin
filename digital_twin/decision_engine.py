from typing import Dict, Any, List

from digital_twin.machine_state import MachineState


def generate_decisions(
    current_state: MachineState,
    trends: Dict[str, str],
    changes: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Generate operator-oriented decisions from the current
    Digital Twin state, recent trends, and state changes.
    """

    decisions = []

    # -----------------------------------------------------
    # 1. Critical engine temperature
    # -----------------------------------------------------

    if current_state.engine.temperature_c >= 120:

        decisions.append({
            "severity": "CRITICAL",
            "issue": "CRITICAL_ENGINE_TEMPERATURE",
            "reason": (
                f"Engine temperature is "
                f"{current_state.engine.temperature_c:.1f}°C."
            ),
            "recommended_action": (
                "Stop heavy operation and allow the engine to cool. "
                "Inspect the cooling system before continuing."
            )
        })

    # -----------------------------------------------------
    # 2. Increasing engine temperature
    # -----------------------------------------------------

    elif (
        current_state.engine.temperature_c >= 100
        and trends.get("engine_temperature") == "RISING"
    ):

        decisions.append({
            "severity": "WARNING",
            "issue": "INCREASING_ENGINE_TEMPERATURE",
            "reason": (
                "Engine temperature is elevated and continuing to rise."
            ),
            "recommended_action": (
                "Reduce machine load and monitor engine temperature."
            )
        })

    # -----------------------------------------------------
    # 3. High hydraulic pressure
    # -----------------------------------------------------

    if current_state.hydraulics.pressure_bar > 350:

        decisions.append({
            "severity": "CRITICAL",
            "issue": "HIGH_HYDRAULIC_PRESSURE",
            "reason": (
                f"Hydraulic pressure is "
                f"{current_state.hydraulics.pressure_bar:.1f} bar."
            ),
            "recommended_action": (
                "Stop hydraulic operation and inspect the hydraulic system."
            )
        })

    # -----------------------------------------------------
    # 4. Low hydraulic pressure
    # -----------------------------------------------------

    elif current_state.hydraulics.pressure_bar < 100:

        decisions.append({
            "severity": "CRITICAL",
            "issue": "LOW_HYDRAULIC_PRESSURE",
            "reason": (
                f"Hydraulic pressure is "
                f"{current_state.hydraulics.pressure_bar:.1f} bar."
            ),
            "recommended_action": (
                "Stop operation and inspect the hydraulic system."
            )
        })

    # -----------------------------------------------------
    # 5. Heavy load
    # -----------------------------------------------------

    if current_state.operation.load_percentage >= 80:

        decisions.append({
            "severity": "WARNING",
            "issue": "HEAVY_LOAD",
            "reason": (
                f"Machine load is "
                f"{current_state.operation.load_percentage:.1f}%."
            ),
            "recommended_action": (
                "Reduce load if possible and avoid prolonged "
                "operation at high load."
            )
        })

    # -----------------------------------------------------
    # 6. Excessive idling
    # -----------------------------------------------------

    if (
        current_state.operation.idle_time_minutes >= 15
        and current_state.operation.speed_kmh == 0
    ):

        decisions.append({
            "severity": "WARNING",
            "issue": "EXCESSIVE_IDLE",
            "reason": (
                f"Machine has been idle for "
                f"{current_state.operation.idle_time_minutes:.1f} minutes."
            ),
            "recommended_action": (
                "Stop the engine if operation is not required."
            )
        })

    # -----------------------------------------------------
    # 7. Fuel efficiency
    # -----------------------------------------------------

    if current_state.fuel.consumption_lph >= 14:

        decisions.append({
            "severity": "WARNING",
            "issue": "HIGH_FUEL_CONSUMPTION",
            "reason": (
                f"Fuel consumption is "
                f"{current_state.fuel.consumption_lph:.1f} L/h."
            ),
            "recommended_action": (
                "Reduce unnecessary high-load operation and "
                "check operating conditions."
            )
        })

    # -----------------------------------------------------
    # 8. Low fuel
    # -----------------------------------------------------

    if current_state.fuel.level_percent <= 10:

        decisions.append({
            "severity": "CRITICAL",
            "issue": "CRITICAL_LOW_FUEL",
            "reason": (
                f"Fuel level is "
                f"{current_state.fuel.level_percent:.1f}%."
            ),
            "recommended_action": (
                "Refuel the machine before continuing extended operation."
            )
        })

    elif current_state.fuel.level_percent <= 20:

        decisions.append({
            "severity": "WARNING",
            "issue": "LOW_FUEL",
            "reason": (
                f"Fuel level is "
                f"{current_state.fuel.level_percent:.1f}%."
            ),
            "recommended_action": (
                "Plan refueling soon."
            )
        })

    # -----------------------------------------------------
    # 9. Safety violation
    # -----------------------------------------------------

    if (
        current_state.safety.operator_present
        and not current_state.safety.seatbelt_fastened
    ):

        decisions.append({
            "severity": "CRITICAL",
            "issue": "SEATBELT_VIOLATION",
            "reason": (
                "Operator is present but the seatbelt is not fastened."
            ),
            "recommended_action": (
                "Fasten the seatbelt before continuing machine operation."
            )
        })

    # -----------------------------------------------------
    # 10. Falling machine health
    # -----------------------------------------------------

    if (
        current_state.machine_health_score < 80
        and trends.get("machine_health") == "FALLING"
    ):

        decisions.append({
            "severity": "WARNING",
            "issue": "DECLINING_MACHINE_HEALTH",
            "reason": (
                "Machine health is below the normal range "
                "and continuing to decline."
            ),
            "recommended_action": (
                "Reduce machine stress and inspect the machine "
                "for developing issues."
            )
        })

    # -----------------------------------------------------
    # 11. No detected issues
    # -----------------------------------------------------

    if not decisions:

        decisions.append({
            "severity": "NORMAL",
            "issue": "NO_ACTIVE_ISSUES",
            "reason": "Machine parameters are within expected limits.",
            "recommended_action": (
                "Continue operation while monitoring machine telemetry."
            )
        })

    return decisions