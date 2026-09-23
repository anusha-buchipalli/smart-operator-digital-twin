import pandas as pd

from digital_twin.twin_engine import DigitalTwinEngine
from digital_twin.state_comparator import compare_states
from digital_twin.trend_analyzer import analyze_trends
from digital_twin.decision_engine import generate_decisions
from digital_twin.recommendation_engine import RecommendationEngine
from digital_twin.twin_snapshot import DigitalTwinSnapshot


DATA_PATH = "data/raw/machine_telemetry.csv"


def main():

    print("=" * 70)
    print("DIGITAL TWIN SNAPSHOT TEST")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Load telemetry
    # --------------------------------------------------

    print("\n[1] Loading telemetry...")

    df = pd.read_csv(DATA_PATH)

    print(f"Records available: {len(df):,}")

    # --------------------------------------------------
    # 2. Create Digital Twin components
    # --------------------------------------------------

    twin = DigitalTwinEngine(max_history=100)

    recommendation_engine = RecommendationEngine()

    # --------------------------------------------------
    # 3. Process records
    # --------------------------------------------------

    print("\n[2] Building Digital Twin snapshot...")

    snapshot = None

    # We process the first 100 records because the
    # Digital Twin history is limited to 100 records.

    for _, row in df.head(100).iterrows():

        telemetry = row.to_dict()

        # Update Digital Twin
        current_state = twin.update(telemetry)

        # Previous state
        previous_state = twin.get_previous_state()

        # History
        history = twin.get_history()

        # State comparison
        changes = compare_states(
            previous_state,
            current_state
        )

        # Trend analysis
        trends = analyze_trends(history)

        # Decisions
        decisions = generate_decisions(
            current_state,
            trends,
            changes
        )

        # Operator recommendations
        recommendations = (
            recommendation_engine
            .get_recommendations(decisions)
        )

        # Create snapshot
        snapshot = DigitalTwinSnapshot(
            current_state=current_state,
            previous_state=previous_state,
            trends=trends,
            changes=changes,
            decisions=decisions,
            recommendations=recommendations
        )

    # --------------------------------------------------
    # 4. Check snapshot
    # --------------------------------------------------

    if snapshot is None:

        print("ERROR: Snapshot was not created.")

        return

    print("\n[3] Snapshot successfully created.")

    # --------------------------------------------------
    # 5. Display machine information
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("MACHINE")
    print("=" * 70)

    print(
        f"Machine ID     : "
        f"{snapshot.machine_id}"
    )

    print(
        f"Timestamp      : "
        f"{snapshot.timestamp}"
    )

    print(
        f"Overall Status : "
        f"{snapshot.overall_status}"
    )

    print(
        f"Machine Health : "
        f"{snapshot.machine_health:.2f}"
    )

    # --------------------------------------------------
    # 6. Display engine
    # --------------------------------------------------

    state = snapshot.current_state

    print("\n" + "=" * 70)
    print("ENGINE")
    print("=" * 70)

    print(
        f"RPM            : "
        f"{state.engine.rpm:.2f}"
    )

    print(
        f"Temperature    : "
        f"{state.engine.temperature_c:.2f} °C"
    )

    print(
        f"Status         : "
        f"{state.engine.status}"
    )

    # --------------------------------------------------
    # 7. Display hydraulics
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("HYDRAULICS")
    print("=" * 70)

    print(
        f"Pressure       : "
        f"{state.hydraulics.pressure_bar:.2f} bar"
    )

    print(
        f"Status         : "
        f"{state.hydraulics.status}"
    )

    # --------------------------------------------------
    # 8. Display fuel
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("FUEL")
    print("=" * 70)

    print(
        f"Fuel Level     : "
        f"{state.fuel.level_percent:.2f}%"
    )

    print(
        f"Consumption    : "
        f"{state.fuel.consumption_lph:.2f} L/h"
    )

    print(
        f"Status         : "
        f"{state.fuel.status}"
    )

    # --------------------------------------------------
    # 9. Display operation
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("OPERATION")
    print("=" * 70)

    print(
        f"Load           : "
        f"{state.operation.load_percentage:.2f}%"
    )

    print(
        f"Speed          : "
        f"{state.operation.speed_kmh:.2f} km/h"
    )

    print(
        f"Idle Time      : "
        f"{state.operation.idle_time_minutes:.2f} min"
    )

    print(
        f"Status         : "
        f"{state.operation.status}"
    )

    # --------------------------------------------------
    # 10. Display trends
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("TRENDS")
    print("=" * 70)

    for metric, trend in snapshot.trends.items():

        print(
            f"{metric:25} : {trend}"
        )

    # --------------------------------------------------
    # 11. Display active decisions
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("ACTIVE DECISIONS")
    print("=" * 70)

    active_issues = snapshot.get_active_issues()

    if not active_issues:

        print("No active issues.")

    else:

        for decision in active_issues:

            print(
                f"\n[{decision['severity']}] "
                f"{decision['issue']}"
            )

            print(
                f"Reason : "
                f"{decision['reason']}"
            )

            print(
                f"Action : "
                f"{decision['recommended_action']}"
            )

    # --------------------------------------------------
    # 12. Highest priority recommendation
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("HIGHEST PRIORITY RECOMMENDATION")
    print("=" * 70)

    highest = (
        snapshot
        .get_highest_priority_recommendation()
    )

    if highest is None:

        print("No recommendation available.")

    else:

        print(
            f"Priority : "
            f"{highest['priority']}"
        )

        print(
            f"Title    : "
            f"{highest['title']}"
        )

        print(
            f"Message  : "
            f"{highest['message']}"
        )

        print(
            f"Action   : "
            f"{highest['action']}"
        )

        print(
            f"Reason   : "
            f"{highest['reason']}"
        )

    # --------------------------------------------------
    # 13. Convert complete snapshot to dictionary
    # --------------------------------------------------

    snapshot_dict = snapshot.to_dict()

    print("\n" + "=" * 70)
    print("SNAPSHOT DICTIONARY")
    print("=" * 70)

    print(
        f"Top-level sections: "
        f"{list(snapshot_dict.keys())}"
    )

    print("\nSnapshot test completed successfully.")

    print("=" * 70)


if __name__ == "__main__":
    main()