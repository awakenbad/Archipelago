from typing import NamedTuple

class SkillItem(NamedTuple):
    name: str
    item_id: int
    effect: str

    always_generated: bool

SKILL_ITEMS = (
    SkillItem("Max Cycling Skill", 130, "max_cycling_skill", always_generated=False),
    SkillItem("Max Bike Skill", 131, "max_bike_skill", always_generated=True),
    SkillItem("Max Driving Skill", 132, "max_driving_skill", always_generated=True),
    SkillItem("Max Muscle", 133, "max_muscle", always_generated=True),
)

SKILL_ITEM_IDS = {item.name: item.item_id for item in SKILL_ITEMS}

ALWAYS_GENERATED_SKILL_ITEMS = tuple(item.name for item in SKILL_ITEMS if item.always_generated)
