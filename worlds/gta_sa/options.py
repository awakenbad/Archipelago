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

    default = option_the_green_sabre

class IncludeSnapshots(Toggle):
    """
    Whether to include all 50 San Fierro snapshots as individual location checks.
    Ignored unless San Fierro is in scope for your goal.
    """

    display_name = "Include Snapshots"

    default = 1

class IncludeTags(Toggle):
    """
    Whether to include all 100 Los Santos spray tags as individual location checks.
    """

    display_name = "Include Tags"

    default = 1

class IncludeHorseshoes(Toggle):
    """
    Whether to include all 50 Las Venturas horseshoes as individual location checks.
    Ignored unless Las Venturas is in scope for your goal.
    """

    display_name = "Include Horseshoes"

    default = 1

class IncludeAmmunationShop(Toggle):
    """
    Whether Ammu-Nation purchases are location checks. Buying an item sends the check
    instead of giving the vanilla weapon (money is still spent).
    """

    display_name = "Include Ammu-Nation Shop"

    default = 1

class IncludeSubmissions(Choice):
    """
    How submissions send checks.

    *Per Level*: a check for every level, fare or tier of progress.
    *On Completion*: a single check for finishing the whole activity.
    """

    display_name = "Include Submissions"

    option_per_level = 0
    option_on_completion = 1

    default = option_per_level

class IncludeOysters(Toggle):
    """
    Whether to include all 50 oysters as individual location checks. They are scattered statewide
    and underwater, so they only appear on goals that open the whole map (A Home in the Hills and later).
    """

    display_name = "Include Oysters"

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
    include_tags: IncludeTags
    include_snapshots: IncludeSnapshots
    include_horseshoes: IncludeHorseshoes
    include_oysters: IncludeOysters
    include_ammunation_shop: IncludeAmmunationShop
    trap_percentage: TrapPercentage
    include_submissions: IncludeSubmissions

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [StartingPoint, EndGoal, DeathLink, IncludeTags, IncludeSnapshots, IncludeHorseshoes, IncludeOysters,
         IncludeAmmunationShop, TrapPercentage],
    ),
    OptionGroup(
        "Submission Options",
        [IncludeSubmissions],
    ),
]

option_presets = {
    "Los Santos": {
        "end_goal": 0
    }
}