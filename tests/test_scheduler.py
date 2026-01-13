from datetime import datetime
from healthcare_suite.scheduler import AppointmentRequest, DoctorCalendar, Priority, schedule_requests

def dt(h, m):
    return datetime(2026, 1, 13, h, m)

def test_greedy_schedules_routine():
    cal = DoctorCalendar(open_time=dt(9,0), close_time=dt(10,0), slot_minutes=5)
    reqs = [
        AppointmentRequest("p1", dt(9,0), dt(10,0), duration_minutes=15, priority=Priority.ROUTINE),
        AppointmentRequest("p2", dt(9,0), dt(10,0), duration_minutes=15, priority=Priority.ROUTINE),
    ]
    res = schedule_requests(cal, reqs)
    assert len(res.confirmed) == 2
    assert len(res.rejected) == 0

def test_emergency_can_preempt():
    cal = DoctorCalendar(open_time=dt(9,0), close_time=dt(10,0), slot_minutes=5)
    routine = AppointmentRequest("p1", dt(9,0), dt(10,0), duration_minutes=30, priority=Priority.ROUTINE)
    emergency = AppointmentRequest("pE", dt(9,0), dt(9,30), duration_minutes=30, priority=Priority.EMERGENCY)
    res = schedule_requests(cal, [routine, emergency])
    assert any(a.patient_id == "pE" for a in res.confirmed)
    assert len(res.preempted) == 1
