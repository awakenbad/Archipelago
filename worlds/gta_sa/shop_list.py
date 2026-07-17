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

# Only the stock reachable in the current Los Santos-only scope (goal: The Green Sabre) is
# included as locations. Vanilla unlocks the rest after San Fierro+ missions (AK-47 after
# Lure, Sniper after Pier 69, M4 after Yay Ka-Boom-Boom, Desert Eagle after Black Project,
# Combat Shotgun after Don Peyote, Country Rifle after Body Harvest, Satchel Charge after
# Against All Odds) - add them with proper gates when those regions get populated.
# Value = Progressive Mission count required, following rules.py's story-order convention:
# the shop itself opens after Doberman (story index 10 -> 11), Silenced Pistol needs Gray
# Imports (11 -> 12), Sawn-off Shotgun needs Just Business (18 -> 19).
INCLUDED_SHOP_SLOTS = {
    0: 11,   # Pistol - base stock
    1: 12,   # Silenced Pistol - after Gray Imports
    3: 11,   # Grenade - base stock
    4: 11,   # Shotgun - base stock
    6: 19,   # Sawn-off Shotgun - after Just Business
    7: 11,   # Micro Uzi - base stock
    8: 11,   # Tec-9 - base stock
    15: 11,  # Armor - base stock
}
