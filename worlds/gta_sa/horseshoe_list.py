HORSESHOE_BASE_ID = 600
HORSESHOE_COUNT = 50
HORSESHOE_REGION = "Las Venturas"

# Display numbers are 1-50, matching the C++ side's 0-indexed horseshoePositions array offset by 1.
HORSESHOE_LOCATION_NAMES = [f"LV Horseshoe: #{i + 1}" for i in range(HORSESHOE_COUNT)]

# Horseshoes sit in and around Las Venturas, which the region entrance already gates - this mirrors
# it rather than gating any individual one.
HORSESHOE_REQUIREMENT = 54
