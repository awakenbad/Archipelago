from test.bases import WorldTestBase

from ..world import GTASAWorld


class GTASATestBase(WorldTestBase):
    game = "Grand Theft Auto: San Andreas"
    world: GTASAWorld
