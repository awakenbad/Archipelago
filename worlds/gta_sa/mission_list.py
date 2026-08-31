from typing import NamedTuple

from .branch_list import BRANCHES
from .challenge_list import CHALLENGE_LOCATION_IDS
from .gym_list import GYM_LOCATION_IDS
from .stadium_list import STADIUM_LOCATION_IDS

REGION_ABBREVIATIONS = {
    "Los Santos": "LS",
    "Badlands": "BD",
    "San Fierro": "SF",
    "Las Venturas": "LV",
    "Return to Los Santos": "RTLS",
}

COMPLETION_ID = 160

class StoryMilestone(NamedTuple):
    """One cut point on the story order, usable as a starting point, a goal, or both.

    Adding a milestone is one row here plus the matching option value - it becomes available as
    both ends of a seed at once, which is what keeps start/goal from drifting into two tables
    that have to be kept in sync by hand.
    """

    # Story positions completed at this point. As a goal that is the Progressive Mission pool
    # size; as a starting point it is how many positions the shipped save has already spent.
    story_index: int

    # Names where the player begins. None when this milestone cannot be a starting point -
    # the last one can't, since there is no goal beyond it.
    start_option_value: str | None

    # Names the mission that ends the run, and that mission's id - it becomes the Victory event
    # location. Both None when this milestone cannot be a goal (the game's opening).
    goal_option_value: str | None
    goal_mission_id: int | None

    # Regions the seed generates when this is the goal. Independent of the starting point:
    # map access is cumulative and Los Santos never re-locks, so a later start needs the same
    # regions, just fewer story missions inside them.
    regions_in_scope: tuple[str, ...]

MILESTONES = (
    StoryMilestone(0,  "los_santos",   None,                          None, ("Los Santos",)),
    StoryMilestone(27, "badlands",     "the_green_sabre",               38, ("Los Santos",)),
    StoryMilestone(36, "san_fierro",   "are_you_going_to_san_fierro",   47, ("Los Santos", "Badlands")),
    StoryMilestone(54, "las_venturas", "yay_ka_boom_boom",              63, ("Los Santos", "Badlands", "San Fierro")),
    StoryMilestone(76, None, "a_home_in_the_hills",  102,
                   ("Los Santos", "Badlands", "San Fierro", "Las Venturas")),
    StoryMilestone(84, None,           "end_of_the_line",              112,
                   ("Los Santos", "Badlands", "San Fierro", "Las Venturas", "Return to Los Santos")),
    StoryMilestone(84, None,           "one_hundred_percent",          COMPLETION_ID,
                   ("Los Santos", "Badlands", "San Fierro", "Las Venturas", "Return to Los Santos")),
)

def get_goal(world) -> StoryMilestone:
    for milestone in MILESTONES:
        if milestone.goal_option_value is not None and world.options.end_goal == milestone.goal_option_value:
            return milestone
    raise ValueError(f"No milestone for end_goal {world.options.end_goal!r} - options.py and MILESTONES disagree")

def get_start(world) -> StoryMilestone:
    for milestone in MILESTONES:
        if milestone.start_option_value is not None and world.options.starting_point == milestone.start_option_value:
            return milestone
    raise ValueError(
        f"No milestone for starting_point {world.options.starting_point!r} - options.py and MILESTONES disagree"
    )

def get_included_regions(world) -> set[str]:
    return set(get_goal(world).regions_in_scope)

def get_story_mission_count(world) -> int:
    return get_goal(world).story_index

def get_start_index(world) -> int:
    return get_start(world).story_index

def get_goal_mission_id(world) -> int:
    return get_goal(world).goal_mission_id

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

    # Badlands story missions.
    (39, "Badlands", "Badlands"),
    (41, "First Date", "Badlands"),
    (42, "First Base", "Badlands"),
    (43, "Gone Courting", "Badlands"),
    (44, "Made in Heaven", "Badlands"),
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

    # Las Venturas story missions.
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

    # Return to Los Santos story missions
    (103, "Vertical Bird", "Return to Los Santos"),
    (104, "Home Coming", "Return to Los Santos"),
    (105, "Cut Throat Business", "Return to Los Santos"),
    (106, "Beat Down on B Dup", "Return to Los Santos"),
    (107, "Grove 4 Life", "Return to Los Santos"),
    (108, "Riot", "Return to Los Santos"),
    (109, "Los Desperados", "Return to Los Santos"),
    (112, "End of the Line", "Return to Los Santos"),

    # Optional Las Venturas side content: the Caligula's heist.
    (96, "Architectural Espionage", "Las Venturas"),
    (97, "Key To Her Heart", "Las Venturas"),
    (98, "Dam And Blast", "Las Venturas"),
    (99, "Cop Wheels", "Las Venturas"),
    (100, "Up, Up and Away!", "Las Venturas"),
    (101, "Breaking the Bank at Caligula's", "Las Venturas"),

    # Optional San Fierro side content.
    (71, "Back to School", "San Fierro"),
    (72, "Air Raid", "San Fierro"),
    (73, "Supply Lines...", "San Fierro"),
    (74, "New Model Army", "San Fierro"),
    (67, "Zeroing In", "San Fierro"),
    (68, "Test Drive", "San Fierro"),
    (69, "Customs Fast Track", "San Fierro"),
    (70, "Puncture Wounds", "San Fierro"),

    (114, "Fight School", "Los Santos"),
    (115, "Fight School", "San Fierro"),
    (116, "Fight School", "Las Venturas"),
    (133, "BMX", "Los Santos"),
    (136, "NRG-500", "San Fierro"),
    (132, "Chiliad", "Badlands"),
    (COMPLETION_ID, "100% Completion", "Return to Los Santos"),
    # Stadium events
    (140, "8-Track", "Los Santos"),
    (141, "Dirt Track", "Las Venturas"),
    (142, "Blood Ring", "San Fierro"),
    (143, "Kickstart", "Las Venturas"),
]

class OptionalMissionBranch(NamedTuple):
    name: str
    mission_ids: tuple[int, ...]
    required_progressive_missions: int

OPTIONAL_MISSION_BRANCHES = (
    OptionalMissionBranch("Zero", (72, 73, 74), 37),
    OptionalMissionBranch("Driving School", (71,), 39),
    OptionalMissionBranch("Wang Cars", (67, 68, 69, 70), 54),
    OptionalMissionBranch("Heist", (96, 97, 98, 99, 100), 65),
    OptionalMissionBranch("Heist", (101,), 75),
)

_BRANCH_LABEL_BY_MISSION_ID = {
    mission_id: branch.name for branch in BRANCHES for mission_id in branch.missions
}
_BRANCH_LABEL_BY_MISSION_ID.update({
    mission_id: branch.name
    for branch in OPTIONAL_MISSION_BRANCHES for mission_id in branch.mission_ids
})
_BRANCH_LABEL_BY_MISSION_ID.update(dict.fromkeys(GYM_LOCATION_IDS, "Gym"))
_BRANCH_LABEL_BY_MISSION_ID.update(dict.fromkeys(CHALLENGE_LOCATION_IDS, "Challenge"))
_BRANCH_LABEL_BY_MISSION_ID.update(dict.fromkeys(STADIUM_LOCATION_IDS, "Stadium"))
for mission_id, mission_name, _ in MISSION_DATA:
    if _BRANCH_LABEL_BY_MISSION_ID.get(mission_id) == mission_name:
        del _BRANCH_LABEL_BY_MISSION_ID[mission_id]

def get_branch_label(mission_id: int) -> str:
    return _BRANCH_LABEL_BY_MISSION_ID.get(mission_id, "Mission")

MISSION_ID_TO_LOCATION_NAME = {
    mission_id: f"{REGION_ABBREVIATIONS[region]} {get_branch_label(mission_id)}: {name}"
    for mission_id, name, region in MISSION_DATA
}

MISSION_ID_TO_REGION = {mission_id: region for mission_id, _, region in MISSION_DATA}

def get_mission_location_name(mission_id: int) -> str:
    return MISSION_ID_TO_LOCATION_NAME[mission_id]

def get_mission_region(mission_id: int) -> str:
    return MISSION_ID_TO_REGION[mission_id]

LOCATION_NAME_TO_MISSION_ID = {name: mission_id for mission_id, name in MISSION_ID_TO_LOCATION_NAME.items()}
MISSION_NAME_TO_ID = {name: mission_id for mission_id, name, _ in MISSION_DATA}

STORY_MISSION_NAME_ORDER = (
    "Big Smoke",                                # 0
    "Ryder",                                    # 1
    "Tagging Up Turf",                          # 2
    "Cleaning The Hood",                        # 3
    "Drive-Thru",                               # 4
    "Nines And AK's",                           # 5  - opens the parallel strands
    "Drive-By",                                 # 6
    "Sweet's Girl",                             # 7
    "Cesar Vialpando",                          # 8
    "Lowrider (High Stakes)",                   # 9  - only needs Cesar Vialpando
    "OG Loc",                                   # 10
    "Running Dog",                              # 11
    "Wrong Side of the Tracks",                 # 12
    "Just Business",                            # 13
    "Home Invasion",                            # 14
    "Catalyst",                                 # 15
    "Robbing Uncle Sam",                        # 16
    "Life's a Beach",                           # 17
    "Madd Dogg's Rhymes",                       # 18
    "Management Issues",                        # 19
    "House Party",                              # 20
    "Burning Desire",                           # 21 - needs Madd Dogg's Rhymes
    "Gray Imports",                             # 22 - needs Burning Desire
    "Doberman",                                 # 23 - needs Cesar Vialpando + Burning Desire
    "Los Sepulcros",                            # 24 - needs Doberman
    "Reuniting The Families",                   # 25
    "The Green Sabre",                          # 26

    "Badlands",                                 # 27
    "First Date",                               # 28
    "Body Harvest",                             # 29
    "First Base",                               # 30
    "Wu Zi Mu",                                 # 31 - unlocks after 2 robberies
    "Gone Courting",                            # 32
    "Made in Heaven",                           # 33
    "Farewell, My Love...",                     # 34
    "Are You Going to San Fierro?",             # 35

    "Wear Flowers in Your Hair",                # 36 - first SF mission, opens the garage
    "555 WE TIP",                               # 37
    "Deconstruction",                           # 38
    "Photo Opportunity",                        # 39
    "Jizzy",                                    # 40
    "T-Bone Mendez",                            # 41
    "Mountain Cloud Boys",                      # 42
    "Mike Toreno",                              # 43
    "Ran Fa Li",                                # 44
    "Outrider",                                 # 45
    "Lure",                                     # 46
    "Snail Trail",                              # 47
    "Amphibious Assault",                       # 48
    "Ice Cold Killa",                           # 49
    "The Da Nang Thang",                        # 50
    "Pier 69",                                  # 51
    "Toreno's Last Flight",                     # 52
    "Yay Ka-Boom-Boom",                         # 53 - ends San Fierro

    "Monster",                                  # 54 - first of Toreno's desert arc
    "Highjack",                                 # 55
    "Interdiction",                             # 56
    "Verdant Meadows",                          # 57 - buys the airstrip
    "Learning to Fly",                          # 58 - flight school, gates every mission after it
    "N.O.E.",                                   # 59
    "Stowaway",                                 # 60
    "Black Project",                            # 61
    "Green Goo",                                # 62
    "Fender Ketchup",                           # 63 - casino arc starts
    "Explosive Situation",                      # 64
    "You've Had Your Chips",                    # 65
    "Don Peyote",                               # 66
    "Intensive Care",                           # 67
    "The Meat Business",                        # 68
    "Fish in a Barrel",                         # 69 - opens off The Meat Business
    "Madd Dogg",                                # 70 - also opens off The Meat Business
    "Misappropriation",                         # 71 - needs Intensive Care
    "Freefall",                                 # 72
    "High Noon",                                # 73 - needs Misappropriation + Freefall
    "Saint Mark's Bistro",                      # 74 - needs every other Las Venturas mission
    "A Home in the Hills",                      # 75 - opens the Los Santos endgame

    "Vertical Bird",                            # 76
    "Home Coming",                              # 77
    "Cut Throat Business",                      # 78
    "Beat Down on B Dup",                       # 79
    "Grove 4 Life",                             # 80
    "Riot",                                     # 81
    "Los Desperados",                           # 82
    "End of the Line",                          # 83
)

STORY_MISSION_ORDER = tuple(MISSION_NAME_TO_ID[name] for name in STORY_MISSION_NAME_ORDER)

STORY_INDEX_BY_MISSION_ID = {mission_id: index for index, mission_id in enumerate(STORY_MISSION_ORDER)}

def get_story_index(mission_id: int) -> int | None:
    """The mission's position in the story, or None when it isn't a story mission."""
    return STORY_INDEX_BY_MISSION_ID.get(mission_id)

def get_optional_mission_ids() -> set[int]:
    return {mission_id for branch in OPTIONAL_MISSION_BRANCHES for mission_id in branch.mission_ids}

def get_optional_branch_requirements_by_id() -> dict[int, int]:
    """Mission ID -> Progressive Missions needed, for every optional branch."""
    return {
        mission_id: branch.required_progressive_missions
        for branch in OPTIONAL_MISSION_BRANCHES
        for mission_id in branch.mission_ids
    }

def get_optional_mission_requirements() -> dict[str, int]:
    """Location name -> Progressive Missions needed, for every optional branch."""
    return {
        get_mission_location_name(mission_id): branch.required_progressive_missions
        for branch in OPTIONAL_MISSION_BRANCHES
        for mission_id in branch.mission_ids
    }
