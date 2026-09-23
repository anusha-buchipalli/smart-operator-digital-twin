"""
Operator Recommendation Engine

Converts Digital Twin decisions into
simple operator-facing messages.
"""


class RecommendationEngine:

    # --------------------------------------------------
    # Human-friendly titles for Decision Engine issues
    # --------------------------------------------------

    TITLES = {

        "CRITICAL_ENGINE_TEMPERATURE":
            "Engine Overheating",

        "INCREASING_ENGINE_TEMPERATURE":
            "Engine Temperature Rising",

        "HIGH_HYDRAULIC_PRESSURE":
            "High Hydraulic Pressure",

        "LOW_HYDRAULIC_PRESSURE":
            "Low Hydraulic Pressure",

        "HEAVY_LOAD":
            "Heavy Load",

        "EXCESSIVE_IDLE":
            "Excessive Idling",

        "HIGH_FUEL_CONSUMPTION":
            "High Fuel Consumption",

        "CRITICAL_LOW_FUEL":
            "Critically Low Fuel",

        "LOW_FUEL":
            "Low Fuel",

        "SEATBELT_VIOLATION":
            "Seatbelt Safety Violation",

        "DECLINING_MACHINE_HEALTH":
            "Machine Health Declining",

        "NO_ACTIVE_ISSUES":
            "Machine Operating Normally"
    }

    # --------------------------------------------------
    # Convert one Decision Engine result into an
    # operator-friendly recommendation
    # --------------------------------------------------

    def get_recommendation(self, decision):

        issue = decision.get("issue")

        severity = decision.get(
            "severity",
            "UNKNOWN"
        )

        reason = decision.get(
            "reason",
            "The Digital Twin detected a machine condition."
        )

        action = decision.get(
            "recommended_action",
            "Inspect the machine condition."
        )

        # Get a human-friendly title.
        # If the issue is not known, use a generic title
        # instead of saying "Unknown Machine Condition".

        title = self.TITLES.get(
            issue,
            "Machine Condition Detected"
        )

        # --------------------------------------------------
        # Create operator-friendly message
        # --------------------------------------------------

        if severity == "CRITICAL":

            message = (
                f"Critical machine condition detected: "
                f"{title}."
            )

        elif severity == "WARNING":

            message = (
                f"Machine condition requires attention: "
                f"{title}."
            )

        elif severity == "NORMAL":

            message = (
                "Machine is operating within "
                "expected conditions."
            )

        else:

            message = (
                f"Machine condition detected: "
                f"{title}."
            )

        # --------------------------------------------------
        # Return structured recommendation
        # --------------------------------------------------

        return {
            "priority": severity,
            "title": title,
            "message": message,
            "action": action,
            "reason": reason,
            "decision_issue": issue
        }

    # --------------------------------------------------
    # Convert multiple decisions
    # --------------------------------------------------

    def get_recommendations(self, decisions):

        return [
            self.get_recommendation(decision)
            for decision in decisions
        ]

    # --------------------------------------------------
    # Find the most important recommendation
    # --------------------------------------------------

    def get_highest_priority(self, recommendations):

        priority_order = {
            "CRITICAL": 3,
            "WARNING": 2,
            "NORMAL": 1,
            "UNKNOWN": 0
        }

        if not recommendations:
            return None

        return max(
            recommendations,
            key=lambda recommendation:
            priority_order.get(
                recommendation["priority"],
                0
            )
        )