from typing import NamedTuple

class StadiumEvent(NamedTuple):
    location_id: int
    skill_item: str | None = None

STADIUM_EVENTS = (
    StadiumEvent(140, "Max Driving Skill"),   # 8-Track
    StadiumEvent(141, "Max Bike Skill"),      # Dirt Track
    StadiumEvent(142),                        # Blood Ring
    StadiumEvent(143),                        # Kickstart
)

STADIUM_LOCATION_IDS = {event.location_id for event in STADIUM_EVENTS}
