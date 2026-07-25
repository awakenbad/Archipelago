SNAPSHOT_BASE_ID = 500
SNAPSHOT_COUNT = 50
SNAPSHOT_REGION = "San Fierro"

# Display numbers are 1-50, matching the C++ side's 0-indexed snapshotPositions array offset by 1.
SNAPSHOT_LOCATION_NAMES = [f"SF Snapshot: #{i + 1}" for i in range(SNAPSHOT_COUNT)]

# Snapshots only exist once the player is in San Fierro, which the region itself already enforces -
# but the photo camera is only obtainable there too, so this mirrors the region entrance rather than
# gating any individual one.
SNAPSHOT_REQUIREMENT = 36
