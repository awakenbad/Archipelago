EXPORT_BASE_ID = 700
EXPORT_REGION = "San Fierro"

# The Easter Basin export board, in board order: three lists of ten. Order must match
# exportVehicleModels in the mod's ExportVehicles.h exactly - index is the location index.
EXPORT_VEHICLES = (
    # List 1
    "Patriot", "Sanchez", "Stretch", "Feltzer", "Remington",
    "Buffalo", "Sentinel", "Infernus", "Camper", "Admiral",
    # List 2
    "Slamvan", "Blista Compact", "Stafford", "Sabre", "FCR-900",
    "Cheetah", "Rancher", "Stallion", "Tanker", "Comet",
    # List 3
    "Blade", "Freeway", "Mesa", "ZR-350", "Euros",
    "Banshee", "Super GT", "Journey", "Huntley", "BF Injection",
)

EXPORT_COUNT = len(EXPORT_VEHICLES)

EXPORT_LOCATION_NAMES = [f"SF Export: {name}" for name in EXPORT_VEHICLES]

# The docks open after Yay Ka-Boom-Boom (story position 53).
EXPORT_REQUIREMENT = 54
