SUBMISSION_TIER_BASE_ID = 400
SUBMISSION_TIER_REGION = "Los Santos"

# Submissions that pay out in tiers rather than once on completion. The plugin sends
# base_slot + (tier - 1); a tier is reached at value_per_tier * tier of whatever that
# submission measures.
#
# MUST match the SubmissionTierSpec constants in the mod's EntityIDs.h exactly - same order,
# same base slots, same tier counts, same value per tier. Append new entries at the end;
# inserting in the middle renumbers every slot after it and invalidates existing seeds.
#
# In name_template, {tier} is the tier number and {value} is tier * value_per_tier.
SUBMISSION_TIERS = [
    # (base_slot, tier_count, name_template, value_per_tier)
    (0,  12, "Paramedic Level {tier}",     1),
    (12, 12, "Firefighter Level {tier}",   1),
    (24, 12, "Vigilante Level {tier}",     1),
    (36, 10, "Taxi Driver {value} Fares",  5),
    (46, 10, "Burglary ${value:,} Stolen", 1000),
]

SUBMISSION_TIER_SLOT_COUNT = 56

def build_tier_location_names() -> list[str]:
    """Location names in slot order, so index == the slot the plugin sends."""
    names = []
    for base_slot, tier_count, name_template, value_per_tier in SUBMISSION_TIERS:
        for tier in range(1, tier_count + 1):
            label = name_template.format(tier=tier, value=tier * value_per_tier)
            names.append(f"LS Mission: {label}")
    return names

SUBMISSION_TIER_LOCATION_NAMES = build_tier_location_names()
