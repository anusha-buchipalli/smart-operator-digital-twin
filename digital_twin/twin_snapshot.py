"""
Digital Twin Snapshot

Combines the current machine state, trends, changes,
decisions, and operator recommendations into one
structured object for the application/dashboard.
"""

from typing import Dict, Any, List, Optional

from digital_twin.machine_state import MachineState


class DigitalTwinSnapshot:
    """
    Represents one complete view of the Digital Twin
    at a particular point in time.
    """

    def __init__(
        self,
        current_state: MachineState,
        previous_state: Optional[MachineState],
        trends: Dict[str, str],
        changes: Dict[str, Any],
        decisions: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]]
    ):

        self.current_state = current_state
        self.previous_state = previous_state
        self.trends = trends
        self.changes = changes
        self.decisions = decisions
        self.recommendations = recommendations

    # --------------------------------------------------
    # Machine status
    # --------------------------------------------------

    @property
    def machine_id(self):
        return self.current_state.machine_id

    @property
    def timestamp(self):
        return self.current_state.timestamp

    @property
    def overall_status(self):
        return self.current_state.overall_status

    @property
    def machine_health(self):
        return self.current_state.machine_health_score

    # --------------------------------------------------
    # Active issues
    # --------------------------------------------------

    def get_active_issues(self) -> List[Dict[str, Any]]:
        """
        Return only actual machine issues.

        The normal 'NO_ACTIVE_ISSUES' decision is excluded.
        """

        return [
            decision
            for decision in self.decisions
            if decision.get("issue") != "NO_ACTIVE_ISSUES"
        ]

    # --------------------------------------------------
    # Highest priority issue
    # --------------------------------------------------

    def get_highest_priority_recommendation(
        self
    ) -> Optional[Dict[str, Any]]:

        if not self.recommendations:
            return None

        priority_order = {
            "CRITICAL": 3,
            "WARNING": 2,
            "NORMAL": 1,
            "UNKNOWN": 0
        }

        return max(
            self.recommendations,
            key=lambda recommendation:
            priority_order.get(
                recommendation.get("priority"),
                0
            )
        )

    # --------------------------------------------------
    # Convert snapshot into a dictionary
    # --------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        state = self.current_state

        highest_priority = (
            self.get_highest_priority_recommendation()
        )

        return {

            # ------------------------------------------
            # Machine information
            # ------------------------------------------

            "machine": {
                "machine_id": state.machine_id,
                "timestamp": state.timestamp,
                "scenario": state.scenario,
                "overall_status": state.overall_status,
                "machine_health": state.machine_health_score
            },

            # ------------------------------------------
            # Engine
            # ------------------------------------------

            "engine": {
                "rpm": state.engine.rpm,
                "temperature_c":
                    state.engine.temperature_c,
                "status":
                    state.engine.status
            },

            # ------------------------------------------
            # Hydraulics
            # ------------------------------------------

            "hydraulics": {
                "pressure_bar":
                    state.hydraulics.pressure_bar,
                "status":
                    state.hydraulics.status
            },

            # ------------------------------------------
            # Fuel
            # ------------------------------------------

            "fuel": {
                "level_percent":
                    state.fuel.level_percent,
                "consumption_lph":
                    state.fuel.consumption_lph,
                "status":
                    state.fuel.status
            },

            # ------------------------------------------
            # Operation
            # ------------------------------------------

            "operation": {
                "load_percentage":
                    state.operation.load_percentage,
                "speed_kmh":
                    state.operation.speed_kmh,
                "idle_time_minutes":
                    state.operation.idle_time_minutes,
                "status":
                    state.operation.status
            },

            # ------------------------------------------
            # Safety
            # ------------------------------------------

            "safety": {
                "operator_present":
                    state.safety.operator_present,
                "seatbelt_fastened":
                    state.safety.seatbelt_fastened,
                "status":
                    state.safety.status
            },

            # ------------------------------------------
            # Trends
            # ------------------------------------------

            "trends": self.trends,

            # ------------------------------------------
            # State changes
            # ------------------------------------------

            "changes": self.changes,

            # ------------------------------------------
            # Decisions
            # ------------------------------------------

            "decisions": self.decisions,

            # ------------------------------------------
            # Recommendations
            # ------------------------------------------

            "recommendations":
                self.recommendations,

            # ------------------------------------------
            # Highest priority recommendation
            # ------------------------------------------

            "highest_priority_recommendation":
                highest_priority
        }