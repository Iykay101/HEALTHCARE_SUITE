from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable, List

from .calendar import DoctorCalendar
from .models import AppointmentRequest, ConfirmedAppointment, Priority


@dataclass
class SchedulingResult:
    confirmed: List[ConfirmedAppointment]
    rejected: List[AppointmentRequest]
    preempted: List[ConfirmedAppointment]


def schedule_requests(calendar: DoctorCalendar, requests: Iterable[AppointmentRequest]) -> SchedulingResult:
    reqs = list(requests)
    for r in reqs:
        r.validate()

    confirmed: List[ConfirmedAppointment] = []
    rejected: List[AppointmentRequest] = []
    preempted: List[ConfirmedAppointment] = []

    for req in reqs:
        duration = timedelta(minutes=req.duration_minutes)
        fit = calendar.find_first_fit(req.requested_start, req.requested_end, duration)
        if fit:
            start, end = fit
            appt = ConfirmedAppointment(req.patient_id, start, end, req.priority, req.note)
            calendar.add_appointment(appt)
            confirmed.append(appt)
            continue

        if req.priority == Priority.EMERGENCY:
            start = max(req.requested_start, calendar.open_time).replace(second=0, microsecond=0)
            end = start + duration
            if calendar.is_within_hours(start, end):
                removed = calendar.preempt_if_needed(start, end, req.priority)
                if calendar.overlaps_existing(start, end) is None:
                    appt = ConfirmedAppointment(req.patient_id, start, end, req.priority, req.note)
                    calendar.add_appointment(appt)
                    confirmed.append(appt)
                    preempted.extend(removed)
                    continue
                for a in removed:
                    calendar.add_appointment(a)

        rejected.append(req)

    return SchedulingResult(confirmed=confirmed, rejected=rejected, preempted=preempted)
