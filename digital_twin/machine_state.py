from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class EngineState:
    rpm: float
    temperature_c: float
    status: str


@dataclass
class HydraulicState:
    pressure_bar: float
    status: str


@dataclass
class FuelState:
    level_percent: float
    consumption_lph: float
    status: str


@dataclass
class OperationState:
    load_percentage: float
    speed_kmh: float
    idle_time_minutes: float
    status: str


@dataclass
class SafetyState:
    seatbelt_fastened: bool
    operator_present: bool
    status: str


@dataclass
class MachineState:
    machine_id: str
    timestamp: str
    overall_status: str

    engine: EngineState
    hydraulics: HydraulicState
    fuel: FuelState
    operation: OperationState
    safety: SafetyState

    machine_health_score: float
    anomaly_detected: bool
    scenario: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Digital Twin state into a dictionary.
        """
        return asdict(self)