from typing import NamedTuple

from .mission_list import REGION_ABBREVIATIONS

SUBMISSION_TIER_BASE_ID = 400

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

# Submissions that pay out in tiers rather than once on completion. The plugin sends
# base_slot + (tier - 1); a tier is reached at value_per_tier * tier of whatever that
# submission measures.
#
# MUST match the SubmissionTierSpec constants in the mod's EntityIDs.h exactly - same order,
# same base slots, same tier counts, same value per tier. Append new entries at the end;
# inserting in the middle renumbers every slot after it and invalidates existing seeds.
SUBMISSION_TIERS = [
    SubmissionTier(0,  12, "Paramedic Level {tier}",     1,    "Los Santos", 1),
    SubmissionTier(12, 12, "Firefighter Level {tier}",   1,    "Los Santos", 1),
    SubmissionTier(24, 12, "Vigilante Level {tier}",     1,    "Los Santos", 1),
    SubmissionTier(36, 10, "Taxi Driver {value} Fares",  5,    "Los Santos", 1),
    SubmissionTier(46, 10, "Burglary ${value:,} Stolen", 1000, "Los Santos", 1),
    SubmissionTier(56, 8,  "Trucking Level {tier}",      1,    "Badlands",   33),
    SubmissionTier(64, 5,  "Valet {value} Cars Parked",  0,    "San Fierro", 38,
                   thresholds=(3, 7, 12, 18, 25)),
    SubmissionTier(69, 12, "Driving School - {name}",    0,    "San Fierro", 39,
                   tier_names=DRIVING_SCHOOL_TESTS),
    SubmissionTier(81, 10, "Pimping Level {tier}",       1,    "Los Santos", 1),
]

SUBMISSION_TIER_SLOT_COUNT = 91

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

def get_tier_location_names_by_region() -> dict[str, list[str]]:
    """Every submission's location names grouped by region, ignoring the options."""
    grouped: dict[str, list[str]] = {}
    for tier_spec in SUBMISSION_TIERS:
        grouped.setdefault(tier_spec.region, []).extend(get_tier_names(tier_spec))
    return grouped

def get_included_tier_names_by_region(options) -> dict[str, list[str]]:
    """As above, but honouring Include Submissions.

    on_completion keeps only each submission's final tier - reaching that one means the whole
    activity is done, so no extra location IDs are needed for it.
    """
    if options.include_submissions != "on_completion":
        return get_tier_location_names_by_region()

    grouped: dict[str, list[str]] = {}
    for tier_spec in SUBMISSION_TIERS:
        grouped.setdefault(tier_spec.region, []).extend(get_tier_names(tier_spec)[-1:])
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
