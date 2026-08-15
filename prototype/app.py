from pathlib import Path
from datetime import date

import joblib
import pandas as pd
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartCare AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

    /* ======================================================
       GLOBAL
    ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(33, 105, 150, 0.12),
                transparent 30%
            ),
            #081018;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }


    /* ======================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {
        background: #0d1721;
        border-right: 1px solid #20303e;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #22313e;
    }

    .sidebar-brand {
        padding: 12px 4px 20px 4px;
    }

    .sidebar-brand-title {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 3px;
    }

    .sidebar-brand-subtitle {
        color: #8296a8;
        font-size: 13px;
        line-height: 1.5;
    }


    /* ======================================================
       HERO
    ====================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                120deg,
                #123a56 0%,
                #10283c 48%,
                #0c1c2b 100%
            );

        border: 1px solid #24506a;
        border-radius: 24px;

        padding: 38px 42px;
        margin-bottom: 30px;

        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.22);
    }

    .hero::after {
        content: "";
        position: absolute;

        width: 330px;
        height: 330px;

        right: -120px;
        top: -170px;

        border-radius: 50%;

        background:
            rgba(81, 169, 218, 0.12);
    }

    .hero-badge {
        display: inline-block;

        background: rgba(85, 178, 229, 0.12);
        border: 1px solid rgba(109, 192, 237, 0.23);

        color: #8bd5fa;

        padding: 7px 13px;
        border-radius: 999px;

        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.6px;

        margin-bottom: 15px;
    }

    .hero-title {
        color: #ffffff;

        font-size: 43px;
        font-weight: 850;

        line-height: 1.08;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        max-width: 850px;

        color: #b8cad8;

        font-size: 16px;
        line-height: 1.7;
    }


    /* ======================================================
       SECTION TITLE
    ====================================================== */

    .section-header {
        margin-top: 8px;
        margin-bottom: 15px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 780;
        color: #ffffff;
    }

    .section-subtitle {
        color: #7f94a7;
        font-size: 13px;
        margin-top: 3px;
    }


    /* ======================================================
       OVERVIEW CARDS
    ====================================================== */

    .overview-card {
        height: 145px;

        background:
            linear-gradient(
                145deg,
                #101c27,
                #0e1822
            );

        border: 1px solid #223646;

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.15);
    }

    .overview-icon {
        font-size: 23px;
        margin-bottom: 12px;
    }

    .overview-label {
        color: #8195a6;
        font-size: 12px;
        font-weight: 600;

        margin-bottom: 5px;
    }

    .overview-value {
        color: #f7fbff;

        font-size: 23px;
        font-weight: 780;

        line-height: 1.25;
    }


    /* ======================================================
       EMPTY STATE
    ====================================================== */

    .empty-card {
        margin-top: 27px;

        background: #0e1923;

        border:
            1px dashed #294153;

        border-radius: 20px;

        padding: 38px 25px;

        text-align: center;
    }

    .empty-icon {
        font-size: 38px;
        margin-bottom: 10px;
    }

    .empty-title {
        color: white;

        font-size: 19px;
        font-weight: 750;

        margin-bottom: 6px;
    }

    .empty-text {
        color: #8498aa;

        font-size: 14px;
    }


    /* ======================================================
       RESULT CARD
    ====================================================== */

    .result-card {
        border-radius: 22px;

        padding: 28px 30px;

        margin-bottom: 20px;

        border: 1px solid;

        box-shadow:
            0 12px 32px
            rgba(0, 0, 0, 0.20);
    }

    .result-low {
        background:
            linear-gradient(
                120deg,
                rgba(15, 89, 65, 0.42),
                rgba(9, 42, 34, 0.75)
            );

        border-color:
            rgba(65, 211, 153, 0.35);
    }

    .result-medium {
        background:
            linear-gradient(
                120deg,
                rgba(112, 77, 17, 0.42),
                rgba(47, 34, 9, 0.78)
            );

        border-color:
            rgba(245, 190, 76, 0.37);
    }

    .result-high {
        background:
            linear-gradient(
                120deg,
                rgba(112, 35, 45, 0.45),
                rgba(49, 15, 21, 0.80)
            );

        border-color:
            rgba(247, 92, 110, 0.38);
    }

    .risk-badge {
        display: inline-block;

        padding: 7px 13px;
        border-radius: 999px;

        font-size: 12px;
        font-weight: 800;

        letter-spacing: 0.6px;

        margin-bottom: 13px;
    }

    .badge-low {
        background:
            rgba(51, 211, 153, 0.16);

        color: #62e5ae;
    }

    .badge-medium {
        background:
            rgba(251, 191, 36, 0.16);

        color: #ffd467;
    }

    .badge-high {
        background:
            rgba(248, 113, 113, 0.17);

        color: #ff909c;
    }

    .result-heading {
        color: #ffffff;

        font-size: 27px;
        font-weight: 820;

        margin-bottom: 8px;
    }

    .result-description {
        color: #c4d0da;

        font-size: 14px;
        line-height: 1.7;

        max-width: 900px;
    }


    /* ======================================================
       PROBABILITY CARDS
    ====================================================== */

    .metric-card {
        height: 132px;

        background: #0f1a24;

        border: 1px solid #213545;

        border-radius: 18px;

        padding: 22px;

        text-align: center;
    }

    .metric-label {
        color: #8498aa;

        font-size: 12px;
        font-weight: 600;

        margin-bottom: 8px;
    }

    .metric-value {
        color: #ffffff;

        font-size: 33px;
        font-weight: 820;
    }

    .metric-small {
        font-size: 24px;
    }


    /* ======================================================
       RISK BAR
    ====================================================== */

    .risk-bar-background {
        width: 100%;
        height: 13px;

        background: #1d2a35;

        border-radius: 30px;

        overflow: hidden;

        margin-top: 8px;
    }

    .risk-bar-fill {
        height: 13px;

        border-radius: 30px;

        transition: width 0.3s ease;
    }

    .risk-bar-labels {
        display: flex;
        justify-content: space-between;

        color: #728798;

        font-size: 11px;

        margin-top: 7px;
    }


    /* ======================================================
       FACTOR CARDS
    ====================================================== */

    .factor-card {
        min-height: 180px;

        background: #0f1a24;

        border: 1px solid #213545;

        border-radius: 18px;

        padding: 22px;
    }

    .factor-icon {
        font-size: 25px;
        margin-bottom: 11px;
    }

    .factor-title {
        color: #ffffff;

        font-size: 17px;
        font-weight: 750;

        margin-bottom: 8px;
    }

    .factor-description {
        color: #879bad;

        font-size: 13px;
        line-height: 1.65;
    }


    /* ======================================================
       INFO BOX
    ====================================================== */

    .model-note {
        background:
            rgba(37, 99, 235, 0.08);

        border:
            1px solid rgba(66, 133, 230, 0.20);

        border-radius: 15px;

        padding: 18px 20px;

        color: #aec9e3;

        font-size: 13px;
        line-height: 1.65;
    }


    /* ======================================================
       FOOTER
    ====================================================== */

    .footer {
        margin-top: 45px;

        border-top: 1px solid #1d2c38;

        padding-top: 22px;
        padding-bottom: 15px;

        text-align: center;

        color: #637789;

        font-size: 12px;
    }


    /* ======================================================
       STREAMLIT BUTTON
    ====================================================== */

    div.stButton > button {
        width: 100%;

        min-height: 48px;

        border: none;
        border-radius: 12px;

        background:
            linear-gradient(
                90deg,
                #1675b8,
                #2093c7
            );

        color: white;

        font-size: 15px;
        font-weight: 750;

        box-shadow:
            0 7px 20px
            rgba(30, 126, 185, 0.22);
    }

    div.stButton > button:hover {
        border: none;

        background:
            linear-gradient(
                90deg,
                #1a82c8,
                #24a0d3
            );
    }


    /* ======================================================
       DATAFRAME
    ====================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }


    /* ======================================================
       RESPONSIVENESS
    ====================================================== */

    @media (max-width: 900px) {

        .hero-title {
            font-size: 34px;
        }

        .hero {
            padding: 28px;
        }

    }

    </style>
    """
)


# ============================================================
# 3. MODEL LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "smartcare_no_show_model.joblib"
)


# ============================================================
# 4. LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


if not MODEL_PATH.exists():

    st.error(
        "The trained model could not be found."
    )

    st.code(
        str(MODEL_PATH)
    )

    st.stop()


try:

    model = load_model()

except Exception as error:

    st.error(
        "The trained model could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-title">
                🏥 SmartCare
            </div>

            <div class="sidebar-brand-subtitle">
                AI-powered appointment
                attendance risk assessment
            </div>

        </div>
        """
    )

    st.divider()

    st.subheader(
        "👤 Patient Details"
    )


    age = st.number_input(
        "Age",
        min_value=1,
        max_value=90,
        value=45,
        step=1
    )


    gender = st.selectbox(
        "Gender",
        [
            "Female",
            "Male"
        ]
    )


    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+",
            "A-",
            "AB+",
            "AB-",
            "B+",
            "B-",
            "O+",
            "O-"
        ]
    )


    department = st.selectbox(
        "Department",
        [
            "Cardiology",
            "General Medicine",
            "Laboratory Services",
            "Neurology",
            "Orthopedics",
            "Pediatrics",
            "Radiology"
        ]
    )


    diagnosis = st.selectbox(
        "Diagnosis",
        [
            "Asthma",
            "Back Pain",
            "Chest Pain",
            "Diabetes",
            "Fever",
            "Fracture",
            "Hypertension",
            "Kidney Infection",
            "Migraine",
            "Pneumonia"
        ]
    )


    st.divider()

    st.subheader(
        "📅 Appointment Details"
    )


    appointment_date = st.date_input(
        "Appointment Date",
        value=date.today()
    )


    waiting_days = st.number_input(
        "Waiting Days",
        min_value=0,
        max_value=44,
        value=14,
        step=1,
        help=(
            "Number of days between booking "
            "and the appointment."
        )
    )


    st.divider()

    st.subheader(
        "📋 Patient History"
    )


    previous_appointments = st.number_input(
        "Previous Appointments",
        min_value=0,
        max_value=10,
        value=3,
        step=1
    )


    # Prevent logically invalid value
    maximum_missed = int(
        previous_appointments
    )


    default_missed = min(
        1,
        maximum_missed
    )


    missed_previous_appointments = (
        st.number_input(
            "Previously Missed Appointments",
            min_value=0,
            max_value=maximum_missed,
            value=default_missed,
            step=1
        )
    )


    previous_admissions = st.number_input(
        "Previous Admissions",
        min_value=0,
        max_value=5,
        value=1,
        step=1
    )


    st.divider()


    predict_button = st.button(
        "🔍 Run AI Prediction",
        type="primary"
    )


# ============================================================
# 6. FEATURE ENGINEERING
# ============================================================

appointment_month = str(
    appointment_date.month
)


appointment_day_of_week = (
    appointment_date.strftime("%A")
)


appointment_is_weekend = int(
    appointment_date.weekday() >= 5
)


if previous_appointments > 0:

    previous_no_show_rate = (
        missed_previous_appointments
        / previous_appointments
    )

else:

    previous_no_show_rate = 0.0


has_previous_no_show = int(
    missed_previous_appointments > 0
)


# ============================================================
# 7. CREATE INPUT DATAFRAME
# ============================================================

input_data = pd.DataFrame(
    [
        {
            "age":
                int(age),

            "gender":
                gender,

            "blood_group":
                blood_group,

            "department":
                department,

            "diagnosis":
                diagnosis,

            "waiting_days":
                int(waiting_days),

            "previous_appointments":
                int(previous_appointments),

            "missed_previous_appointments":
                int(
                    missed_previous_appointments
                ),

            "previous_admissions":
                int(previous_admissions),

            "appointment_month":
                appointment_month,

            "appointment_day_of_week":
                appointment_day_of_week,

            "appointment_is_weekend":
                appointment_is_weekend,

            "previous_no_show_rate":
                previous_no_show_rate,

            "has_previous_no_show":
                has_previous_no_show
        }
    ]
)


# ============================================================
# 8. HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-badge">
            AI-POWERED HEALTHCARE DECISION SUPPORT
        </div>

        <div class="hero-title">
            SmartCare AI
        </div>

        <div class="hero-subtitle">

            Appointment No-Show Prediction System.
            Estimate appointment attendance risk using
            patient information, appointment history,
            and a trained machine-learning model.

        </div>

    </div>
    """
)


# ============================================================
# 9. PATIENT OVERVIEW
# ============================================================

st.html(
    """
    <div class="section-header">

        <div class="section-title">
            Patient Overview
        </div>

        <div class="section-subtitle">
            Current information entered for this assessment
        </div>

    </div>
    """
)


overview1, overview2, overview3, overview4 = (
    st.columns(4)
)


with overview1:

    st.html(
        f"""
        <div class="overview-card">

            <div class="overview-icon">
                👤
            </div>

            <div class="overview-label">
                PATIENT AGE
            </div>

            <div class="overview-value">
                {age} Years
            </div>

        </div>
        """
    )


with overview2:

    st.html(
        f"""
        <div class="overview-card">

            <div class="overview-icon">
                🏥
            </div>

            <div class="overview-label">
                DEPARTMENT
            </div>

            <div class="overview-value">
                {department}
            </div>

        </div>
        """
    )


with overview3:

    st.html(
        f"""
        <div class="overview-card">

            <div class="overview-icon">
                📅
            </div>

            <div class="overview-label">
                WAITING TIME
            </div>

            <div class="overview-value">
                {waiting_days} Days
            </div>

        </div>
        """
    )


with overview4:

    st.html(
        f"""
        <div class="overview-card">

            <div class="overview-icon">
                📊
            </div>

            <div class="overview-label">
                PREVIOUS NO-SHOW RATE
            </div>

            <div class="overview-value">
                {previous_no_show_rate * 100:.1f}%
            </div>

        </div>
        """
    )


# ============================================================
# 10. EMPTY STATE
# ============================================================

if not predict_button:

    st.html(
        """
        <div class="empty-card">

            <div class="empty-icon">
                🤖
            </div>

            <div class="empty-title">
                Ready for AI Assessment
            </div>

            <div class="empty-text">
                Enter patient information in the sidebar
                and select <b>Run AI Prediction</b>.
            </div>

        </div>
        """
    )


# ============================================================
# 11. PREDICTION
# ============================================================

if predict_button:

    try:

        prediction = int(
            model.predict(
                input_data
            )[0]
        )


        probabilities = model.predict_proba(
            input_data
        )[0]


        attendance_probability = float(
            probabilities[0]
        )


        no_show_probability = float(
            probabilities[1]
        )


        attendance_percentage = (
            attendance_probability
            * 100
        )


        no_show_percentage = (
            no_show_probability
            * 100
        )


        # ====================================================
        # RISK BAND
        #
        # These Low / Moderate / High bands are a
        # presentation layer.
        #
        # Actual ML classification still comes from
        # model.predict().
        # ====================================================

        if no_show_percentage < 40:

            risk_level = "LOW RISK"

            result_class = "result-low"

            badge_class = "badge-low"

            risk_icon = "✅"

            risk_colour = "#3dd19a"

            result_heading = (
                "Lower appointment no-show risk"
            )

            result_description = (
                "The predicted probability of "
                "non-attendance is relatively low. "
                "The model currently indicates a lower "
                "risk of this appointment being missed."
            )


        elif no_show_percentage < 60:

            risk_level = "MODERATE RISK"

            result_class = "result-medium"

            badge_class = "badge-medium"

            risk_icon = "⚠️"

            risk_colour = "#f2ba4c"

            result_heading = (
                "Borderline appointment risk"
            )

            result_description = (
                "The predicted probability is close to "
                "the classification boundary. "
                "This result should therefore be interpreted "
                "cautiously rather than as a confident outcome."
            )


        else:

            risk_level = "HIGH RISK"

            result_class = "result-high"

            badge_class = "badge-high"

            risk_icon = "🚨"

            risk_colour = "#ef6372"

            result_heading = (
                "Higher appointment no-show risk"
            )

            result_description = (
                "The model estimates an elevated probability "
                "of appointment non-attendance. "
                "A supportive reminder or appointment "
                "confirmation may be considered."
            )


        # ====================================================
        # RESULT HEADER
        # ====================================================

        st.html(
            """
            <div style="height:28px;"></div>

            <div class="section-header">

                <div class="section-title">
                    AI Risk Assessment
                </div>

                <div class="section-subtitle">
                    Prediction generated by the trained
                    Logistic Regression model
                </div>

            </div>
            """
        )


        st.html(
            f"""
            <div class="
                result-card
                {result_class}
            ">

                <div class="
                    risk-badge
                    {badge_class}
                ">
                    {risk_icon} {risk_level}
                </div>

                <div class="result-heading">
                    {result_heading}
                </div>

                <div class="result-description">
                    {result_description}
                </div>

            </div>
            """
        )


        # ====================================================
        # METRICS
        # ====================================================

        metric1, metric2, metric3 = (
            st.columns(3)
        )


        with metric1:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        NO-SHOW PROBABILITY
                    </div>

                    <div class="metric-value">
                        {no_show_percentage:.1f}%
                    </div>

                </div>
                """
            )


        with metric2:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        ATTENDANCE PROBABILITY
                    </div>

                    <div class="metric-value">
                        {attendance_percentage:.1f}%
                    </div>

                </div>
                """
            )


        model_class_name = (
            "No-Show"
            if prediction == 1
            else "Attended"
        )


        with metric3:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        MODEL CLASS
                    </div>

                    <div class="
                        metric-value
                        metric-small
                    ">
                        {model_class_name}
                    </div>

                </div>
                """
            )


        # ====================================================
        # RISK BAR
        # ====================================================

        st.html(
            f"""
            <div style="height:25px;"></div>

            <div class="section-header">

                <div class="section-title">
                    No-Show Risk Probability
                </div>

            </div>

            <div class="risk-bar-background">

                <div
                    class="risk-bar-fill"
                    style="
                        width:
                        {no_show_percentage:.1f}%;

                        background:
                        {risk_colour};
                    "
                >
                </div>

            </div>

            <div class="risk-bar-labels">

                <span>
                    0% Low
                </span>

                <span>
                    40% Moderate
                </span>

                <span>
                    60% High
                </span>

                <span>
                    100%
                </span>

            </div>
            """
        )


        # ====================================================
        # EXPLANATION
        # ====================================================

        st.html(
            """
            <div style="height:28px;"></div>

            <div class="section-header">

                <div class="section-title">
                    Model-Wide Important Factors
                </div>

                <div class="section-subtitle">
                    Important variables identified during
                    Explainable AI analysis
                </div>

            </div>
            """
        )


        factor1, factor2, factor3 = (
            st.columns(3)
        )


        with factor1:

            st.html(
                """
                <div class="factor-card">

                    <div class="factor-icon">
                        ⏳
                    </div>

                    <div class="factor-title">
                        Waiting Days
                    </div>

                    <div class="factor-description">

                        Appointment waiting time was identified
                        as the strongest overall predictor in
                        the model-wide feature-importance
                        analysis.

                    </div>

                </div>
                """
            )


        with factor2:

            st.html(
                """
                <div class="factor-card">

                    <div class="factor-icon">
                        📋
                    </div>

                    <div class="factor-title">
                        Previous No-Shows
                    </div>

                    <div class="factor-description">

                        Historical missed appointments
                        contribute useful information about
                        future appointment attendance patterns.

                    </div>

                </div>
                """
            )


        with factor3:

            st.html(
                """
                <div class="factor-card">

                    <div class="factor-icon">
                        📈
                    </div>

                    <div class="factor-title">
                        Appointment History
                    </div>

                    <div class="factor-description">

                        Previous appointment behaviour and
                        previous no-show rate contribute to
                        the model's overall risk assessment.

                    </div>

                </div>
                """
            )


        # ====================================================
        # PATIENT DATA
        # ====================================================

        st.html(
            """
            <div style="height:24px;"></div>
            """
        )


        with st.expander(
            "🔎 View information sent to the AI model"
        ):

            display_data = input_data.copy()


            display_data[
                "previous_no_show_rate"
            ] = (
                display_data[
                    "previous_no_show_rate"
                ]
                * 100
            ).round(1)


            display_data = display_data.rename(
                columns={

                    "age":
                        "Age",

                    "gender":
                        "Gender",

                    "blood_group":
                        "Blood Group",

                    "department":
                        "Department",

                    "diagnosis":
                        "Diagnosis",

                    "waiting_days":
                        "Waiting Days",

                    "previous_appointments":
                        "Previous Appointments",

                    "missed_previous_appointments":
                        "Previously Missed",

                    "previous_admissions":
                        "Previous Admissions",

                    "appointment_month":
                        "Appointment Month",

                    "appointment_day_of_week":
                        "Appointment Day",

                    "appointment_is_weekend":
                        "Weekend",

                    "previous_no_show_rate":
                        "Previous No-Show Rate (%)",

                    "has_previous_no_show":
                        "Has Previous No-Show"
                }
            )


            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True
            )


        # ====================================================
        # MODEL CLASS EXPLANATION
        # ====================================================

        st.html(
            f"""
            <div class="model-note">

                <b>Model classification:</b>
                {model_class_name}
                ({prediction})

                <br><br>

                The machine-learning class above comes directly
                from the trained model.
                The Low / Moderate / High risk level is an
                additional probability-based display used to make
                the result easier to interpret.

            </div>
            """
        )


        # ====================================================
        # ETHICAL NOTICE
        # ====================================================

        st.warning(
            """
            ⚕️ **Decision-Support Notice**

            This prototype is intended for educational
            decision-support purposes.

            A prediction should not automatically be used to
            cancel an appointment, deny healthcare services,
            or penalize a patient.

            Human judgement should remain part of any
            healthcare-related decision.
            """
        )


    except Exception as error:

        st.error(
            "An error occurred while generating "
            "the prediction."
        )

        st.exception(error)


# ============================================================
# 12. ABOUT MODEL
# ============================================================

st.html(
    """
    <div style="height:25px;"></div>
    """
)


with st.expander(
    "🤖 About the SmartCare AI Model"
):

    st.write(
        "**Selected model:** Logistic Regression"
    )

    st.write(
        "**Problem type:** Binary Classification"
    )

    st.write(
        "**Target variable:** `no_show`"
    )

    st.write(
        "**Class 0:** Attended / Other"
    )

    st.write(
        "**Class 1:** No-Show"
    )

    st.write(
        """
        Logistic Regression was selected after
        comparison with Decision Tree and Random Forest
        models using Accuracy, Precision, Recall,
        F1 Score, and ROC-AUC.
        """
    )


# ============================================================
# 13. FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        SmartCare AI
        &nbsp;&nbsp;•&nbsp;&nbsp;
        CCS3440 Artificial Intelligence Coursework
        &nbsp;&nbsp;•&nbsp;&nbsp;
        Appointment Decision Support

    </div>
    """
)