from typing import Dict, Any, List, Optional, Tuple

from digital_twin.machine_state import MachineState
from digital_twin.state_mapper import map_telemetry_to_state


class DigitalTwinEngine:
    """
    Core Digital Twin engine.

    Converts raw machine telemetry into structured
    MachineState objects and maintains the machine's
    recent digital history.
    """

    def __init__(self, max_history: int = 100):
        self.current_state: Optional[MachineState] = None
        self.history: List[MachineState] = []
        self.max_history = max_history

    def update(self, telemetry: Dict[str, Any]) -> MachineState:
        """
        Process a new telemetry record and update
        the Digital Twin state.
        """

        new_state = map_telemetry_to_state(telemetry)

        self.current_state = new_state

        self.history.append(new_state)

        # Keep only the most recent states
        if len(self.history) > self.max_history:
            self.history.pop(0)

        return new_state

    def get_current_state(self) -> Optional[MachineState]:
        """
        Return the current Digital Twin state.
        """

        return self.current_state

    def get_previous_state(self) -> Optional[MachineState]:
        """
        Return the state immediately before the current state.
        """

        if len(self.history) < 2:
            return None

        return self.history[-2]

    def get_history(self) -> List[MachineState]:
        """
        Return the stored Digital Twin history.
        """

        return self.history

    def get_recent_history(
        self,
        count: int = 10
    ) -> List[MachineState]:
        """
        Return the most recent N machine states.
        """

        if count <= 0:
            return []

        return self.history[-count:]

    def get_current_and_previous(
        self
    ) -> Tuple[Optional[MachineState], Optional[MachineState]]:
        """
        Return the current and previous Digital Twin states.
        """

        return (
            self.get_current_state(),
            self.get_previous_state()
        )

    def get_history_as_dicts(self) -> List[Dict[str, Any]]:
        """
        Convert Digital Twin history into dictionaries.
        """

        return [
            state.to_dict()
            for state in self.history
        ]

    def reset(self) -> None:
        """
        Reset the Digital Twin state and history.
        """

        self.current_state = None
        self.history.clear()