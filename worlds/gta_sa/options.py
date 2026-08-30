from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle

class StartingPoint(Choice):
    """
    Where your game begins.

    Anything past Los Santos requires loading the matching save file that ships with the mod -
    the story missions before that point are dropped from the pool entirely.

    Note: This option does not affect collectibles. I.e., starting in Badlands and leaving Include
    Tags on will keep all tags in the pool.

    Must be earlier than your End Goal.
    """

    display_name = "Starting Point"

    option_los_santos = 0
    option_badlands = 1
    option_san_fierro = 2
    option_las_venturas = 3
    # No Return to Los Santos start yet - it needs a shipped save file that doesn't exist. Re-add it
    # here (value 4) and on its MILESTONES row once that save is made.

    default = option_los_santos

class EndGoal(Choice):
    """
    What mission you need to complete to finish your game.
    """

    display_name = "End Goal"

    option_the_green_sabre = 0
    option_are_you_going_to_san_fierro = 1
    option_yay_ka_boom_boom = 2
    option_a_home_in_the_hills = 3
    option_end_of_the_line = 4
    option_one_hundred_percent = 5

    default = option_the_green_sabre

class SnapshotChecks(Range):
    """
    How many of the 50 San Fierro snapshots are location checks - a random set of that size, and
    only the chosen ones show blips. 0 disables them. Ignored unless San Fierro is in scope.
    """

    display_name = "Snapshot Checks"

    range_start = 0
    range_end = 50
    default = 50

class TagChecks(Range):
    """
    How many of the 100 Los Santos spray tags are location checks - a random set of that size, and
    only the chosen ones show blips. 0 disables them.
    """

    display_name = "Tag Checks"

    range_start = 0
    range_end = 100
    default = 100

class HorseshoeChecks(Range):
    """
    How many of the 50 Las Venturas horseshoes are location checks - a random set of that size, and
    only the chosen ones show blips. 0 disables them. Ignored unless Las Venturas is in scope.
    """

    display_name = "Horseshoe Checks"

    range_start = 0
    range_end = 50
    default = 50

class IncludeAmmunationShop(Toggle):
    """
    Whether Ammu-Nation purchases are location checks. Buying an item sends the check
    instead of giving the vanilla weapon (money is still spent).
    """

    display_name = "Include Ammu-Nation Shop"

    default = 1

class ParamedicChecks(Range):
    """How many Paramedic levels send a check."""
    display_name = "Paramedic Checks"
    range_start = 1
    range_end = 12
    default = 12

class FirefighterChecks(Range):
    """How many Firefighter levels send a check."""
    display_name = "Firefighter Checks"
    range_start = 1
    range_end = 12
    default = 12

class VigilanteChecks(Range):
    """How many Vigilante levels send a check."""
    display_name = "Vigilante Checks"
    range_start = 1
    range_end = 12
    default = 12

class TaxiChecks(Range):
    """How many Taxi fare milestones send a check. Each milestone is 1 fare, so
    e.g. 3 sends checks at 1, 2 and 3 fares."""
    display_name = "Taxi Checks"
    range_start = 1
    range_end = 50
    default = 50

class BurglaryChecks(Range):
    """How many Burglary milestones send a check. Each milestone is $1000 stolen,
    so e.g. 3 sends checks at $1000, $2000 and $3000. 0 removes Burglary from the seed."""
    display_name = "Burglary Checks"
    range_start = 0
    range_end = 10
    default = 10

class TruckingChecks(Range):
    """How many Trucking levels send a check. 0 removes Trucking from the seed."""
    display_name = "Trucking Checks"
    range_start = 0
    range_end = 8
    default = 8

class ValetChecks(Range):
    """How many Valet milestones send a check. The milestones are at 3, 7, 12, 18
    and 25 cars, so e.g. 3 sends checks at 3, 7 and 12 cars. 0 removes Valet from the seed."""
    display_name = "Valet Checks"
    range_start = 0
    range_end = 5
    default = 5

class PimpingChecks(Range):
    """How many Pimping levels send a check. 0 removes Pimping from the seed."""
    display_name = "Pimping Checks"
    range_start = 0
    range_end = 10
    default = 10

class QuarryChecks(Range):
    """How many Quarry missions send a check. 0 removes the Quarry from the seed."""
    display_name = "Quarry Checks"
    range_start = 0
    range_end = 7
    default = 7

class CourierChecks(Range):
    """How many Courier levels send a check (Roboi's Food Mart, Hippy Shopper, Burger
    Shot). 0 turns courier checks off entirely."""
    display_name = "Courier Checks"
    range_start = 0
    range_end = 4
    default = 4

class FreightChecks(Range):
    """How many levels of the Brown Streak freight mission send a check. 0 turns the freight off
    entirely. Only in seeds that go past Yay Ka-Boom-Boom."""
    display_name = "Freight Checks"
    range_start = 0
    range_end = 2
    default = 2

class GangTerritoryTarget(Range):
    """Percentage of gang territory to retake in Return to Los Santos, sending a check every 5% up
    to your target (so 35 sends checks at 5, 10, ... 35%). Rounded DOWN to the nearest 5%, anything below 5 turns gang territory
    checks off entirely, same as 0. Only appears on the End of the Line goal."""
    display_name = "Gang Territory Target %"
    range_start = 0
    range_end = 100
    default = 35

class OysterChecks(Range):
    """
    How many of the 50 oysters are location checks - a random set of that size, and only the chosen
    ones show blips. 0 disables them. They are statewide and underwater, so they only appear on goals
    that open the whole map (A Home in the Hills and later).
    """

    display_name = "Oyster Checks"

    range_start = 0
    range_end = 50
    default = 50

class SchoolMedals(Choice):
    """
    Which medals will send checks to the multiworld.
    E.g. Choosing silver will generate checks for bronze and silver medals.

    Off removes all four schools - driving, flying, boat and bike - from the seed.
    """

    display_name = "School Medals"

    option_off = 0
    option_bronze = 1
    option_silver = 2
    option_gold = 3

    default = 3

class IncludeExports(Choice):
    """
    How many lists on the San Fierro export board are location checks.
    Ignored unless San Fierro is in scope.
    """

    display_name = "Include Exports"

    option_off = 0
    option_list_1 = 1
    option_lists_1_and_2 = 2
    option_lists_1_2_and_3 = 3

    default = 3

class IncludeChallenges(Toggle):
    """
    Whether challenges (BMX, NRG-500, Chilliad Races) are included as locations.
    """

    display_name = "Include Challenges"

    default = 1

class IncludeStadiumEvents(Toggle):
    """
    Whether the stadium events (8-Track, Dirt Track, Blood Ring, Kickstart) are included as
    locations. 8-Track and Dirt Track are gated behind Max Driving Skill and Max Bike Skill respectively.
    """

    display_name = "Include Stadium Events"

    default = 1

class IncludeStreetRaces(Toggle):
    """
    Whether the 25 street races are included as locations, one per race won.

    Turning this on, will add a Street Races Unlock item to the pool which upon receiving creates the blips
    at any point in the game.

    With it off, there are no race locations, no item, and the races unlock the vanilla way.
    """

    display_name = "Include Street Races"

    default = 1

class StartingUnlock(Toggle):
    """
    Whether one randomly chosen unlock item is granted at the start.

    Every side activity is gated behind its own item, this hands over one of them - a submission, the tags,
    or the street races.
    """

    display_name = "Starting Unlock"

    default = 1

class IncludeShootingRange(Toggle):
    """
    Whether the four Ammu-Nation shooting range challenges are included as locations, one per weapon
    challenge passed: Pistol, Micro Uzi, Shotgun and AK-47.
    """

    display_name = "Include Shooting Range"

    default = 1

class TrapPercentage(Range):
    """
    Percentage of filler items that are traps (flat tires, fat CJ, wanted level, car fire).
    """

    display_name = "Trap Percentage"

    range_start = 0
    range_end = 100
    default = 15

@dataclass
class GTASAOptions(PerGameCommonOptions):
    starting_point: StartingPoint
    end_goal: EndGoal
    death_link: DeathLink
    tag_checks: TagChecks
    snapshot_checks: SnapshotChecks
    horseshoe_checks: HorseshoeChecks
    oyster_checks: OysterChecks
    include_exports: IncludeExports
    include_ammunation_shop: IncludeAmmunationShop
    include_challenges: IncludeChallenges
    include_stadium_events: IncludeStadiumEvents
    include_street_races: IncludeStreetRaces
    include_shooting_range: IncludeShootingRange
    starting_unlock: StartingUnlock
    trap_percentage: TrapPercentage
    paramedic_checks: ParamedicChecks
    firefighter_checks: FirefighterChecks
    vigilante_checks: VigilanteChecks
    taxi_checks: TaxiChecks
    burglary_checks: BurglaryChecks
    trucking_checks: TruckingChecks
    valet_checks: ValetChecks
    pimping_checks: PimpingChecks
    quarry_checks: QuarryChecks
    courier_checks: CourierChecks
    freight_checks: FreightChecks
    school_medals: SchoolMedals
    gang_territory_target: GangTerritoryTarget

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [StartingPoint, EndGoal, DeathLink, TagChecks, SnapshotChecks, HorseshoeChecks, OysterChecks, SchoolMedals,
         IncludeExports, IncludeAmmunationShop, IncludeChallenges, IncludeStadiumEvents, IncludeStreetRaces,
         IncludeShootingRange, StartingUnlock, TrapPercentage],
    ),
    OptionGroup(
        "Submission Options",
        [ParamedicChecks, FirefighterChecks, VigilanteChecks, TaxiChecks, BurglaryChecks,
         TruckingChecks, ValetChecks, PimpingChecks, QuarryChecks, CourierChecks, FreightChecks,
         GangTerritoryTarget],
    ),
]

option_presets = {
    "Los Santos": {
        "end_goal": 0
    }
}