from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
class EndGoal(Choice):
    """
    What mission you need to complete to finish your game.
    """

    display_name = "End Goal"

    option_the_green_sabre = 0

    default = option_the_green_sabre

@dataclass
class GTASAOptions(PerGameCommonOptions):
    end_goal: EndGoal

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [EndGoal],
    ),
]

option_presets = {
    "Los Santos": {
        "end_goal": 0
    }
}