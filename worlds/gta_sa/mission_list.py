from typing import NamedTuple

REGION_ABBREVIATIONS = {
    "Los Santos": "LS",
    "Badlands": "BD",
    "San Fierro": "SF",
    "Las Venturas": "LV",
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
    GoalSpec("a_home_in_the_hills", 102,
             ("Los Santos", "Badlands", "San Fierro", "Las Venturas"), 76),
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

    # Las Venturas story missions - the desert/Toreno arc through the casino arc. They sit in the
    # Las Venturas region rather than the Badlands because they unlock after San Fierro, which is
    # what the region gate models.
    #
    # The six Caligula's heist missions (96-101) are deliberately absent: optional side content
    # whose GXT keys are not verified yet. They take no story position and spend no Progressive
    # Mission - see OPTIONAL_MISSION_IDS in the mod's EntityIDs.h.
    (75, "Monster", "Las Venturas"),
    (76, "Highjack", "Las Venturas"),
    (77, "Interdiction", "Las Venturas"),
    (78, "Verdant Meadows", "Las Venturas"),
    (83, "Learning to Fly", "Las Venturas"),
    (79, "N.O.E.", "Las Venturas"),
    (80, "Stowaway", "Las Venturas"),
    (81, "Black Project", "Las Venturas"),
    (82, "Green Goo", "Las Venturas"),
    (84, "Fender Ketchup", "Las Venturas"),
    (85, "Explosive Situation", "Las Venturas"),
    (86, "You've Had Your Chips", "Las Venturas"),
    (88, "Don Peyote", "Las Venturas"),
    (89, "Intensive Care", "Las Venturas"),
    (90, "The Meat Business", "Las Venturas"),
    (87, "Fish in a Barrel", "Las Venturas"),
    (91, "Freefall", "Las Venturas"),
    (92, "Saint Mark's Bistro", "Las Venturas"),
    (93, "Misappropriation", "Las Venturas"),
    (94, "High Noon", "Las Venturas"),
    (95, "Madd Dogg", "Las Venturas"),
    # Starts in Las Venturas even though the mansion itself is in Los Santos.
    (102, "A Home in the Hills", "Las Venturas"),

    # Optional San Fierro side content.
    (71, "Back to School", "San Fierro"),
    (72, "Air Raid", "San Fierro"),
    (73, "Supply Lines...", "San Fierro"),
    (74, "New Model Army", "San Fierro"),

    # Paramedic (122), Firefighter (123), Vigilante (124), Taxi (121) and Burglary (125) are
    # deliberately absent: they pay out per tier rather than once on completion, so their
    # locations live in submission_tier_list.py.
    (114, "Los Santos Gym Fight School", "Los Santos"),
    (115, "San Fierro Gym Fight School", "San Fierro"),
    (116, "Las Venturas Gym Fight School", "Las Venturas"),
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

class OptionalMissionBranch(NamedTuple):
    name: str
    mission_ids: tuple[int, ...]
    required_progressive_missions: int

OPTIONAL_MISSION_BRANCHES = (
    # Zero's RC missions, off Wear Flowers in Your Hair (story position 36).
    OptionalMissionBranch("Zero", (72, 73, 74), 37),
    # Driving school, off Deconstruction (story position 38).
    OptionalMissionBranch("Driving School", (71,), 39),
)

def get_optional_mission_ids() -> set[int]:
    return {mission_id for branch in OPTIONAL_MISSION_BRANCHES for mission_id in branch.mission_ids}

def get_optional_mission_requirements() -> dict[str, int]:
    """Location name -> Progressive Missions needed, for every optional branch."""
    return {
        get_mission_location_name(mission_id): branch.required_progressive_missions
        for branch in OPTIONAL_MISSION_BRANCHES
        for mission_id in branch.mission_ids
    }