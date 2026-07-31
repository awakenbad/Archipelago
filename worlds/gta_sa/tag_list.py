TAG_BASE_ID = 200
TAG_COUNT = 100
TAG_REGION = "Los Santos"

# Display numbers are 1-100, matching the C++ side's 0-indexed tagPositions array offset by 1.
TAG_LOCATION_NAMES = [f"LS Tag: #{i + 1}" for i in range(TAG_COUNT)]

# Tagging Up Turf sprays these six as part of the mission itself, so a save that starts past that
# point has already moved the counter with no checks sent - they can never be earned.
MISSION_SPRAYED_TAGS = (1, 2, 3, 26, 27, 28)

# Story position of Tagging Up Turf. A starting point beyond it has consumed the six above.
MISSION_SPRAYED_TAGS_STORY_INDEX = 2

def get_earnable_tag_names(start_index: int) -> list[str]:
    if start_index <= MISSION_SPRAYED_TAGS_STORY_INDEX:
        return TAG_LOCATION_NAMES
    sprayed = {TAG_LOCATION_NAMES[number - 1] for number in MISSION_SPRAYED_TAGS}
    return [name for name in TAG_LOCATION_NAMES if name not in sprayed]
