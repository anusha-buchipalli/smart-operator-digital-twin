import pandas as pd

from digital_twin.twin_engine import DigitalTwinEngine
from digital_twin.state_comparator import compare_states
from digital_twin.trend_analyzer import analyze_trends
from digital_twin.decision_engine import generate_decisions
from digital_twin.recommendation_engine import RecommendationEngine


DATA_PATH = "data/raw/machine_telemetry.csv"


def main():

    print("=" * 70)
    print("DIGITAL TWIN END-TO-END PIPELINE TEST")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Load telemetry
    # --------------------------------------------------

    print("\n[1] Loading machine telemetry...")

    df = pd.read_csv(DATA_PATH)

    print(f"Records loaded: {len(df):,}")

    # --------------------------------------------------
    # 2. Create Digital Twin
    # --------------------------------------------------

    twin = DigitalTwinEngine(max_history=100)

    recommendation_engine = RecommendationEngine()

    detected_conditions = []

    # --------------------------------------------------
    # 3. Process telemetry
    # --------------------------------------------------

    print("\n[2] Processing telemetry...")

    for _, row in df.iterrows():

        telemetry = row.to_dict()

        # Update Digital Twin
        current_state = twin.update(telemetry)

        # Get previous state
        previous_state = twin.get_previous_state()

        # Get recent history
        history = twin.get_history()

        # ----------------------------------------------
        # State comparison
        # ----------------------------------------------

        changes = compare_states(
            previous_state,
            current_state
        )

        # ----------------------------------------------
        # Trend analysis
        # ----------------------------------------------

        trends = analyze_trends(history)

        # ----------------------------------------------
        # Decision Engine
        # ----------------------------------------------

        decisions = generate_decisions(
            current_state,
            trends,
            changes
        )

        # ----------------------------------------------
        # Recommendation Engine
        # ----------------------------------------------

        recommendations = (
            recommendation_engine
            .get_recommendations(decisions)
        )

        # ----------------------------------------------
        # Store non-normal conditions
        # ----------------------------------------------

        for decision, recommendation in zip(
            decisions,
            recommendations
        ):

            if decision["issue"] != "NO_ACTIVE_ISSUES":

                detected_conditions.append(
                    {
                        "timestamp": current_state.timestamp,
                        "scenario": current_state.scenario,
                        "issue": decision["issue"],
                        "severity": decision["severity"],
                        "title": recommendation["title"],
                        "action": recommendation["action"]
                    }
                )

    # --------------------------------------------------
    # 4. Results
    # --------------------------------------------------

    print("\n[3] Pipeline processing completed.")

    print(
        f"Total telemetry records: "
        f"{len(df):,}"
    )

    print(
        f"Conditions detected: "
        f"{len(detected_conditions):,}"
    )

    # --------------------------------------------------
    # 5. Sample alerts
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("SAMPLE OPERATOR ALERTS")
    print("=" * 70)

    for alert in detected_conditions[:10]:

        print("\n" + "-" * 70)

        print(
            f"Timestamp : {alert['timestamp']}"
        )

        print(
            f"Scenario  : {alert['scenario']}"
        )

        print(
            f"Severity  : {alert['severity']}"
        )

        print(
            f"Problem   : {alert['title']}"
        )

        print(
            f"Action    : {alert['action']}"
        )

    # --------------------------------------------------
    # 6. Alert summary
    # --------------------------------------------------

    if detected_conditions:

        alerts_df = pd.DataFrame(
            detected_conditions
        )

        print("\n" + "=" * 70)
        print("ALERT SUMMARY")
        print("=" * 70)

        print("\nBy severity:")

        print(
            alerts_df["severity"]
            .value_counts()
        )

        print("\nTop detected issues:")

        print(
            alerts_df["issue"]
            .value_counts()
            .head(10)
        )

    # --------------------------------------------------
    # 7. Final Digital Twin state
    # --------------------------------------------------

    final_state = twin.get_current_state()

    print("\n" + "=" * 70)
    print("FINAL DIGITAL TWIN STATE")
    print("=" * 70)

    print(
        f"Machine ID      : "
        f"{final_state.machine_id}"
    )

    print(
        f"Timestamp       : "
        f"{final_state.timestamp}"
    )

    print(
        f"Overall Status  : "
        f"{final_state.overall_status}"
    )

    print(
        f"Engine Temp     : "
        f"{final_state.engine.temperature_c:.2f} °C"
    )

    print(
        f"Engine RPM      : "
        f"{final_state.engine.rpm:.2f}"
    )

    print(
        f"Hydraulic Press : "
        f"{final_state.hydraulics.pressure_bar:.2f} bar"
    )

    print(
        f"Fuel Level      : "
        f"{final_state.fuel.level_percent:.2f} %"
    )

    print(
        f"Machine Health  : "
        f"{final_state.machine_health_score:.2f}"
    )

    print("\n" + "=" * 70)
    print("END-TO-END PIPELINE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()