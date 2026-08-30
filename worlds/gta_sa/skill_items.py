from typing import NamedTuple

class SkillItem(NamedTuple):
    name: str
    item_id: int
    effect: str

    generated_by_default: bool

SKILL_ITEMS = (
    SkillItem("Max Cycling Skill", 130, "max_cycling_skill", generated_by_default=False),
    SkillItem("Max Bike Skill", 131, "max_bike_skill", generated_by_default=True),
    SkillItem("Max Driving Skill", 132, "max_driving_skill", generated_by_default=True),
    SkillItem("Max Muscle", 133, "max_muscle", generated_by_default=True),
)

SKILL_ITEM_IDS = {item.name: item.item_id for item in SKILL_ITEMS}

DEFAULT_SKILL_ITEMS = tuple(item.name for item in SKILL_ITEMS if item.generated_by_default)
