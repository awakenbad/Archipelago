from __future__ import annotations

from typing import NamedTuple

class Challenge(NamedTuple):
    location_id: int
    gate_item: str
    gate_item_id: int
    effect: str

CHALLENGES = [
    Challenge(133, "Max Cycling Skill", 130, "max_cycling_skill"),
]

CHALLENGE_LOCATION_IDS = {challenge.location_id for challenge in CHALLENGES}
CHALLENGE_GATE_ITEMS = {challenge.gate_item: challenge.gate_item_id for challenge in CHALLENGES}
