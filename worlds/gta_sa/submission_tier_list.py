from typing import NamedTuple

from .mission_list import REGION_ABBREVIATIONS

SUBMISSION_TIER_BASE_ID = 400

class SubmissionTier(NamedTuple):
    base_slot: int
    tier_count: int
    # {tier} is the tier number, {value} is tier * value_per_tier.
    name_template: str
    value_per_tier: int
    region: str
    # Progressive Missions needed before the activity itself can be started.
    required_progressive_missions: int

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
]

SUBMISSION_TIER_SLOT_COUNT = 64

def build_tier_location_names() -> list[str]:
    """Location names in slot order, so index == the slot the plugin sends."""
    names = []
    for tier_spec in SUBMISSION_TIERS:
        prefix = REGION_ABBREVIATIONS[tier_spec.region]
        for tier in range(1, tier_spec.tier_count + 1):
            label = tier_spec.name_template.format(
                tier=tier,
                value=tier * tier_spec.value_per_tier,
            )
            names.append(f"{prefix} Mission: {label}")
    return names

SUBMISSION_TIER_LOCATION_NAMES = build_tier_location_names()

def get_tier_location_names_by_region() -> dict[str, list[str]]:
    """Location names grouped by region, so out-of-scope regions can be skipped."""
    grouped: dict[str, list[str]] = {}
    slot = 0
    for tier_spec in SUBMISSION_TIERS:
        names = SUBMISSION_TIER_LOCATION_NAMES[slot:slot + tier_spec.tier_count]
        grouped.setdefault(tier_spec.region, []).extend(names)
        slot += tier_spec.tier_count
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
