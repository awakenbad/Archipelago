from __future__ import annotations

from typing import NamedTuple

class Challenge(NamedTuple):
    location_id: int
    skill_item: str
    gates: bool = True

CHALLENGES = [
    Challenge(133, "Max Cycling Skill", gates=True),
    Challenge(136, "Max Bike Skill", gates=False),
    Challenge(132, "Max Cycling Skill", gates=True),
]

CHALLENGE_LOCATION_IDS = {challenge.location_id for challenge in CHALLENGES}
