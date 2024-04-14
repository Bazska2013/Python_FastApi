from fastapi import APIRouter, HTTPException
from typing import List

from .event_analyzer import EventAnalyzer
from .models import Event
from .file_storage import EventFileManager

router = APIRouter()


def event_exists(event_id: int) -> bool:
    events = EventFileManager.read_events_from_file()
    for event in events:
        if event["id"] == event_id:
            return True
    return False


@router.get("/events", response_model=List[Event])
async def get_all_events():
    return EventFileManager.read_events_from_file()


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager.read_events_from_file()
    if date:
        events = [event for event in events if event["date"] == date]
    if organizer:
        events = [event for event in events if event["organizer"] == organizer]
    if status:
        events = [event for event in events if event["status"] == status]
    if event_type:
        events = [event for event in events if event["type"] == event_type]
    return events


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager.read_events_from_file()
    for event in events:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event Not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    if event_exists(event.id):
        raise HTTPException(status_code=400, detail="Event ID already exists")
    events = EventFileManager.read_events_from_file()
    events.append(event.dict())
    EventFileManager.write_events_to_file(events)
    return event


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    if not event_exists(event_id):
        raise HTTPException(status_code=404, detail="Event Not found")
    events = EventFileManager.read_events_from_file()
    for i in range(len(events)):
        if events[i]["id"] == event_id:
            events[i] = event.dict()
            EventFileManager.write_events_to_file(events)
            return event
    raise HTTPException(status_code=404, detail="Event Not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    if not event_exists(event_id):
        raise HTTPException(status_code=404, detail="Event Not found")
    events = EventFileManager.read_events_from_file()
    events = [event for event in events if event["id"] != event_id]
    EventFileManager.write_events_to_file(events)
    return {"message": "Event deleted successfully"}


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    events = EventFileManager.read_events_from_file()
    joiners = EventAnalyzer.get_joiners_multiple_meetings_method(events)
    if not joiners:
        return "No joiners attending at least 2 meetings"
    return joiners
