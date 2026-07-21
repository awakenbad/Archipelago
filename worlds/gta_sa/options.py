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

    default = option_the_green_sabre

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
    include_ammunation_shop: IncludeAmmunationShop
    trap_percentage: TrapPercentage

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [EndGoal, DeathLink, IncludeTags, IncludeAmmunationShop, TrapPercentage],
    ),
]

option_presets = {
    "Los Santos": {
        "end_goal": 0
    }
}