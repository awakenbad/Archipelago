SCHOOLS_CALL = (47, 50)
ZERO_CALL = (47, 49)

TIER_TRIGGERS = {
    96: (44,),          # Trucking: Tanker Commander
    109: SCHOOLS_CALL,  # Driving School
    185: SCHOOLS_CALL,  # Boat School
    200: SCHOOLS_CALL,  # Bike School
    282: (21,),         # Shooting Range (Pistol): Doberman
    283: (21,),         # Shooting Range (Micro Uzi)
}

OPTIONAL_TRIGGERS = {
    71: SCHOOLS_CALL,   # Back to School
    72: ZERO_CALL,      # Air Raid, after Zero
    73: ZERO_CALL,
    74: ZERO_CALL,
}

WANG_CARS_TRIGGERS = {mission_id: SCHOOLS_CALL for mission_id in (67, 68, 69, 70)}

EXPORT_TRIGGER = SCHOOLS_CALL
