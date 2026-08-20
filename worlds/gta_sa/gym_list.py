from typing import NamedTuple

GYM_SKILL_ITEM = "Max Muscle"

class Gym(NamedTuple):
    location_id: int
    location_name: str
    required_count: int

GYMS = (
    Gym(114, "LS Mission: Los Santos Gym Fight School", 5),
    Gym(115, "SF Mission: San Fierro Gym Fight School", 36),
    Gym(116, "LV Mission: Las Venturas Gym Fight School", 54),
)
