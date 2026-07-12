from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import GTASAWorld

def create_and_connect_regions(world: GTASAWorld) -> None:
    create_all_regions(world)
    connect_regions(world)
def create_all_regions(world: GTASAWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    los_santos = Region("Los Santos", world.player, world.multiworld)
    san_fierro = Region("San Fierro", world.player, world.multiworld)
    las_venturas = Region("Las Venturas", world.player, world.multiworld)
    badlands = Region("Badlands", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [los_santos, san_fierro, las_venturas, badlands]

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions

def connect_regions(world: GTASAWorld) -> None:
    los_santos = world.get_region("Los Santos")
    san_fierro = world.get_region("San Fierro")
    las_venturas = world.get_region("Las Venturas")
    badlands = world.get_region("Badlands")

    los_santos_to_badlands = Entrance(world.player, "Los Santos to Badlands", parent=los_santos)
    los_santos.exits.append(los_santos_to_badlands)
    los_santos_to_badlands.connect(badlands)

    badlands_to_san_fierro = Entrance(world.player, "Badlands to San Fierro", parent=badlands)
    badlands.exits.append(badlands_to_san_fierro)
    badlands_to_san_fierro.connect(san_fierro)

    san_fierro_to_las_venturas = Entrance(world.player, "San Fierro to Las Venturas", parent=san_fierro)
    san_fierro.exits.append(san_fierro_to_las_venturas)
    san_fierro_to_las_venturas.connect(las_venturas)

    las_venturas_to_los_santos = Entrance(world.player, "Las Venturas to Los Santos", parent=las_venturas)
    las_venturas.exits.append(las_venturas_to_los_santos)
    las_venturas_to_los_santos.connect(los_santos)

    # An even easier way is to use the region.connect helper.
    #overworld.connect(right_room, "Overworld to Right Room")
    #right_room.connect(final_boss_room, "Right Room to Final Boss Room")