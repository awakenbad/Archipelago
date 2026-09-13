from .bases import GTASATestBase

CITIES = ("LS Courier: Roboi's Food Mart", "SF Courier: Hippy Shopper", "LV Courier: Burger Shot")

def courier_locations(multiworld, player):
    return sorted(
        loc.name for loc in multiworld.get_locations(player)
        if any(loc.name.startswith(city) for city in CITIES)
    )

def make_case(value):
    class Case(GTASATestBase):
        options = {
            "courier_checks": value,
            "end_goal": "end_of_the_line",
        }

        def test_location_count(self) -> None:
            names = courier_locations(self.multiworld, self.player)
            expected = value * 3
            self.assertEqual(len(names), expected)
            if names:
                for city in CITIES:
                    self.assertEqual(sum(1 for n in names if n.startswith(city)),
                                     expected // 3, f"{city} count differs from the others")
    Case.__name__ = f"TestSweep_{value}"
    return Case

for _value in range(0, 5):
    globals()[f"TestSweep_{_value}"] = make_case(_value)
