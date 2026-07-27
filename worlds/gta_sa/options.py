from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle

# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
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
    end_goal: EndGoal
    death_link: DeathLink
    include_tags: IncludeTags
    include_snapshots: IncludeSnapshots
    include_ammunation_shop: IncludeAmmunationShop
    trap_percentage: TrapPercentage
    include_submissions: IncludeSubmissions

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [EndGoal, DeathLink, IncludeTags, IncludeSnapshots, IncludeAmmunationShop, TrapPercentage],
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