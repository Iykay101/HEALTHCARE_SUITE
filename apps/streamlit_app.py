from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from healthcare_suite.interactions import InteractionDB, parse_med_list_from_text
from healthcare_suite.sir import SIRModel, SIRParams
from healthcare_suite.sir.plots import plot_sir_matplotlib, plot_sir_plotly
from healthcare_suite.scheduler import AppointmentRequest, DoctorCalendar, Priority, schedule_requests

st.set_page_config(page_title="Healthcare Suite", layout="wide")
st.title("Healthcare Suite")

tab1, tab2, tab3 = st.tabs(["Drug interactions", "SIR simulator", "Appointment scheduler"])

with tab1:
    st.subheader("Drug interaction checker")
    db_path = st.text_input("Interaction CSV path", value="data/sample_interactions.csv")
    meds_text = st.text_area("Medications (comma or newline separated)", value="warfarin\nibuprofen\namiodarone", height=120)
    if st.button("Check interactions"):
        try:
            db = InteractionDB.from_csv(db_path)
            meds = parse_med_list_from_text(meds_text)
            hits = db.check_list(meds)
            if not hits:
                st.success("No interactions found in the current dataset.")
            else:
                st.warning(f"Found {len(hits)} interaction(s).")
                st.dataframe(pd.DataFrame([h.__dict__ for h in hits]), use_container_width=True)
        except Exception as e:
            st.error(str(e))

with tab2:
    st.subheader("SIR model simulator")
    col1, col2, col3 = st.columns(3)
    with col1:
        population = st.number_input("Population (N)", min_value=10, max_value=10_000_000, value=1000, step=10)
        initial_infected = st.number_input("Initial infected (I0)", min_value=1, max_value=int(population), value=5, step=1)
        days = st.number_input("Days", min_value=1, max_value=3650, value=160, step=1)
    with col2:
        beta = st.number_input("Infection rate (beta)", min_value=0.0, max_value=5.0, value=0.35, step=0.01, format="%.2f")
        gamma = st.number_input("Recovery rate (gamma)", min_value=0.0, max_value=5.0, value=0.10, step=0.01, format="%.2f")
        dt = st.number_input("Time step (dt)", min_value=0.01, max_value=2.0, value=0.2, step=0.01, format="%.2f")
    with col3:
        chart_type = st.selectbox("Chart", ["Matplotlib", "Plotly"])
        title = st.text_input("Plot title", value="SIR Simulation")

    if st.button("Run simulation"):
        try:
            params = SIRParams(population=int(population), beta=float(beta), gamma=float(gamma), initial_infected=int(initial_infected))
            model = SIRModel(params)
            df = model.simulate_euler(days=int(days), dt=float(dt))
            st.dataframe(df.head(10), use_container_width=True)
            if chart_type == "Matplotlib":
                st.pyplot(plot_sir_matplotlib(df, title=title), clear_figure=True)
            else:
                st.plotly_chart(plot_sir_plotly(df, title=title), use_container_width=True)
        except Exception as e:
            st.error(str(e))

with tab3:
    st.subheader("Doctor appointment scheduler (greedy)")

    today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    clinic_day = st.date_input("Clinic day", value=today.date())
    open_dt = datetime.combine(clinic_day, datetime.min.time()).replace(hour=9, minute=0)
    close_dt = datetime.combine(clinic_day, datetime.min.time()).replace(hour=17, minute=0)
    st.caption("Working hours fixed to 09:00–17:00 for demo.")
    n = st.number_input("Number of requests", min_value=1, max_value=30, value=5, step=1)

    requests = []
    for i in range(int(n)):
        with st.expander(f"Request {i+1}", expanded=(i == 0)):
            patient_id = st.text_input(f"Patient id {i+1}", value=f"P{i+1}", key=f"pid{i}")
            pr = st.selectbox(f"Priority {i+1}", list(Priority), format_func=lambda p: p.name, key=f"pr{i}")
            desired_start = st.time_input(f"Desired earliest start {i+1}", value=(open_dt + timedelta(minutes=30*i)).time(), key=f"ds{i}")
            desired_end = st.time_input(f"Desired latest end {i+1}", value=(open_dt + timedelta(minutes=30*i+60)).time(), key=f"de{i}")
            duration = st.selectbox(f"Duration (min) {i+1}", [10, 15, 20, 30, 45, 60], index=1, key=f"dur{i}")
            note = st.text_input(f"Note {i+1}", value="", key=f"note{i}")
            rs = datetime.combine(clinic_day, desired_start)
            re = datetime.combine(clinic_day, desired_end)
            requests.append(AppointmentRequest(patient_id, rs, re, int(duration), pr, note))

    if st.button("Schedule"):
        try:
            cal = DoctorCalendar(open_time=open_dt, close_time=close_dt, slot_minutes=5)
            result = schedule_requests(cal, requests)
            st.success(f"Confirmed: {len(result.confirmed)} | Rejected: {len(result.rejected)} | Preempted: {len(result.preempted)}")
            if result.preempted:
                st.warning("Preempted (removed due to emergency):")
                st.dataframe(pd.DataFrame([a.__dict__ for a in result.preempted]), use_container_width=True)

            st.subheader("Confirmed schedule")
            dfc = pd.DataFrame([a.__dict__ for a in cal.appointments])
            st.dataframe(dfc, use_container_width=True)

            if result.rejected:
                st.subheader("Rejected requests")
                dfr = pd.DataFrame([{
                    "patient_id": r.patient_id,
                    "priority": r.priority.name,
                    "requested_start": r.requested_start,
                    "requested_end": r.requested_end,
                    "duration_minutes": r.duration_minutes,
                } for r in result.rejected])
                st.dataframe(dfr, use_container_width=True)
        except Exception as e:
            st.error(str(e))
