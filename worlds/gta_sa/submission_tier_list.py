from typing import NamedTuple

from .race_list import RACE_GROUPS

from .mission_list import REGION_ABBREVIATIONS

SUBMISSION_TIER_BASE_ID = 1000

DRIVING_SCHOOL_TESTS = (
    "The 360",
    "The 180",
    "Whip and Terminate",
    "Pop and Control",
    "Burn and Lap",
    "Cone Coil",
    "The '90'",
    "Wheelie Weave",
    "Spin and Go",
    "P.I.T. Maneuver",
    "Alley Oop",
    "City Slicking",
)

# In the school's own order, matching FLYING_SCHOOL_SCORE_GLOBALS in the mod's EntityIDs.h. Names
# are from american.gxt, title-cased for consistency with the rest of the location names.
FLYING_SCHOOL_LESSONS = (
    "Takeoff",
    "Land Plane",
    "Circle Airstrip",
    "Circle Airstrip and Land",
    "Helicopter Takeoff",
    "Land Helicopter",
    "Destroy Targets",
    "Loop-the-Loop",
    "Barrel Roll",
    "Parachute onto Target",
)

BOAT_SCHOOL_TESTS = (
    "Basic Seamanship",
    "Plot a Course",
    "Fresh Slalom",
    "Flying Fish",
    "Land, Sea and Air",
)

BIKE_SCHOOL_TESTS = (
    "The 360",
    "The 180",
    "The Wheelie",
    "The Stoppie",
    "Jump & Stop",
    "Jump & Stoppie",
)

SCHOOL_MEDALS = ("Bronze", "Silver", "Gold")

SHOOTING_RANGE_WEAPONS = (
    "Pistol",
    "Micro Uzi",
    "Shotgun",
    "AK-47",
)

def medal_tiers(tests: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(f"{test} ({medal})" for test in tests for medal in SCHOOL_MEDALS)

class SubmissionTier(NamedTuple):
    base_slot: int
    tier_count: int
    # {tier} is the tier number, {value} the progress it needs, {name} the entry from tier_names.
    name_template: str
    value_per_tier: int
    region: str
    # Progressive Missions needed before the activity itself can be started.
    required_progressive_missions: int
    # Cumulative progress per tier, for activities whose levels are unevenly spaced.
    # Empty means the uniform value_per_tier * tier applies.
    thresholds: tuple[int, ...] = ()
    # Per-tier names, for activities whose levels are named rather than numbered (Driving School).
    # Empty means name_template is formatted instead.
    tier_names: tuple[str, ...] = ()

    # Story position that completes this activity outright, for the one submission that doubles as
    # a story mission. A start past it has already passed every tier, so they can never be checked.
    # -1 means nothing consumes it and it stays available at any starting point.
    consumed_at_story_index: int = -1

    # GTASAOptions attribute of this submission's length slider (Per Level mode), or "" for the
    option_attr: str = ""

    zero_disables: bool = False

    percentage_slider: bool = False

    on_completion_tier: int = 0

    medals_per_test: int = 0

    requires_option: str = ""

    def included_tier_count(self, options) -> int:
        slider = getattr(options, self.option_attr).value
        if self.percentage_slider:
            return slider // self.value_per_tier
        return slider

# Submissions that pay out in tiers rather than once on completion. The plugin sends
# base_slot + (tier - 1); a tier is reached at value_per_tier * tier of whatever that
# submission measures.
#
# MUST match the SubmissionTierSpec constants in the mod's EntityIDs.h exactly - same order,
# same base slots, same tier counts, same value per tier. Append new entries at the end;
# inserting in the middle renumbers every slot after it and invalidates existing seeds.
SUBMISSION_TIERS = [
    SubmissionTier(0,  12, "Paramedic Level {tier}",     1,    "Los Santos", 0, option_attr="paramedic_checks"),
    SubmissionTier(12, 12, "Firefighter Level {tier}",   1,    "Los Santos", 0, option_attr="firefighter_checks"),
    SubmissionTier(24, 12, "Vigilante Level {tier}",     1,    "Los Santos", 0, option_attr="vigilante_checks"),
    SubmissionTier(36, 50, "Taxi Driver {value} Fares",  1,    "Los Santos", 0, option_attr="taxi_checks"),
    SubmissionTier(86, 10, "Burglary ${value:,} Stolen", 1000, "Los Santos", 0, option_attr="burglary_checks", zero_disables=True),
    SubmissionTier(96, 8,  "Trucking Level {tier}",      1,    "Badlands",   33, option_attr="trucking_checks", zero_disables=True),
    SubmissionTier(104, 5, "Valet {value} Cars Parked",  0,    "San Fierro", 38,
                   thresholds=(3, 7, 12, 18, 25), option_attr="valet_checks", zero_disables=True),
    SubmissionTier(109, 36, "Driving School - {name}",   0,    "San Fierro", 39,
                   tier_names=medal_tiers(DRIVING_SCHOOL_TESTS), medals_per_test=3),
    SubmissionTier(145, 10, "Pimping Level {tier}",      1,    "Los Santos", 0, option_attr="pimping_checks", zero_disables=True),
    SubmissionTier(155, 30, "Flying School - {name}",    0,    "Las Venturas", 58,
                   tier_names=medal_tiers(FLYING_SCHOOL_LESSONS), medals_per_test=3, consumed_at_story_index=58),
    SubmissionTier(185, 15, "Boat School - {name}",      0,    "San Fierro", 54,
                   tier_names=medal_tiers(BOAT_SCHOOL_TESTS), medals_per_test=3),
    SubmissionTier(200, 18, "Bike School - {name}",      0,    "Las Venturas", 54,
                   tier_names=medal_tiers(BIKE_SCHOOL_TESTS), medals_per_test=3),
    SubmissionTier(218, 7, "Quarry Mission {tier}",      1,    "Las Venturas", 65, option_attr="quarry_checks", zero_disables=True),
    SubmissionTier(225, 20, "Gang Territory {value}% Controlled", 5, "Return to Los Santos", 78,
                   option_attr="gang_territory_target", percentage_slider=True, zero_disables=True, on_completion_tier=7),
    SubmissionTier(245, 4, "Roboi's Food Mart Courier Level {tier}", 1, "Los Santos", 0,
                   option_attr="courier_checks", zero_disables=True),
    SubmissionTier(249, 4, "Hippy Shopper Courier Level {tier}", 1, "San Fierro", 38,
                   option_attr="courier_checks", zero_disables=True),
    SubmissionTier(253, 4, "Burger Shot Courier Level {tier}", 1, "Las Venturas", 54,
                   option_attr="courier_checks", zero_disables=True),
    SubmissionTier(257, 9, "Street Race - {name}",      0,    "Los Santos", 0,
                   tier_names=RACE_GROUPS[0].names, requires_option="include_street_races"),
    SubmissionTier(266, 6, "Street Race - {name}",      0,    "San Fierro", 38,
                   tier_names=RACE_GROUPS[1].names, requires_option="include_street_races"),
    SubmissionTier(272, 10, "Street Race - {name}",     0,    "Las Venturas", 54,
                   tier_names=RACE_GROUPS[2].names, requires_option="include_street_races"),
    SubmissionTier(282, 1, "Shooting Range - {name}",   3,    "Los Santos", 25,
                   tier_names=SHOOTING_RANGE_WEAPONS[0:1], requires_option="include_shooting_range"),
    SubmissionTier(283, 1, "Shooting Range - {name}",   3,    "Los Santos", 25,
                   tier_names=SHOOTING_RANGE_WEAPONS[1:2], requires_option="include_shooting_range"),
    SubmissionTier(284, 1, "Shooting Range - {name}",   3,    "Los Santos", 25,
                   tier_names=SHOOTING_RANGE_WEAPONS[2:3], requires_option="include_shooting_range"),
    SubmissionTier(285, 1, "Shooting Range - {name}",   3,    "Los Santos", 25,
                   tier_names=SHOOTING_RANGE_WEAPONS[3:4], requires_option="include_shooting_range"),
    SubmissionTier(286, 2, "Freight Train Level {tier}",      1,    "San Fierro", 54,
                   option_attr="freight_checks", zero_disables=True),
]

SUBMISSION_TIER_SLOT_COUNT = 288

VEHICLE_LOCKED_SUBMISSIONS = {
    "Paramedic": "Paramedic Unlock",
    "Firefighter": "Firefighter Unlock",
    "Vigilante": "Vigilante Unlock",
    "Taxi Driver": "Taxi Unlock",
    "Pimping": "Pimping Unlock",
    "Burglary": "Burglary Unlock",
}

def unlock_item_for_tier(tier_spec) -> str:
    for prefix, item in VEHICLE_LOCKED_SUBMISSIONS.items():
        if tier_spec.name_template.startswith(prefix):
            return item
    return ""

def unlocked_submission_items(options) -> list[str]:
    wanted = []
    for tier_spec in SUBMISSION_TIERS:
        item = unlock_item_for_tier(tier_spec)
        if not item or item in wanted:
            continue
        if tier_spec.zero_disables and tier_spec.included_tier_count(options) == 0:
            continue
        wanted.append(item)
    return wanted

def build_tier_location_names() -> list[str]:
    """Location names in slot order, so index == the slot the plugin sends."""
    names = []
    for tier_spec in SUBMISSION_TIERS:
        prefix = REGION_ABBREVIATIONS[tier_spec.region]
        for tier in range(1, tier_spec.tier_count + 1):
            if tier_spec.thresholds:
                value = tier_spec.thresholds[tier - 1]
            else:
                value = tier * tier_spec.value_per_tier
            name = tier_spec.tier_names[tier - 1] if tier_spec.tier_names else ""
            label = tier_spec.name_template.format(tier=tier, value=value, name=name)
            names.append(f"{prefix} Mission: {label}")
    return names

SUBMISSION_TIER_LOCATION_NAMES = build_tier_location_names()

def get_tier_names(tier_spec: SubmissionTier) -> list[str]:
    """One submission's location names, in slot order."""
    start = tier_spec.base_slot
    return SUBMISSION_TIER_LOCATION_NAMES[start:start + tier_spec.tier_count]

def get_included_tier_names_by_region(options, story_mission_count: int,
                                      start_index: int = 0) -> dict[str, list[str]]:
    """Location names grouped by region, honouring Include Submissions and this seed's span.

    on_completion keeps only each submission's completion tier - reaching that one means the activity
    is done, so no extra location IDs are needed. That's the final tier for most, but the
    story-required 35% for gang territory (see on_completion_tier).
    """
    on_completion_only = options.include_submissions == "on_completion"

    grouped: dict[str, list[str]] = {}
    for tier_spec in SUBMISSION_TIERS:
        if tier_spec.requires_option and not getattr(options, tier_spec.requires_option):
            continue
        if tier_spec.zero_disables and tier_spec.included_tier_count(options) == 0:
            continue
        if tier_spec.required_progressive_missions >= story_mission_count:
            continue
        # Already finished by the save this starting point expects, so no tier can be earned.
        if 0 <= tier_spec.consumed_at_story_index < start_index:
            continue

        if tier_spec.medals_per_test and options.school_medals.value == 0:
            continue

        names = get_tier_names(tier_spec)
        if tier_spec.medals_per_test:
            names = _capped_medal_names(tier_spec, names, options, on_completion_only)
        elif on_completion_only:
            tier = tier_spec.on_completion_tier or tier_spec.tier_count
            names = names[tier - 1:tier]
        elif tier_spec.option_attr:
            names = names[:tier_spec.included_tier_count(options)]
        grouped.setdefault(tier_spec.region, []).extend(names)
    return grouped

def _capped_medal_names(tier_spec: SubmissionTier, names: list[str], options,
                        on_completion_only: bool) -> list[str]:
    cap = options.school_medals.value
    kept = [name for index, name in enumerate(names) if index % tier_spec.medals_per_test < cap]

    if on_completion_only:
        return kept[-1:]
    return kept

def get_tier_requirements() -> dict[str, int]:
    """Location name -> Progressive Missions needed to start that activity."""
    requirements = {}
    slot = 0
    for tier_spec in SUBMISSION_TIERS:
        for name in SUBMISSION_TIER_LOCATION_NAMES[slot:slot + tier_spec.tier_count]:
            requirements[name] = tier_spec.required_progressive_missions
        slot += tier_spec.tier_count
    return requirements
