from typing import NamedTuple

class Branch(NamedTuple):
    name: str
    missions: tuple[int, ...]

FREE_MISSIONS = (11,)

BRANCHES = (
    Branch("Sweet", (13, 14, 15, 16, 17, 18, 19, 21, 20, 37, 38,
                     106, 107, 108, 109, 112)),
    Branch("Ryder", (12, 24, 25, 26)),
    Branch("Big Smoke", (27, 28, 29, 30)),
    Branch("OG Loc", (31, 32, 33, 34)),
    Branch("Cesar", (36, 48, 135)),
    Branch("C.R.A.S.H.", (22, 23, 39, 52, 93, 94)),
    Branch("Catalina", (41, 42, 43, 44)),
    Branch("The Truth", (46, 47)),
    Branch("Garage", (49, 51, 50)),
    Branch("Triads", (58, 60, 61, 64, 62, 63)),
    Branch("Loco Syndicate", (59, 65, 66)),
    Branch("Woozie", (53, 54, 55, 56, 57)),
    Branch("Toreno", (75, 76, 77, 78, 83, 79, 80, 81, 82)),
    Branch("Four Dragons Casino", (84, 85, 86, 88, 87, 102)),
    Branch("Caligula's Palace", (89, 90, 91, 92)),
    Branch("Madd Dogg", (95,)),
    Branch("Return", (103, 104, 105)),
)
