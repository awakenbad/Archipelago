from __future__ import annotations

from typing import NamedTuple

class Challenge(NamedTuple):
    location_id: int
    skill_item: str
    skill_item_id: int
    effect: str
    gates: bool = True

CHALLENGES = [
    Challenge(133, "Max Cycling Skill", 130, "max_cycling_skill", gates=True),
    Challenge(136, "Max Bike Skill", 131, "max_bike_skill", gates=False),
    Challenge(132, "Max Cycling Skill", 130, "max_cycling_skill", gates=True),
]

CHALLENGE_LOCATION_IDS = {challenge.location_id for challenge in CHALLENGES}
