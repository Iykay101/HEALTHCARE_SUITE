from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from .models import ConfirmedAppointment, Priority


def _ceil_to(minutes: int, dt: datetime) -> datetime:
    epoch = datetime(dt.year, dt.month, dt.day)
    minutes_since = int((dt - epoch).total_seconds() // 60)
    rounded = ((minutes_since + minutes - 1) // minutes) * minutes
    return epoch + timedelta(minutes=rounded)


@dataclass
class DoctorCalendar:
    open_time: datetime
    close_time: datetime
    slot_minutes: int = 5

    def __post_init__(self) -> None:
        if self.close_time <= self.open_time:
            raise ValueError("close_time must be after open_time")
        if self.slot_minutes <= 0:
            raise ValueError("slot_minutes must be positive")
        self._appts: List[ConfirmedAppointment] = []

    @property
    def appointments(self) -> List[ConfirmedAppointment]:
        return list(self._appts)

    def is_within_hours(self, start: datetime, end: datetime) -> bool:
        return self.open_time <= start and end <= self.close_time

    def overlaps_existing(self, start: datetime, end: datetime) -> Optional[ConfirmedAppointment]:
        for appt in self._appts:
            if not (end <= appt.start or start >= appt.end):
                return appt
        return None

    def add_appointment(self, appt: ConfirmedAppointment) -> None:
        if not self.is_within_hours(appt.start, appt.end):
            raise ValueError("appointment outside working hours")
        if self.overlaps_existing(appt.start, appt.end):
            raise ValueError("appointment overlaps existing")
        self._appts.append(appt)
        self._appts.sort(key=lambda a: a.start)

    def remove_appointment(self, appt: ConfirmedAppointment) -> None:
        self._appts = [a for a in self._appts if a != appt]

    def find_first_fit(
        self,
        window_start: datetime,
        window_end: datetime,
        duration: timedelta,
        step_minutes: Optional[int] = None,
    ) -> Optional[Tuple[datetime, datetime]]:
        step = step_minutes or self.slot_minutes
        cursor = _ceil_to(step, max(window_start, self.open_time))
        latest_start = min(window_end, self.close_time) - duration
        while cursor <= latest_start:
            end = cursor + duration
            if end <= self.close_time and self.overlaps_existing(cursor, end) is None:
                return cursor, end
            cursor += timedelta(minutes=step)
        return None

    def preempt_if_needed(self, start: datetime, end: datetime, incoming_priority: Priority) -> List[ConfirmedAppointment]:
        removed: List[ConfirmedAppointment] = []
        for appt in list(self._appts):
            if not (end <= appt.start or start >= appt.end):
                if incoming_priority < appt.priority:
                    self.remove_appointment(appt)
                    removed.append(appt)
        return removed
