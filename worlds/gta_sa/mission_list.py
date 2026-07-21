REGION_ABBREVIATIONS = {
    "Los Santos": "LS",
    "Badlands": "BD",
    #"San Fierro": "SF",
    #"Las Venturas": "LV",
}

# Content past the end goal is left out of the seed entirely. If it were still generated,
# another player's progression item could land in a region this seed never requires visiting -
# the GTA player would legitimately stop at their goal and strand it. Both helpers key off the
# same option so the scope can't drift apart.
def badlands_in_scope(world) -> bool:
    return world.options.end_goal == "are_you_going_to_san_fierro"

def get_included_regions(world) -> set[str]:
    return {"Los Santos", "Badlands"} if badlands_in_scope(world) else {"Los Santos"}

# Story-mission positions in play, indexing into rules.py's story_mission_order
# (Los Santos is 0-26, Badlands 27-35). Also the Progressive Mission pool size: the goal sits
# at the last position and needs that many items, leaving exactly one spare.
def get_story_mission_count(world) -> int:
    return 36 if badlands_in_scope(world) else 27

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

    (121, "Taxi Driver 50 Fares", "Los Santos"),
    (122, "Paramedic Level 12", "Los Santos"),
    (123, "Firefighter Level 12", "Los Santos"),
    (124, "Vigilante Level 12", "Los Santos"),
    (125, "Burglary $10,000 Stolen", "Los Santos"),
    (114, "Los Santos Gym Fight School", "Los Santos"),
]