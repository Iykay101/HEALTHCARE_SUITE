from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import IntEnum


class Priority(IntEnum):
    EMERGENCY = 0
    URGENT = 1
    ROUTINE = 2


@dataclass(frozen=True)
class AppointmentRequest:
    patient_id: str
    requested_start: datetime
    requested_end: datetime
    duration_minutes: int = 15
    priority: Priority = Priority.ROUTINE
    note: str = ""

    def validate(self) -> None:
        if self.requested_end <= self.requested_start:
            raise ValueError("requested_end must be after requested_start")
        if self.duration_minutes <= 0 or self.duration_minutes % 5 != 0:
            raise ValueError("duration_minutes must be positive and a multiple of 5")


@dataclass(frozen=True)
class ConfirmedAppointment:
    patient_id: str
    start: datetime
    end: datetime
    priority: Priority
    note: str = ""

    @property
    def duration(self) -> timedelta:
        return self.end - self.start
