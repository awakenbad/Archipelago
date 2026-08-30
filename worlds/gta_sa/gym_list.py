from typing import NamedTuple

GYM_SKILL_ITEM = "Max Muscle"

class Gym(NamedTuple):
    location_id: int
    required_count: int

GYMS = (
    Gym(114, 5),
    Gym(115, 36),
    Gym(116, 54),
)

GYM_LOCATION_IDS = {gym.location_id for gym in GYMS}
