from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import GTASAWorld

def set_all_rules(world: GTASAWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: GTASAWorld) -> None:
    los_santos_to_badlands = world.get_entrance("Los Santos to Badlands")
    badlands_to_san_fierro = world.get_entrance("Badlands to San Fierro")
    san_fierro_to_las_venturas = world.get_entrance("San Fierro to Las Venturas")

    world.set_rule(los_santos_to_badlands, Has("Progressive Map", 1))
    world.set_rule(badlands_to_san_fierro, Has("Progressive Map", 2))
    world.set_rule(san_fierro_to_las_venturas, Has("Progressive Map", 3))

def set_all_location_rules(world: GTASAWorld) -> None:
    pass

def set_completion_condition(world: GTASAWorld) -> None:
    pass