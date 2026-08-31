from .mission_list import get_mission_location_name, get_story_index

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

_SHOP_OPENS = 21  # Doberman

INCLUDED_SHOP_SLOTS = {
    0: (_SHOP_OPENS,),        # Pistol
    3: (_SHOP_OPENS,),        # Grenade
    4: (_SHOP_OPENS,),        # Shotgun
    7: (_SHOP_OPENS,),        # Micro Uzi
    8: (_SHOP_OPENS,),        # Tec-9
    15: (_SHOP_OPENS,),       # Armor
    9: (_SHOP_OPENS, 26),     # MP5             - ryder > 2,  Robbing Uncle Sam
    6: (_SHOP_OPENS, 30),     # Sawn-off        - smoke > 3,  Just Business
    1: (_SHOP_OPENS, 34),     # Silenced        - strap > 4,  House Party
    12: (_SHOP_OPENS, 46),    # Country Rifle   - truth > 0,  Body Harvest
    14: (_SHOP_OPENS, 46),    # Satchel Charge  - truth > 0 covers cat4
    10: (_SHOP_OPENS, 53),    # AK-47           - wuzi > 0,   Mountain Cloud Boys
    13: (_SHOP_OPENS, 53),    # Sniper Rifle    - wuzi > 0 covers synd > 7
    11: (_SHOP_OPENS, 63),    # M4              - synd > 9,   Yay Ka-Boom-Boom
    2: (_SHOP_OPENS, 81),     # Desert Eagle    - desert > 7, Black Project
    5: (_SHOP_OPENS, 86),     # Combat Shotgun  - casino > 2, You've Had Your Chips
}

def required_story_count(prerequisites: tuple[int, ...]) -> int:
    indices = []
    for mission_id in prerequisites:
        story_index = get_story_index(mission_id)
        if story_index is None:
            raise ValueError(
                f"{get_mission_location_name(mission_id)} gates a shop slot but is not a story mission"
            )
        indices.append(story_index)
    return max(indices) + 1
