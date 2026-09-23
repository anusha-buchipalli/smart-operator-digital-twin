import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from digital_twin.twin_engine import DigitalTwinEngine
from digital_twin.state_comparator import compare_states
from digital_twin.trend_analyzer import analyze_trends
from digital_twin.decision_engine import generate_decisions
from digital_twin.recommendation_engine import RecommendationEngine
from digital_twin.twin_snapshot import DigitalTwinSnapshot


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Digital Twin",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(

    """
    <style>

    /* Main page */
    .main {
        background-color: #f5f9f7;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Hero */
    .hero {
        padding: 1.5rem 2rem;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #dff5e8,
            #e3f2fd
        );
        border: 1px solid #d4e8dc;
        margin-bottom: 1.5rem;
    }

    /* Machine header card */
    .machine-card {
        padding: 1rem 1.3rem;
        border-radius: 15px;
        background: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    /* Status */
    .status-normal {
        background-color: #dcfce7;
        color: #166534;
        padding: 0.6rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
    }

    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 0.6rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
    }

    .status-critical {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.6rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
    }

    /* Section spacing */
    .section-space {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 0.8rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = Path(
    "data/raw/machine_telemetry.csv"
)


@st.cache_data
def load_data():

    if not DATA_PATH.exists():
        return None

    data = pd.read_csv(
        DATA_PATH
    )

    data["timestamp"] = pd.to_datetime(
        data["timestamp"]
    )

    return data


df = load_data()


if df is None:

    st.error(
        "Telemetry dataset not found at "
        "`data/raw/machine_telemetry.csv`."
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "record_number" not in st.session_state:

    st.session_state.record_number = min(
        99,
        len(df) - 1
    )


if "playing" not in st.session_state:

    st.session_state.playing = False


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🏗️ Digital Twin Controls"
)


st.sidebar.markdown(
    "### Machine"
)

st.sidebar.write(
    "**CAT-SIM-EXC-001**"
)

st.sidebar.caption(
    "Synthetic excavator telemetry"
)


st.sidebar.divider()


# ============================================================
# SIMULATION CONTROLS
# ============================================================

st.sidebar.markdown(
    "### 🎮 Simulation Controls"
)


col_play, col_pause = st.sidebar.columns(2)


with col_play:

    if st.button(
        "▶ Start",
        use_container_width=True
    ):

        st.session_state.playing = True


with col_pause:

    if st.button(
        "⏸ Pause",
        use_container_width=True
    ):

        st.session_state.playing = False


if st.sidebar.button(
    "↻ Reset Simulation",
    use_container_width=True
):

    st.session_state.record_number = 0
    st.session_state.playing = False
    st.rerun()


# ============================================================
# SPEED CONTROL
# ============================================================

simulation_speed = st.sidebar.selectbox(
    "Simulation Speed",
    [
        "Slow",
        "Normal",
        "Fast"
    ],
    index=1
)


speed_settings = {
    "Slow": 1.0,
    "Normal": 0.5,
    "Fast": 0.15
}


# ============================================================
# TELEMETRY SLIDER
# ============================================================

selected_record = st.sidebar.slider(
    "Telemetry Time Point",
    min_value=0,
    max_value=len(df) - 1,
    value=st.session_state.record_number,
    step=1,
    key="telemetry_slider"
)


# Only allow manual slider movement
# when simulation is paused.

if not st.session_state.playing:

    st.session_state.record_number = (
        selected_record
    )


st.sidebar.caption(
    f"{st.session_state.record_number + 1:,} / "
    f"{len(df):,} telemetry records"
)


# ============================================================
# SIMULATION STATUS
# ============================================================

if st.session_state.playing:

    st.sidebar.success(
        "🟢 Simulation running"
    )

else:

    st.sidebar.info(
        "⏸ Simulation paused"
    )


st.sidebar.divider()


# ============================================================
# PIPELINE
# ============================================================

st.sidebar.markdown(
    "### 🔄 Digital Twin Pipeline"
)

st.sidebar.markdown(
    """
    🛰️ **Telemetry**

    ↓

    🧠 **Digital Twin**

    ↓

    📊 **State Analysis**

    ↓

    📈 **Trend Analysis**

    ↓

    🤖 **Decision Engine**

    ↓

    👷 **Operator Recommendation**
    """
)


# ============================================================
# CURRENT RECORD
# ============================================================

record_number = st.session_state.record_number

current_record = df.iloc[
    record_number
]


# ============================================================
# DIGITAL TWIN ENGINE
# ============================================================

engine = DigitalTwinEngine(
    max_history=100
)


selected_records = df.iloc[
    :record_number + 1
]


for _, row in selected_records.iterrows():

    engine.update(
        row.to_dict()
    )


# ============================================================
# MACHINE STATES
# ============================================================

current_state = (
    engine.get_current_state()
)

previous_state = (
    engine.get_previous_state()
)

history = (
    engine.get_history()
)


if current_state is None:

    st.error(
        "Unable to create Digital Twin state."
    )

    st.stop()


# ============================================================
# STATE COMPARISON
# ============================================================

changes = compare_states(
    previous_state,
    current_state
)


# ============================================================
# TREND ANALYSIS
# ============================================================

trend_result = analyze_trends(
    history
)


if (
    isinstance(trend_result, dict)
    and "trends" in trend_result
):

    trends = trend_result["trends"]

else:

    trends = trend_result


# ============================================================
# DECISION ENGINE
# ============================================================

decisions = generate_decisions(
    current_state,
    trends,
    changes
)


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

recommendation_engine = (
    RecommendationEngine()
)


recommendations = (
    recommendation_engine
    .get_recommendations(
        decisions
    )
)


# ============================================================
# SNAPSHOT
# ============================================================

snapshot = DigitalTwinSnapshot(
    current_state=current_state,
    previous_state=previous_state,
    trends=trend_result,
    changes=changes,
    decisions=decisions,
    recommendations=recommendations
)


# ============================================================
# TELEMETRY VALUES
# ============================================================

machine_id = current_record[
    "machine_id"
]

timestamp = current_record[
    "timestamp"
]

scenario = current_record[
    "scenario"
]

engine_temperature = float(
    current_record[
        "engine_temperature_c"
    ]
)

engine_rpm = float(
    current_record[
        "engine_rpm"
    ]
)

hydraulic_pressure = float(
    current_record[
        "hydraulic_pressure_bar"
    ]
)

fuel_consumption = float(
    current_record[
        "fuel_consumption_lph"
    ]
)

fuel_level = float(
    current_record[
        "fuel_level_percent"
    ]
)

load = float(
    current_record[
        "load_percentage"
    ]
)

idle_time = float(
    current_record[
        "idle_time_minutes"
    ]
)

speed = float(
    current_record[
        "machine_speed_kmh"
    ]
)

machine_health = float(
    current_record[
        "machine_health_score"
    ]
)

seatbelt_fastened = bool(
    current_record[
        "seatbelt_fastened"
    ]
)

operator_present = bool(
    current_record[
        "operator_present"
    ]
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

    <h1>🏗️ AI-Assisted Digital Twin</h1>

    <p>
    Construction Equipment Monitoring
    & Operator Assistance
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MACHINE HEADER
# ============================================================

header_left, header_right = st.columns(
    [3, 1]
)


with header_left:

    st.subheader(
        f"Machine: {machine_id}"
    )

    st.caption(
        f"Telemetry: {timestamp}"
    )

    st.caption(
        f"Operating scenario: {scenario}"
    )


with header_right:

    status = snapshot.overall_status


    if status == "CRITICAL":

        st.error(
            "🔴 MACHINE CRITICAL"
        )

    elif status == "WARNING":

        st.warning(
            "🟡 MACHINE WARNING"
        )

    else:

        st.success(
            "🟢 MACHINE NORMAL"
        )


# ============================================================
# LIVE MACHINE STATE
# ============================================================

st.markdown(
    "## 📊 Live Machine State"
)


metric1, metric2, metric3, metric4 = st.columns(
    4
)


with metric1:

    st.metric(
        "🌡️ Engine Temperature",
        f"{engine_temperature:.1f} °C"
    )


with metric2:

    st.metric(
        "⚙️ Engine RPM",
        f"{engine_rpm:.0f}"
    )


with metric3:

    st.metric(
        "💧 Hydraulic Pressure",
        f"{hydraulic_pressure:.1f} bar"
    )


with metric4:

    st.metric(
        "⛽ Fuel Level",
        f"{fuel_level:.1f}%"
    )


metric5, metric6, metric7, metric8 = st.columns(
    4
)


with metric5:

    st.metric(
        "🏋️ Load",
        f"{load:.1f}%"
    )


with metric6:

    st.metric(
        "🚜 Speed",
        f"{speed:.1f} km/h"
    )


with metric7:

    st.metric(
        "⏱️ Idle Time",
        f"{idle_time:.1f} min"
    )


with metric8:

    st.metric(
        "❤️ Machine Health",
        f"{machine_health:.1f}/100"
    )


# ============================================================
# OPERATOR ASSISTANT
# ============================================================

st.markdown(
    "## 🤖 Digital Twin Operator Assistant"
)


if recommendations:

    for recommendation in recommendations:

        priority = recommendation[
            "priority"
        ]

        title = recommendation[
            "title"
        ]

        message = recommendation[
            "message"
        ]

        reason = recommendation[
            "reason"
        ]

        action = recommendation[
            "action"
        ]


        if priority == "CRITICAL":

            with st.container(
                border=True
            ):

                st.error(
                    f"🚨 {title}"
                )

                st.write(
                    message
                )

                st.markdown(
                    "**Why?**"
                )

                st.write(
                    reason
                )

                st.markdown(
                    "**Recommended Action**"
                )

                st.warning(
                    action
                )


        elif priority == "WARNING":

            with st.container(
                border=True
            ):

                st.warning(
                    f"⚠️ {title}"
                )

                st.write(
                    message
                )

                st.markdown(
                    "**Why?**"
                )

                st.write(
                    reason
                )

                st.markdown(
                    "**Recommended Action**"
                )

                st.info(
                    action
                )


        else:

            with st.container(
                border=True
            ):

                st.success(
                    f"✅ {title}"
                )

                st.write(
                    message
                )

                st.markdown(
                    "**Why?**"
                )

                st.write(
                    reason
                )

                st.markdown(
                    "**Recommended Action**"
                )

                st.info(
                    action
                )


# ============================================================
# RECENT HISTORY
# ============================================================

chart_history = df.iloc[
    max(
        0,
        record_number - 99
    ):
    record_number + 1
].copy()


# ============================================================
# MACHINE TRENDS
# ============================================================

st.markdown(
    "## 📈 Machine Trends"
)


chart1, chart2 = st.columns(
    2
)


# ============================================================
# ENGINE TEMPERATURE
# ============================================================

with chart1:

    st.markdown(
        "#### 🌡️ Engine Temperature"
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.plot(
        chart_history["timestamp"],
        chart_history[
            "engine_temperature_c"
        ]
    )

    ax.axhline(
        100,
        linestyle="--",
        label="Warning"
    )

    ax.axhline(
        120,
        linestyle="--",
        label="Critical"
    )

    ax.set_ylabel(
        "Temperature (°C)"
    )

    ax.set_xlabel(
        "Time"
    )

    ax.legend()

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# ============================================================
# MACHINE HEALTH
# ============================================================

with chart2:

    st.markdown(
        "#### ❤️ Machine Health"
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.plot(
        chart_history["timestamp"],
        chart_history[
            "machine_health_score"
        ]
    )

    ax.axhline(
        80,
        linestyle="--",
        label="Warning"
    )

    ax.set_ylabel(
        "Health Score"
    )

    ax.set_xlabel(
        "Time"
    )

    ax.legend()

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# ============================================================
# LOAD + HYDRAULICS
# ============================================================

chart3, chart4 = st.columns(
    2
)


with chart3:

    st.markdown(
        "#### 🏋️ Operating Load"
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.plot(
        chart_history["timestamp"],
        chart_history[
            "load_percentage"
        ]
    )

    ax.axhline(
        80,
        linestyle="--",
        label="Heavy Load"
    )

    ax.axhline(
        95,
        linestyle="--",
        label="Critical Load"
    )

    ax.set_ylabel(
        "Load (%)"
    )

    ax.set_xlabel(
        "Time"
    )

    ax.legend()

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


with chart4:

    st.markdown(
        "#### 💧 Hydraulic Pressure"
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.plot(
        chart_history["timestamp"],
        chart_history[
            "hydraulic_pressure_bar"
        ]
    )

    ax.axhline(
        100,
        linestyle="--",
        label="Low Pressure"
    )

    ax.axhline(
        350,
        linestyle="--",
        label="High Pressure"
    )

    ax.set_ylabel(
        "Pressure (bar)"
    )

    ax.set_xlabel(
        "Time"
    )

    ax.legend()

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# ============================================================
# AI TREND INTERPRETATION
# ============================================================

st.markdown(
    "## 🧠 Trend Analysis"
)

trend_columns = st.columns(
    6
)


trend_items = [
    (
        "Engine Temp",
        trends.get(
            "engine_temperature",
            "N/A"
        )
    ),
    (
        "RPM",
        trends.get(
            "engine_rpm",
            "N/A"
        )
    ),
    (
        "Hydraulic",
        trends.get(
            "hydraulic_pressure",
            "N/A"
        )
    ),
    (
        "Fuel",
        trends.get(
            "fuel_level",
            "N/A"
        )
    ),
    (
        "Load",
        trends.get(
            "load",
            "N/A"
        )
    ),
    (
        "Health",
        trends.get(
            "machine_health",
            "N/A"
        )
    )
]


for column, (
    name,
    trend
) in zip(
    trend_columns,
    trend_items
):

    with column:

        if trend == "RISING":

            icon = "📈"

        elif trend == "FALLING":

            icon = "📉"

        elif trend == "STABLE":

            icon = "➡️"

        else:

            icon = "❓"


        st.metric(
            name,
            f"{icon} {trend}"
        )


# ============================================================
# OPERATING CONDITIONS
# ============================================================

st.markdown(
    "## ⚙️ Operating Conditions"
)


condition1, condition2, condition3, condition4 = st.columns(
    4
)


with condition1:

    st.metric(
        "Engine Status",
        str(
            current_state.engine.status
        )
    )


with condition2:

    st.metric(
        "Hydraulic Status",
        str(
            current_state.hydraulics.status
        )
    )


with condition3:

    st.metric(
        "Fuel Status",
        str(
            current_state.fuel.status
        )
    )


with condition4:

    st.metric(
        "Operation Status",
        str(
            current_state.operation.status
        )
    )


# ============================================================
# SAFETY
# ============================================================

st.markdown(
    "## 🦺 Safety Status"
)


safety1, safety2 = st.columns(
    2
)


with safety1:

    if operator_present:

        st.success(
            "👷 Operator detected"
        )

    else:

        st.warning(
            "⚠️ No operator detected"
        )


with safety2:

    if seatbelt_fastened:

        st.success(
            "✅ Seatbelt fastened"
        )

    else:

        st.error(
            "🚨 Seatbelt violation"
        )


# ============================================================
# EVENT / ANOMALY INFORMATION
# ============================================================

st.markdown(
    "## 🚨 Current Event Status"
)


event1, event2, event3 = st.columns(
    3
)


with event1:

    anomaly = bool(
        current_record[
            "anomaly_label"
        ]
    )

    if anomaly:

        st.error(
            "🚨 Anomaly Detected"
        )

    else:

        st.success(
            "✅ No Anomaly Detected"
        )


with event2:

    if bool(
        current_record["refueled"]
    ):

        st.info(
            "⛽ Refueling Event"
        )

    else:

        st.write(
            "No refueling event"
        )


with event3:

    st.metric(
        "Fuel Consumption",
        f"{fuel_consumption:.2f} L/h"
    )
# ============================================================
# MACHINE EVENT TIMELINE
# ============================================================

st.markdown(
    "## 🚨 Machine Event Timeline"
)

st.caption(
    "Recent machine events detected from the Digital Twin telemetry."
)


# ------------------------------------------------------------
# Build events from recent telemetry
# ------------------------------------------------------------

timeline_history = df.iloc[
    max(
        0,
        record_number - 99
    ):
    record_number + 1
].copy()


events = []


for _, row in timeline_history.iterrows():

    event_time = row["timestamp"]

    event_scenario = row["scenario"]

    temp = float(
        row["engine_temperature_c"]
    )

    hydraulic = float(
        row["hydraulic_pressure_bar"]
    )

    fuel = float(
        row["fuel_level_percent"]
    )

    load_value = float(
        row["load_percentage"]
    )

    idle = float(
        row["idle_time_minutes"]
    )

    speed_value = float(
        row["machine_speed_kmh"]
    )

    health = float(
        row["machine_health_score"]
    )

    seatbelt = bool(
        row["seatbelt_fastened"]
    )

    operator = bool(
        row["operator_present"]
    )


    # --------------------------------------------------------
    # CRITICAL EVENTS
    # --------------------------------------------------------

    if temp >= 120:

        events.append(
            {
                "timestamp": event_time,
                "severity": "CRITICAL",
                "icon": "🔴",
                "title": "Engine Overheating",
                "reason":
                    f"Engine temperature reached "
                    f"{temp:.1f} °C.",
                "action":
                    "Stop heavy operation and allow "
                    "the engine to cool."
            }
        )


    elif hydraulic > 350:

        events.append(
            {
                "timestamp": event_time,
                "severity": "CRITICAL",
                "icon": "🔴",
                "title": "High Hydraulic Pressure",
                "reason":
                    f"Hydraulic pressure reached "
                    f"{hydraulic:.1f} bar.",
                "action":
                    "Reduce hydraulic load and inspect "
                    "the hydraulic system."
            }
        )


    elif hydraulic < 100:

        events.append(
            {
                "timestamp": event_time,
                "severity": "CRITICAL",
                "icon": "🔴",
                "title": "Low Hydraulic Pressure",
                "reason":
                    f"Hydraulic pressure dropped to "
                    f"{hydraulic:.1f} bar.",
                "action":
                    "Inspect the hydraulic system "
                    "before continuing heavy operation."
            }
        )


    elif operator and not seatbelt:

        events.append(
            {
                "timestamp": event_time,
                "severity": "CRITICAL",
                "icon": "🔴",
                "title": "Seatbelt Safety Violation",
                "reason":
                    "Operator detected without "
                    "seatbelt fastened.",
                "action":
                    "Fasten the seatbelt before "
                    "continuing operation."
            }
        )


    # --------------------------------------------------------
    # WARNING EVENTS
    # --------------------------------------------------------

    elif temp >= 100:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Engine Temperature Warning",
                "reason":
                    f"Engine temperature reached "
                    f"{temp:.1f} °C.",
                "action":
                    "Reduce load and monitor "
                    "engine temperature."
            }
        )


    elif load_value >= 95:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Critical Operating Load",
                "reason":
                    f"Machine load reached "
                    f"{load_value:.1f}%.",
                "action":
                    "Reduce the operating load "
                    "to prevent machine stress."
            }
        )


    elif load_value >= 80:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Heavy Load",
                "reason":
                    f"Machine load reached "
                    f"{load_value:.1f}%.",
                "action":
                    "Monitor machine load and "
                    "avoid prolonged heavy operation."
            }
        )


    elif idle >= 15 and speed_value == 0:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Excessive Idling",
                "reason":
                    f"Machine has been idle for "
                    f"{idle:.1f} minutes.",
                "action":
                    "Reduce unnecessary idling "
                    "to improve fuel efficiency."
            }
        )


    elif fuel <= 10:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Critically Low Fuel",
                "reason":
                    f"Fuel level dropped to "
                    f"{fuel:.1f}%.",
                "action":
                    "Refuel the machine soon."
            }
        )


    elif fuel <= 20:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Low Fuel",
                "reason":
                    f"Fuel level is "
                    f"{fuel:.1f}%.",
                "action":
                    "Plan a refueling stop."
            }
        )


    elif health < 80:

        events.append(
            {
                "timestamp": event_time,
                "severity": "WARNING",
                "icon": "🟡",
                "title": "Machine Health Declining",
                "reason":
                    f"Machine health score is "
                    f"{health:.1f}/100.",
                "action":
                    "Inspect the machine and "
                    "monitor health indicators."
            }
        )


# ------------------------------------------------------------
# Remove consecutive duplicate events
# ------------------------------------------------------------

filtered_events = []

previous_event_key = None


for event in events:

    event_key = (
        event["title"]
    )

    if event_key != previous_event_key:

        filtered_events.append(
            event
        )

        previous_event_key = event_key


# ------------------------------------------------------------
# Display timeline
# ------------------------------------------------------------

if filtered_events:

    # Show newest events first

    display_events = filtered_events[
        ::-1
    ][:10]


    for event in display_events:

        severity = event[
            "severity"
        ]


        if severity == "CRITICAL":

            with st.container(
                border=True
            ):

                st.error(
                    f'{event["icon"]} '
                    f'{event["title"]}'
                )

                st.caption(
                    event["timestamp"]
                )

                st.write(
                    f'**Why:** '
                    f'{event["reason"]}'
                )

                st.write(
                    f'**Action:** '
                    f'{event["action"]}'
                )


        else:

            with st.container(
                border=True
            ):

                st.warning(
                    f'{event["icon"]} '
                    f'{event["title"]}'
                )

                st.caption(
                    event["timestamp"]
                )

                st.write(
                    f'**Why:** '
                    f'{event["reason"]}'
                )

                st.write(
                    f'**Action:** '
                    f'{event["action"]}'
                )


else:

    st.success(
        "🟢 No machine events detected "
        "in the current telemetry window."
    )


# ------------------------------------------------------------
# Event summary
# ------------------------------------------------------------

critical_events = sum(
    1
    for event in filtered_events
    if event["severity"] == "CRITICAL"
)

warning_events = sum(
    1
    for event in filtered_events
    if event["severity"] == "WARNING"
)


summary1, summary2, summary3 = st.columns(
    3
)


with summary1:

    st.metric(
        "Total Events",
        len(filtered_events)
    )


with summary2:

    st.metric(
        "Critical Events",
        critical_events
    )


with summary3:

    st.metric(
        "Warning Events",
        warning_events
    )

# ============================================================
# DIGITAL TWIN DETAILS
# ============================================================

st.markdown(
    "## 🔍 Digital Twin Details"
)


with st.expander(
    "View Digital Twin State"
):

    st.json(
        current_state.to_dict()
    )


with st.expander(
    "View AI Decisions"
):

    st.json(
        decisions
    )


with st.expander(
    "View Operator Recommendations"
):

    st.json(
        recommendations
    )


with st.expander(
    "View State Changes"
):

    st.json(
        changes
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Assisted Digital Twin for Construction Equipment "
    "| Supervised Operator Assistance Prototype"
)


# ============================================================
# AUTO PLAY
# ============================================================

if st.session_state.playing:

    if st.session_state.record_number < len(df) - 1:

        time.sleep(
            speed_settings[
                simulation_speed
            ]
        )

        st.session_state.record_number += 1

        st.rerun()

    else:

        st.session_state.playing = False

        st.success(
            "🏁 Simulation completed."
        )