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

    /* ========================================================
       VISUAL DIGITAL TWIN
       ======================================================== */

    .twin-panel {
        background: linear-gradient(135deg, #ffffff 0%, #f3faf7 55%, #eef7ff 100%);
        border: 1px solid #d8e7df;
        border-radius: 22px;
        padding: 1.25rem;
        margin: 0.5rem 0 1.5rem 0;
        box-shadow: 0 8px 30px rgba(31, 78, 61, 0.08);
    }

    .twin-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }

    .twin-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #16352a;
        margin: 0;
    }

    .twin-subtitle {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    .twin-live-badge {
        padding: 0.42rem 0.8rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.78rem;
        white-space: nowrap;
        border: 1px solid #bbf7d0;
        background: #f0fdf4;
        color: #166534;
    }

    .twin-live-badge.warning {
        border-color: #fde68a;
        background: #fffbeb;
        color: #92400e;
    }

    .twin-live-badge.critical {
        border-color: #fecaca;
        background: #fef2f2;
        color: #991b1b;
        animation: twinPulse 1.4s infinite;
    }

    .twin-body {
        display: grid;
        grid-template-columns: minmax(0, 2.1fr) minmax(230px, 0.9fr);
        gap: 1rem;
        align-items: stretch;
    }

    .twin-machine {
        min-height: 390px;
        border-radius: 18px;
        border: 1px solid #dce8e2;
        background:
            radial-gradient(circle at 50% 45%, rgba(219, 243, 231, 0.75), transparent 42%),
            linear-gradient(180deg, #f9fcfb, #edf7f3);
        overflow: hidden;
        position: relative;
    }

    .twin-machine svg {
        width: 100%;
        height: 100%;
        min-height: 390px;
        display: block;
    }

    /* Pure HTML/CSS excavator - deliberately used instead of SVG so the
       visual remains reliable inside Streamlit's HTML renderer. */
    .excavator-stage {
        position: relative;
        width: 100%;
        height: 390px;
        overflow: hidden;
        background:
            radial-gradient(circle at 48% 42%, rgba(191, 235, 215, 0.72), transparent 38%),
            linear-gradient(180deg, #f9fcfb 0%, #edf7f3 100%);
    }

    .excavator-ground {
        position: absolute;
        left: 6%;
        right: 6%;
        bottom: 44px;
        height: 4px;
        border-radius: 99px;
        background: #94a3b8;
        opacity: 0.55;
    }

    .excavator {
        position: absolute;
        left: 7%;
        right: 5%;
        bottom: 48px;
        height: 285px;
    }

    .exc-track {
        position: absolute;
        bottom: 0;
        width: 37%;
        height: 58px;
        border-radius: 30px;
        background: #334155;
        border: 4px solid #475569;
        box-sizing: border-box;
    }

    .exc-track.left { left: 5%; }
    .exc-track.right { left: 22%; }

    .exc-track::after {
        content: "●  ●  ●  ●  ●";
        position: absolute;
        left: 10%;
        top: 12px;
        color: #94a3b8;
        letter-spacing: 8px;
        font-size: 14px;
    }

    .exc-base {
        position: absolute;
        left: 10%;
        bottom: 48px;
        width: 43%;
        height: 72px;
        background: linear-gradient(135deg, #d9f2e5, #a9d9bf);
        border: 4px solid #27795a;
        border-radius: 24px 32px 12px 12px;
        transform: skewX(-6deg);
        box-sizing: border-box;
    }

    .exc-engine {
        position: absolute;
        left: 34%;
        bottom: 91px;
        width: 16%;
        height: 105px;
        border-radius: 18px 24px 8px 8px;
        background: linear-gradient(135deg, #b7e5ce, #86cbaa);
        border: 4px solid #27795a;
        box-sizing: border-box;
        z-index: 5;
    }

    .exc-engine::before {
        content: "ENGINE";
        position: absolute;
        left: 10%;
        right: 10%;
        bottom: -25px;
        text-align: center;
        font-size: 10px;
        font-weight: 800;
        color: #14532d;
    }

    .exc-engine-core {
        position: absolute;
        left: 50%;
        top: 35%;
        transform: translate(-50%, -50%);
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: white;
        border: 3px solid #27795a;
    }

    .exc-engine-core::after {
        content: "↻";
        position: absolute;
        inset: 3px;
        text-align: center;
        line-height: 27px;
        color: #27795a;
        font-weight: 900;
        font-size: 18px;
    }

    .exc-cabin {
        position: absolute;
        left: 8%;
        bottom: 139px;
        width: 25%;
        height: 100px;
        background: #d5eee3;
        border: 4px solid #27795a;
        border-radius: 22px 18px 6px 6px;
        z-index: 7;
        box-sizing: border-box;
    }

    .exc-window {
        position: absolute;
        left: 12%;
        right: 10%;
        top: 13%;
        height: 48%;
        background: linear-gradient(135deg, #dff3ff, #a9d9ed);
        border: 3px solid #3b7081;
        border-radius: 9px;
    }

    .exc-window::after {
        content: "●";
        position: absolute;
        left: 48%;
        top: 25%;
        color: #475569;
        font-size: 18px;
    }

    .exc-cabin::after {
        content: "OPERATOR";
        position: absolute;
        left: 0;
        right: 0;
        bottom: -20px;
        text-align: center;
        color: #14532d;
        font-size: 10px;
        font-weight: 800;
    }

    .exc-pivot {
        position: absolute;
        left: 31%;
        bottom: 155px;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #bfdbfe;
        border: 4px solid #1d4ed8;
        z-index: 10;
        box-sizing: border-box;
    }

    .exc-pivot::after {
        content: "";
        position: absolute;
        left: 8px;
        top: 8px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #1e40af;
    }

    .exc-boom {
        position: absolute;
        left: 30%;
        bottom: 184px;
        width: 31%;
        height: 30px;
        border-radius: 18px;
        background: linear-gradient(90deg, #bfe8d1, #8ed0b2);
        border: 4px solid #27795a;
        transform: rotate(-28deg);
        transform-origin: left center;
        z-index: 8;
        box-sizing: border-box;
    }

    .exc-boom::after {
        content: "HYDRAULICS";
        position: absolute;
        left: 36%;
        top: -24px;
        font-size: 10px;
        font-weight: 800;
        color: #334155;
        white-space: nowrap;
        transform: rotate(28deg);
    }

    .exc-arm {
        position: absolute;
        left: 57%;
        bottom: 238px;
        width: 28%;
        height: 25px;
        border-radius: 15px;
        background: linear-gradient(90deg, #bfe8d1, #8ed0b2);
        border: 4px solid #27795a;
        transform: rotate(57deg);
        transform-origin: left center;
        z-index: 6;
        box-sizing: border-box;
    }

    .exc-bucket {
        position: absolute;
        left: 76%;
        bottom: 70px;
        width: 19%;
        height: 68px;
        background: #a8d8bf;
        border: 4px solid #27795a;
        border-radius: 8px 10px 28px 5px;
        transform: rotate(12deg) skewX(-8deg);
        z-index: 4;
        box-sizing: border-box;
    }

    .exc-bucket::after {
        content: "⌄  ⌄  ⌄";
        position: absolute;
        left: 15%;
        bottom: -20px;
        color: #27795a;
        font-weight: 900;
        letter-spacing: 5px;
    }

    .exc-cylinder {
        position: absolute;
        left: 39%;
        bottom: 197px;
        width: 21%;
        height: 9px;
        border-radius: 9px;
        background: #64748b;
        transform: rotate(-34deg);
        z-index: 9;
    }

    .exc-cylinder::after {
        content: "";
        position: absolute;
        right: -22px;
        top: 1px;
        width: 45%;
        height: 7px;
        border-radius: 7px;
        background: #e2e8f0;
    }

    .twin-alert-dot {
        position: absolute;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        z-index: 20;
    }

    .twin-alert-dot.engine { left: 47%; bottom: 175px; }
    .twin-alert-dot.hydraulic { left: 55%; bottom: 245px; }
    .twin-alert-dot.fuel { left: 42%; bottom: 110px; }
    .twin-alert-dot.safety { left: 19%; bottom: 225px; }

    .twin-alert-dot.warning {
        background: #f59e0b;
        box-shadow: 0 0 0 5px rgba(245,158,11,0.18), 0 0 12px rgba(245,158,11,0.6);
        animation: componentWarning 1.8s infinite;
    }

    .twin-alert-dot.critical {
        background: #dc2626;
        box-shadow: 0 0 0 6px rgba(220,38,38,0.18), 0 0 16px rgba(220,38,38,0.72);
        animation: componentCritical 1.1s infinite;
    }

    .twin-alert-dot.normal {
        background: #10b981;
        box-shadow: 0 0 0 4px rgba(16,185,129,0.12);
    }


    .twin-callout {
        position: absolute;
        z-index: 30;
        max-width: 180px;
        padding: 0.48rem 0.65rem;
        border-radius: 10px;
        background: rgba(255,255,255,0.96);
        border: 1px solid #dbe4ea;
        box-shadow: 0 5px 18px rgba(15,23,42,0.10);
        font-family: Arial, sans-serif;
        font-size: 11px;
        line-height: 1.3;
    }

    .twin-callout strong {
        display: block;
        font-size: 11px;
        margin-bottom: 2px;
    }

    .twin-callout.warning {
        border-color: #fcd34d;
        box-shadow: 0 5px 18px rgba(245,158,11,0.14);
    }

    .twin-callout.critical {
        border-color: #fca5a5;
        box-shadow: 0 5px 18px rgba(220,38,38,0.18);
    }

    .twin-callout.engine { left: 47%; bottom: 210px; }
    .twin-callout.hydraulic { left: 54%; bottom: 285px; }
    .twin-callout.fuel { left: 39%; bottom: 112px; }
    .twin-callout.safety { left: 12%; bottom: 246px; }
    .twin-callout.operation { left: 64%; bottom: 30px; }

    .twin-interpretation {
        margin-top: 0.75rem;
        padding: 0.8rem 0.9rem;
        border-radius: 14px;
        background: linear-gradient(135deg, #f8fafc, #ffffff);
        border: 1px solid #dbe4ea;
    }

    .twin-interpretation-title {
        font-size: 0.84rem;
        font-weight: 800;
        color: #16352a;
        margin-bottom: 0.25rem;
    }

    .twin-interpretation-main {
        font-size: 0.92rem;
        font-weight: 800;
        color: #334155;
        margin-bottom: 0.22rem;
    }

    .twin-interpretation-detail {
        font-size: 0.78rem;
        color: #64748b;
        line-height: 1.45;
    }

    .twin-action {
        margin-top: 0.55rem;
        padding: 0.5rem 0.65rem;
        border-radius: 9px;
        background: #eff6ff;
        color: #1e40af;
        font-size: 0.76rem;
        line-height: 1.4;
    }


    .twin-component {
        transition: opacity 0.2s ease, filter 0.2s ease;
    }

    .twin-component.normal {
        filter: drop-shadow(0 0 2px rgba(22, 101, 52, 0.12));
    }

    .twin-component.warning {
        filter: drop-shadow(0 0 7px rgba(245, 158, 11, 0.55));
        animation: componentWarning 1.8s infinite;
    }

    .twin-component.critical {
        filter: drop-shadow(0 0 10px rgba(220, 38, 38, 0.72));
        animation: componentCritical 1.1s infinite;
    }

    .twin-machine-label {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .twin-side {
        display: flex;
        flex-direction: column;
        gap: 0.65rem;
    }

    .twin-state-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 0.72rem 0.8rem;
    }

    .twin-state-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5rem;
    }

    .twin-state-name {
        font-size: 0.82rem;
        color: #475569;
        font-weight: 650;
    }

    .twin-state-value {
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.5rem;
        border-radius: 999px;
    }

    .twin-state-value.normal {
        color: #166534;
        background: #dcfce7;
    }

    .twin-state-value.warning {
        color: #92400e;
        background: #fef3c7;
    }

    .twin-state-value.critical {
        color: #991b1b;
        background: #fee2e2;
    }

    .twin-gauge {
        margin-top: 0.5rem;
        height: 8px;
        border-radius: 999px;
        background: #e2e8f0;
        overflow: hidden;
    }

    .twin-gauge-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #34d399, #10b981);
    }

    .twin-explanation {
        margin-top: 0.75rem;
        padding: 0.65rem 0.8rem;
        border-radius: 12px;
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        color: #475569;
        font-size: 0.78rem;
        line-height: 1.45;
    }

    @keyframes componentWarning {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.62; }
    }

    @keyframes componentCritical {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.45; }
    }

    @keyframes twinPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.55; }
    }

    @media (max-width: 900px) {
        .twin-body {
            grid-template-columns: 1fr;
        }
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
# VISUAL DIGITAL TWIN HELPERS
# ============================================================

def twin_status_class(status):
    """Convert a Digital Twin status into a CSS state class."""
    status = str(status).upper()

    if "CRITICAL" in status:
        return "critical"
    if any(word in status for word in ["WARNING", "HEAVY", "OVERHEATING", "LOW_", "HIGH_", "EXCESSIVE", "VIOLATION"]):
        return "warning"
    return "normal"


def twin_status_label(status):
    """Create a short human-readable label for the visual twin."""
    status = str(status).upper()

    if "CRITICAL" in status:
        return "CRITICAL"
    if any(word in status for word in ["WARNING", "HEAVY", "OVERHEATING", "LOW_", "HIGH_", "EXCESSIVE", "VIOLATION"]):
        return "WARNING"
    if "NORMAL" in status or "SAFE" in status:
        return "NORMAL"
    return status.replace("_", " ")


def clamp_percentage(value):
    return max(0, min(100, float(value)))


def render_visual_digital_twin(
    state,
    health,
    temperature,
    hydraulic,
    fuel,
    load,
    recommendations
):
    """Render the excavator as a live visual representation of MachineState."""

    engine_status = twin_status_class(state.engine.status)
    hydraulic_status = twin_status_class(state.hydraulics.status)
    fuel_status = twin_status_class(state.fuel.status)
    operation_status = twin_status_class(state.operation.status)
    safety_status = twin_status_class(state.safety.status)
    overall_status = twin_status_class(state.overall_status)

    engine_label = twin_status_label(state.engine.status)
    hydraulic_label = twin_status_label(state.hydraulics.status)
    fuel_label = twin_status_label(state.fuel.status)
    operation_label = twin_status_label(state.operation.status)
    safety_label = twin_status_label(state.safety.status)
    overall_label = twin_status_label(state.overall_status)

    health_width = clamp_percentage(health)
    fuel_width = clamp_percentage(fuel)
    load_width = clamp_percentage(load)

    # The machine is rendered with HTML/CSS so Streamlit can reliably
    # display it. Each subsystem still receives its state class from the
    # actual Digital Twin MachineState.

    svg = f"""
    <div class="excavator-stage">
        <div class="excavator-ground"></div>

        <div class="excavator">

            <div class="exc-track left twin-component {operation_status}"></div>
            <div class="exc-track right twin-component {operation_status}"></div>

            <div class="exc-base twin-component {operation_status}"></div>

            <div class="exc-engine twin-component {engine_status}">
                <div class="exc-engine-core"></div>
            </div>

            <div class="exc-cabin twin-component {safety_status}">
                <div class="exc-window"></div>
            </div>

            <div class="exc-pivot twin-component {hydraulic_status}"></div>

            <div class="exc-boom twin-component {hydraulic_status}"></div>
            <div class="exc-arm twin-component {hydraulic_status}"></div>
            <div class="exc-cylinder twin-component {hydraulic_status}"></div>
            <div class="exc-bucket twin-component {operation_status}"></div>

            <div class="twin-alert-dot engine {engine_status}"
                 title="Engine: {engine_label}"></div>
            <div class="twin-alert-dot hydraulic {hydraulic_status}"
                 title="Hydraulics: {hydraulic_label}"></div>
            <div class="twin-alert-dot fuel {fuel_status}"
                 title="Fuel: {fuel_label}"></div>
            <div class="twin-alert-dot safety {safety_status}"
                 title="Safety: {safety_label}"></div>

            {
                f'<div class="twin-callout engine {engine_status}"><strong>Engine</strong>{engine_label}<br>{temperature:.1f} °C</div>'
                if engine_status != "normal" else ""
            }

            {
                f'<div class="twin-callout hydraulic {hydraulic_status}"><strong>Hydraulics</strong>{hydraulic_label}<br>{hydraulic:.1f} bar</div>'
                if hydraulic_status != "normal" else ""
            }

            {
                f'<div class="twin-callout fuel {fuel_status}"><strong>Fuel</strong>{fuel_label}<br>{fuel:.1f}% remaining</div>'
                if fuel_status != "normal" else ""
            }

            {
                f'<div class="twin-callout safety {safety_status}"><strong>Safety</strong>{safety_label}</div>'
                if safety_status != "normal" else ""
            }

            {
                f'<div class="twin-callout operation {operation_status}"><strong>Operation</strong>{operation_label}<br>Load {load:.1f}%</div>'
                if operation_status != "normal" else ""
            }
        </div>
    </div>
    """

    status_class = overall_status
    explanation = (
        "The virtual machine is mirroring the current Digital Twin state. "
        "Highlighted subsystems correspond to the engine, hydraulic, "
        "fuel/operation and safety states calculated from telemetry."
    )

    if overall_status == "critical":
        badge = "CRITICAL"
    elif overall_status == "warning":
        badge = "WARNING"
    else:
        badge = "NORMAL"

    # Use the already-computed Recommendation Engine output.
    # This keeps the visual twin aligned with the existing decision pipeline.
    primary_recommendation = None
    if recommendations:
        priority_order = {"CRITICAL": 3, "WARNING": 2, "NORMAL": 1, "UNKNOWN": 0}
        primary_recommendation = max(
            recommendations,
            key=lambda item: priority_order.get(item.get("priority", "UNKNOWN"), 0)
        )

    if primary_recommendation:
        interpretation_title = primary_recommendation.get(
            "title", "Machine condition detected"
        )
        interpretation_message = primary_recommendation.get(
            "message", "The Digital Twin detected a machine condition."
        )
        interpretation_action = primary_recommendation.get(
            "action", "Inspect the machine condition."
        )
    else:
        interpretation_title = "Machine operating normally"
        interpretation_message = "No active operator issue was detected."
        interpretation_action = "Continue operation while monitoring telemetry."

    state_cards = [
        ("Engine", engine_label, engine_status),
        ("Hydraulics", hydraulic_label, hydraulic_status),
        ("Fuel", fuel_label, fuel_status),
        ("Operation", operation_label, operation_status),
        ("Safety", safety_label, safety_status),
    ]

    cards_html = ""
    for name, label, css_class in state_cards:
        cards_html += f"""
        <div class="twin-state-card">
            <div class="twin-state-row">
                <span class="twin-state-name">{name}</span>
                <span class="twin-state-value {css_class}">{label}</span>
            </div>
        </div>
        """

    html = f"""
    <div class="twin-panel">
        <div class="twin-header">
            <div>
                <div class="twin-title">🚜 Live Visual Digital Twin</div>
                <div class="twin-subtitle">
                    A virtual representation of the excavator's current machine state
                </div>
            </div>
            <div class="twin-live-badge {status_class}">
                ● TWIN STATUS: {badge}
            </div>
        </div>

        <div class="twin-body">
            <div class="twin-machine">
                {svg}
            </div>

            <div class="twin-side">
                {cards_html}

                <div class="twin-state-card">
                    <div class="twin-state-name">Machine Load</div>
                    <div class="twin-gauge">
                        <div class="twin-gauge-fill"
                             style="width:{load_width:.1f}%"></div>
                    </div>
                    <div class="twin-state-row" style="margin-top:0.35rem">
                        <span class="twin-state-name">Current load</span>
                        <strong>{load:.1f}%</strong>
                    </div>
                </div>

                <div class="twin-state-card">
                    <div class="twin-state-name">Fuel Level</div>
                    <div class="twin-gauge">
                        <div class="twin-gauge-fill"
                             style="width:{fuel_width:.1f}%"></div>
                    </div>
                    <div class="twin-state-row" style="margin-top:0.35rem">
                        <span class="twin-state-name">Available fuel</span>
                        <strong>{fuel:.1f}%</strong>
                    </div>
                </div>

                <div class="twin-interpretation">
                    <div class="twin-interpretation-title">
                        🧠 Twin Interpretation
                    </div>
                    <div class="twin-interpretation-main">
                        {interpretation_title}
                    </div>
                    <div class="twin-interpretation-detail">
                        {interpretation_message}
                    </div>
                    <div class="twin-action">
                        <strong>Operator action:</strong>
                        {interpretation_action}
                    </div>
                </div>

                <div class="twin-explanation">
                    <strong>How to read this:</strong><br>
                    {explanation}
                </div>
            </div>
        </div>
    </div>
    """

    st.html(html)


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
# VISUAL DIGITAL TWIN
# ============================================================

render_visual_digital_twin(
    current_state,
    machine_health,
    engine_temperature,
    hydraulic_pressure,
    fuel_level,
    load,
    recommendations
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