"""Pydantic models dos retornos principais da API do Dionisio.

Parsing tolerante: campos opcionais com default None e `extra="ignore"` para
nao quebrar quando a API retorna campos adicionais. Estes models documentam o
contrato e dao tipagem para o agente — o `DionisioClient` retorna dicts crus;
quem precisar de validacao usa `Model.model_validate(payload)`.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict


class _Base(BaseModel):
    model_config = ConfigDict(extra="ignore")


class BirthDate(_Base):
    day: int | None = None
    month: int | None = None
    year: int | None = None


class Client(_Base):
    id: str
    name: str
    phone: str
    email: str | None = None
    cpf: str | None = None
    gender: Literal["masc", "fem"] | None = None
    birthDate: BirthDate | None = None
    notes: str | None = None
    clientGroupIds: list[str] = []
    createdAt: int | None = None
    updatedAt: int | None = None


class ClientInsights(_Base):
    clientId: str
    visitsCount: int = 0
    noShowCount: int = 0
    totalSpent: int = 0
    spentThisMonth: int = 0
    couponsUsed: int = 0
    firstVisitAt: int | None = None
    lastVisitAt: int | None = None
    averageTicket: int = 0


class ReservationStatus(str, Enum):
    pending = "pending"
    awaiting_payment = "awaiting_payment"
    confirmed = "confirmed"
    seated = "seated"
    completed = "completed"
    cancelled = "cancelled"
    cancelled_by_client = "cancelled_by_client"
    cancelled_by_business = "cancelled_by_business"
    no_show = "no_show"


class Duration(_Base):
    start: int
    end: int


class PartySize(_Base):
    adults: int = 0
    children: int = 0
    total: int = 0


class Cancellation(_Base):
    reasonCode: str | None = None
    reasonText: str | None = None


class Reservation(_Base):
    id: str
    clientId: str
    areaId: str | None = None
    tableId: str | None = None
    duration: Duration | None = None
    partySize: PartySize | None = None
    status: ReservationStatus | None = None
    description: str | None = None
    cancellation: Cancellation | None = None
    createdAt: int | None = None
    updatedAt: int | None = None


class AvailabilityArea(_Base):
    id: str
    name: str
    capacity: int = 0


class AvailabilitySlot(_Base):
    time: str
    capacity: int = 0
    booked: int = 0
    free: int = 0


class Availability(_Base):
    date: str | None = None
    totalCapacity: int = 0
    areas: list[AvailabilityArea] = []
    slots: list[AvailabilitySlot] = []


class ErrorResponse(_Base):
    error: str
    code: str
