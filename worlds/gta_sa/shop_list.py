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

def gate_after(mission_location_name: str) -> int:
    return get_story_index(LOCATION_NAME_TO_MISSION_ID[mission_location_name]) + 1

_STOCKED_AFTER = gate_after("LS Mission: Doberman")
INCLUDED_SHOP_SLOTS = {
    0: _STOCKED_AFTER,   # Pistol
    1: _STOCKED_AFTER,   # Silenced Pistol
    3: _STOCKED_AFTER,   # Grenade
    4: _STOCKED_AFTER,   # Shotgun
    6: _STOCKED_AFTER,   # Sawn-off Shotgun
    7: _STOCKED_AFTER,   # Micro Uzi
    8: _STOCKED_AFTER,   # Tec-9
    15: _STOCKED_AFTER,  # Armor
}
