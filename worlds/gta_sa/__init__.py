from worlds.LauncherComponents import Component, Type, components, icon_paths, launch as launch_component

from .world import GTASAWorld


def launch_client(*args):
    from .client import launch
    launch_component(launch, name="GTASAClient", args=args)


# ap: resolves the path inside the apworld, so it works from a zipped .apworld too.
icon_paths["gta_sa"] = f"ap:{__name__}/icon.png"

components.append(
    Component("GTA SA Client", func=launch_client, component_type=Type.CLIENT, icon="gta_sa")
)
