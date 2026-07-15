from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle

# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
class EndGoal(Choice):
    """
    What mission you need to complete to finish your game.
    """

    display_name = "End Goal"

    option_the_green_sabre = 0

    default = option_the_green_sabre

class IncludeTags(Toggle):
    """
    Whether to include all 100 Los Santos spray tags as individual location checks.
    """

    display_name = "Include Tags"

    default = 1

@dataclass
class GTASAOptions(PerGameCommonOptions):
    end_goal: EndGoal
    death_link: DeathLink
    include_tags: IncludeTags

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [EndGoal, DeathLink, IncludeTags],
    ),
]

option_presets = {
    "Los Santos": {
        "end_goal": 0
    }
}