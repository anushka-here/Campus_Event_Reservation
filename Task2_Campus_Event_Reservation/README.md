# Campus Event Seat Reservation API

## Project Description
A FastAPI REST API for managing college events and student seat reservations using SQLite and SQLModel.

## Technologies Used
- FastAPI
- SQLModel
- Pydantic validation
- SQLite
- SQLAlchemy `create_engine()`
- Uvicorn

## Installation

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn main:app --reload
```

## Swagger UI

Open:
http://127.0.0.1:8000/docs

## Event Endpoints

- POST `/events`
- GET `/events`
- GET `/events/{event_id}`
- PUT `/events/{event_id}`
- DELETE `/events/{event_id}`

## Reservation Endpoints

- POST `/events/{event_id}/reserve`
- GET `/events/{event_id}/reservations`
- DELETE `/reservations/{reservation_id}`
- GET `/events/{event_id}/availability`

## Business Logic

Before a reservation is created, the API checks:
1. The event exists.
2. The event status is Open.
3. The number of current reservations is below capacity.

The API rejects a reservation when the event is full or closed.

## Database
SQLite is configured through `create_engine()` in `database.py`. SQLModel creates the tables when the application starts.

## Screenshots
Add your Swagger UI proof screenshots inside the `screenshots/` folder.
