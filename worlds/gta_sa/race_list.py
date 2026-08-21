from typing import NamedTuple

class RaceGroup(NamedTuple):
    region: str
    first_index: int
    names: tuple[str, ...]

RACE_GROUPS = (
    RaceGroup("Los Santos", 0, (
        "Lowrider Race",
        "Little Loop",
        "Backroad Wanderer",
        "City Circuit",
        "Vinewood",
        "Freeway",
        "Into the Country",
        "Badlands A",
        "Badlands B",
    )),
    RaceGroup("San Fierro", 9, (
        "Dirtbike Danger",
        "Bandito County",
        "Go-Go Karting",
        "San Fierro Fastlane",
        "San Fierro Hills",
        "Country Endurance",
    )),
    RaceGroup("Las Venturas", 15, (
        "SF to LV",
        "Dam Rider",
        "Desert Tricks",
        "LV Ringroad",
        "World War Ace",
        "Barnstorming",
        "Military Service",
        "Chopper Checkpoint",
        "Whirly Bird Waypoint",
        "Heli Hell",
    )),
)

RACE_COUNT = sum(len(group.names) for group in RACE_GROUPS)
