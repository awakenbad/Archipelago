from BaseClasses import ItemClassification

from .bases import GTASATestBase

REGULAR_TRAPS = {"Flat Tires Trap", "Fat CJ Trap", "Wanted Level Trap", "Car Fire Trap", "Bad Weather Trap"}
DRAWS = 300

class ChaosTrapAssertions:
    expected_traps: set[str] = REGULAR_TRAPS

    def test_filler_draws_only_the_expected_traps(self) -> None:
        drawn = {self.world.get_filler_item_name() for _ in range(DRAWS)}
        self.assertEqual(drawn, self.expected_traps)

    def test_item_pool_traps_are_the_expected_traps(self) -> None:
        pool_traps = {
            item.name for item in self.multiworld.itempool
            if item.player == self.player and item.classification & ItemClassification.trap
        }
        self.assertTrue(pool_traps, "no traps in the pool")
        self.assertLessEqual(pool_traps, self.expected_traps)

class TestChaosModTrapsOff(ChaosTrapAssertions, GTASATestBase):
    options = {"starting_unlock": False, "trap_percentage": 100, "chaos_mod_traps": "off"}

class TestChaosModTrapsLow(ChaosTrapAssertions, GTASATestBase):
    options = {"starting_unlock": False, "trap_percentage": 100, "chaos_mod_traps": "low"}
    expected_traps = {"Low Chaos Trap"}

class TestChaosModTrapsMedium(ChaosTrapAssertions, GTASATestBase):
    options = {"starting_unlock": False, "trap_percentage": 100, "chaos_mod_traps": "medium"}
    expected_traps = {"Low Chaos Trap", "Medium Chaos Trap"}

class TestChaosModTrapsHigh(ChaosTrapAssertions, GTASATestBase):
    options = {"starting_unlock": False, "trap_percentage": 100, "chaos_mod_traps": "high"}
    expected_traps = {"Low Chaos Trap", "Medium Chaos Trap", "High Chaos Trap"}
