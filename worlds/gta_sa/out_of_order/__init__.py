from ..options import MissionOrder


def is_out_of_order(world) -> bool:
    return world.options.mission_order == MissionOrder.option_out_of_order
