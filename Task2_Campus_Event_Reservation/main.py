from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models import Event, Reservation

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Campus Event Seat Reservation API",
    description="REST API for managing college events and student reservations.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: Event):
    with Session(engine) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

@app.get("/events", response_model=list[Event])
def get_events():
    with Session(engine) as session:
        return session.exec(select(Event)).all()

@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, updated_event: Event):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        booked = len(session.exec(
            select(Reservation).where(Reservation.event_id == event_id)
        ).all())

        if updated_event.capacity < booked:
            raise HTTPException(
                status_code=400,
                detail=f"Capacity cannot be less than current booked seats ({booked})"
            )

        event.title = updated_event.title
        event.venue = updated_event.venue
        event.capacity = updated_event.capacity
        event.organizer = updated_event.organizer
        event.status = updated_event.status

        session.add(event)
        session.commit()
        session.refresh(event)
        return event

@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        reservations = session.exec(
            select(Reservation).where(Reservation.event_id == event_id)
        ).all()

        for reservation in reservations:
            session.delete(reservation)

        session.delete(event)
        session.commit()
        return {"message": "Event and its reservations deleted successfully"}

@app.post("/events/{event_id}/reserve", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(event_id: int, reservation: Reservation):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.status != "Open":
            raise HTTPException(
                status_code=400,
                detail="Reservations are closed for this event"
            )

        booked = len(session.exec(
            select(Reservation).where(Reservation.event_id == event_id)
        ).all())

        if booked >= event.capacity:
            raise HTTPException(
                status_code=400,
                detail="Event is full. No remaining seats."
            )

        reservation.event_id = event_id
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation

@app.get("/events/{event_id}/reservations", response_model=list[Reservation])
def get_reservations(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        statement = select(Reservation).where(Reservation.event_id == event_id)
        return session.exec(statement).all()

@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int):
    with Session(engine) as session:
        reservation = session.get(Reservation, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        session.delete(reservation)
        session.commit()
        return {"message": "Reservation cancelled successfully"}

@app.get("/events/{event_id}/availability")
def event_availability(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        booked = len(session.exec(
            select(Reservation).where(Reservation.event_id == event_id)
        ).all())

        return {
            "capacity": event.capacity,
            "booked": booked,
            "remaining": event.capacity - booked
        }
