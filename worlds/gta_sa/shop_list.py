SHOP_BASE_ID = 300
SHOP_REGION = "Los Santos"

# Must match the C++ side's shopItems table in AmmuNationShop.h exactly - the index in this
# list is the CHECK:SHOP:<n> slot id the plugin sends.
SHOP_ITEM_NAMES = [
    "Pistol",            # 0
    "Silenced Pistol",   # 1
    "Desert Eagle",      # 2
    "Grenade",           # 3
    "Shotgun",           # 4
    "Combat Shotgun",    # 5
    "Sawn-off Shotgun",  # 6
    "Micro Uzi",         # 7
    "Tec-9",             # 8
    "MP5",               # 9
    "AK-47",             # 10
    "M4",                # 11
    "Country Rifle",     # 12
    "Sniper Rifle",      # 13
    "Satchel Charge",    # 14
    "Armor",             # 15
]

SHOP_LOCATION_NAMES = [f"Ammu-Nation: {name}" for name in SHOP_ITEM_NAMES]

from .mission_list import LOCATION_NAME_TO_MISSION_ID, get_story_index

_SHOP_OPENS = "LS Mission: Doberman"

INCLUDED_SHOP_SLOTS = {
    0: (_SHOP_OPENS,),                                      # Pistol
    3: (_SHOP_OPENS,),                                      # Grenade
    4: (_SHOP_OPENS,),                                      # Shotgun
    7: (_SHOP_OPENS,),                                      # Micro Uzi
    8: (_SHOP_OPENS,),                                      # Tec-9
    15: (_SHOP_OPENS,),                                     # Armor
    9: (_SHOP_OPENS, "LS Mission: Robbing Uncle Sam"),      # MP5          - ryder > 2
    6: (_SHOP_OPENS, "LS Mission: Just Business"),          # Sawn-off     - smoke > 3
    1: (_SHOP_OPENS, "LS Mission: House Party"),            # Silenced     - strap > 4
    12: (_SHOP_OPENS, "BD Mission: Body Harvest"),          # Country Rifle   - truth > 0
    14: (_SHOP_OPENS, "BD Mission: Body Harvest"),          # Satchel Charge  - truth > 0 covers cat4
    10: (_SHOP_OPENS, "SF Mission: Mountain Cloud Boys"),   # AK-47           - wuzi > 0
    13: (_SHOP_OPENS, "SF Mission: Mountain Cloud Boys"),   # Sniper Rifle    - wuzi > 0 covers synd > 7
    11: (_SHOP_OPENS, "SF Mission: Yay Ka-Boom-Boom"),      # M4              - synd > 9
    2: (_SHOP_OPENS, "LV Mission: Black Project"),          # Desert Eagle    - desert > 7
    5: (_SHOP_OPENS, "LV Mission: You've Had Your Chips"),  # Combat Shotgun  - casino > 2
}

def required_story_count(prerequisites: tuple[str, ...]) -> int:
    indices = []
    for name in prerequisites:
        story_index = get_story_index(LOCATION_NAME_TO_MISSION_ID[name])
        if story_index is None:
            raise ValueError(f"{name} gates a shop slot but is not a story mission")
        indices.append(story_index)
    return max(indices) + 1
