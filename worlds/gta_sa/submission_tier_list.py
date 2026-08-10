from typing import NamedTuple

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

    percentage_slider: bool = False

    on_completion_tier: int = 0

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
    SubmissionTier(86, 10, "Burglary ${value:,} Stolen", 1000, "Los Santos", 0, option_attr="burglary_checks"),
    SubmissionTier(96, 8,  "Trucking Level {tier}",      1,    "Badlands",   33, option_attr="trucking_checks"),
    SubmissionTier(104, 5, "Valet {value} Cars Parked",  0,    "San Fierro", 38,
                   thresholds=(3, 7, 12, 18, 25), option_attr="valet_checks"),
    SubmissionTier(109, 12, "Driving School - {name}",   0,    "San Fierro", 39,
                   tier_names=DRIVING_SCHOOL_TESTS),
    SubmissionTier(121, 10, "Pimping Level {tier}",      1,    "Los Santos", 0, option_attr="pimping_checks"),
    # Learning to Fly (story position 58) is Flying School - passing the mission passes every lesson.
    SubmissionTier(131, 10, "Flying School - {name}",    0,    "Las Venturas", 58,
                   tier_names=FLYING_SCHOOL_LESSONS, consumed_at_story_index=58),
    SubmissionTier(141, 5, "Boat School - {name}",       0,    "San Fierro", 54,
                   tier_names=BOAT_SCHOOL_TESTS),
    SubmissionTier(146, 6, "Bike School - {name}",       0,    "Las Venturas", 54,
                   tier_names=BIKE_SCHOOL_TESTS),
    SubmissionTier(152, 7, "Quarry Mission {tier}",      1,    "Las Venturas", 65, option_attr="quarry_checks"),
    SubmissionTier(159, 20, "Gang Territory {value}% Controlled", 5, "Return to Los Santos", 78,
                   option_attr="gang_territory_target", percentage_slider=True, on_completion_tier=7),
]

SUBMISSION_TIER_SLOT_COUNT = 179

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
        if tier_spec.required_progressive_missions >= story_mission_count:
            continue
        # Already finished by the save this starting point expects, so no tier can be earned.
        if 0 <= tier_spec.consumed_at_story_index < start_index:
            continue

        names = get_tier_names(tier_spec)
        if on_completion_only:
            tier = tier_spec.on_completion_tier or tier_spec.tier_count
            names = names[tier - 1:tier]
        elif tier_spec.option_attr:
            names = names[:tier_spec.included_tier_count(options)]
        grouped.setdefault(tier_spec.region, []).extend(names)
    return grouped

def get_tier_requirements() -> dict[str, int]:
    """Location name -> Progressive Missions needed to start that activity."""
    requirements = {}
    slot = 0
    for tier_spec in SUBMISSION_TIERS:
        for name in SUBMISSION_TIER_LOCATION_NAMES[slot:slot + tier_spec.tier_count]:
            requirements[name] = tier_spec.required_progressive_missions
        slot += tier_spec.tier_count
    return requirements
