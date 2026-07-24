from typing import NamedTuple

REGION_ABBREVIATIONS = {
    "Los Santos": "LS",
    "Badlands": "BD",
    "San Fierro": "SF",
    #"Las Venturas": "LV",
}

class GoalSpec(NamedTuple):
    option_value: str

    # The mission that ends the run. It becomes the Victory event location.
    mission_id: int

    # Regions the seed generates.
    regions_in_scope: tuple[str, ...]

    # Progressive Mission pool size.
    story_mission_count: int

GOALS = (
    GoalSpec("the_green_sabre", 38, ("Los Santos",), 27),
    GoalSpec("are_you_going_to_san_fierro", 47, ("Los Santos", "Badlands"), 36),
    GoalSpec("yay_ka_boom_boom", 63, ("Los Santos", "Badlands", "San Fierro"), 54),
)

def get_goal(world) -> GoalSpec:
    for goal in GOALS:
        if world.options.end_goal == goal.option_value:
            return goal
    raise ValueError(f"No GoalSpec for end_goal {world.options.end_goal!r} - options.py and GOALS disagree")

def get_included_regions(world) -> set[str]:
    return set(get_goal(world).regions_in_scope)

def get_story_mission_count(world) -> int:
    return get_goal(world).story_mission_count

def get_goal_mission_id(world) -> int:
    return get_goal(world).mission_id

def get_goal_region(world) -> str:
    return get_mission_region(get_goal_mission_id(world))

def get_goal_location_name(world) -> str:
    return get_mission_location_name(get_goal_mission_id(world))

MISSION_DATA = [
    (11, "Big Smoke", "Los Santos"),
    (12, "Ryder", "Los Santos"),
    (13, "Tagging Up Turf", "Los Santos"),
    (14, "Cleaning The Hood", "Los Santos"),
    (15, "Drive-Thru", "Los Santos"),
    (16, "Nines And AK's", "Los Santos"),
    (17, "Drive-By", "Los Santos"),
    (18, "Sweet's Girl", "Los Santos"),
    (19, "Cesar Vialpando", "Los Santos"),
    (20, "Los Sepulcros", "Los Santos"),
    (21, "Doberman", "Los Santos"),
    (22, "Burning Desire", "Los Santos"),
    (23, "Gray Imports", "Los Santos"),
    (24, "Home Invasion", "Los Santos"),
    (25, "Catalyst", "Los Santos"),
    (26, "Robbing Uncle Sam", "Los Santos"),
    (27, "OG Loc", "Los Santos"),
    (28, "Running Dog", "Los Santos"),
    (29, "Wrong Side of the Tracks", "Los Santos"),
    (30, "Just Business", "Los Santos"),
    (31, "Life's a Beach", "Los Santos"),
    (32, "Madd Dogg's Rhymes", "Los Santos"),
    (33, "Management Issues", "Los Santos"),
    (34, "House Party", "Los Santos"),
    (36, "Lowrider (High Stakes)", "Los Santos"),
    (37, "Reuniting The Families", "Los Santos"),
    (38, "The Green Sabre", "Los Santos"),

    # Badlands story missions. First Date (40) and King in Exile (45) are deliberately absent:
    # they are cutscene missions that never set LastMissionPassedName, so they can't be detected
    # (verified in-game) and are not locations. Farewell, My Love (135) is a real separate
    # mission the original ID table had merged into Wu Zi Mu's row - see CheckListener.cpp.
    (39, "Badlands", "Badlands"),
    (41, "Local Liquor Store", "Badlands"),
    (42, "Small Town Bank", "Badlands"),
    (43, "Tanker Commander", "Badlands"),
    (44, "Against All Odds", "Badlands"),
    (46, "Body Harvest", "Badlands"),
    (47, "Are You Going to San Fierro?", "Badlands"),
    (48, "Wu Zi Mu", "Badlands"),
    (135, "Farewell, My Love...", "Badlands"),

    # San Fierro story missions.
    (49, "Wear Flowers in Your Hair", "San Fierro"),
    (50, "Deconstruction", "San Fierro"),
    (51, "555 WE TIP", "San Fierro"),
    (52, "Snail Trail", "San Fierro"),
    (53, "Mountain Cloud Boys", "San Fierro"),
    (54, "Ran Fa Li", "San Fierro"),
    (55, "Lure", "San Fierro"),
    (56, "Amphibious Assault", "San Fierro"),
    (57, "The Da Nang Thang", "San Fierro"),
    (58, "Photo Opportunity", "San Fierro"),
    (59, "Jizzy", "San Fierro"),
    (60, "Outrider", "San Fierro"),
    (61, "Ice Cold Killa", "San Fierro"),
    (62, "Toreno's Last Flight", "San Fierro"),
    (63, "Yay Ka-Boom-Boom", "San Fierro"),
    (64, "Pier 69", "San Fierro"),
    (65, "T-Bone Mendez", "San Fierro"),
    (66, "Mike Toreno", "San Fierro"),

    # Paramedic (122), Firefighter (123), Vigilante (124), Taxi (121) and Burglary (125) are
    # deliberately absent: they pay out per tier rather than once on completion, so their
    # locations live in submission_tier_list.py.
    (114, "Los Santos Gym Fight School", "Los Santos"),
]

MISSION_ID_TO_LOCATION_NAME = {
    mission_id: f"{REGION_ABBREVIATIONS[region]} Mission: {name}"
    for mission_id, name, region in MISSION_DATA
}

MISSION_ID_TO_REGION = {mission_id: region for mission_id, _, region in MISSION_DATA}

def get_mission_location_name(mission_id: int) -> str:
    return MISSION_ID_TO_LOCATION_NAME[mission_id]

def get_mission_region(mission_id: int) -> str:
    return MISSION_ID_TO_REGION[mission_id]