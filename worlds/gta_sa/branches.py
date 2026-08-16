from typing import NamedTuple

from .mission_list import STORY_INDEX_BY_MISSION_ID, STORY_MISSION_ORDER

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

CROSS_EDGES = {
    12: (11,),                 # Ryder <- Big Smoke
    13: (12,),                 # Tagging Up Turf <- Ryder
    27: (16,),                 # OG Loc <- Nines and AK's
    24: (17,),                 # Home Invasion <- Drive-By
    31: (27,),                 # Life's a Beach <- OG Loc
    36: (19,),                 # High Stakes <- Cesar Vialpando
    22: (32,),                 # Burning Desire <- Madd Dogg's Rhymes
    21: (22,),                 # Doberman <- Burning Desire
    37: (30, 26, 34, 36, 23),  # Reuniting <- Just Business, Robbing Uncle Sam, House Party, High Stakes, Gray Imports
    39: (38,),                 # Badlands <- The Green Sabre
    41: (39,),                 # 1st robbery <- Badlands
    42: (39, 46),              # 2nd robbery <- Badlands + Body Harvest
    135: (44,),                # Farewell, My Love <- all four robberies
    46: (39,),                 # Body Harvest <- Badlands
    48: (42,),                 # Wu Zi Mu <- 2 robberies done
    47: (135,),                # Are You Going to San Fierro? <- Farewell
    49: (47,),                 # Wear Flowers in Your Hair <- AYGTSF
    58: (50,),                 # Photo Opportunity <- Deconstruction
    59: (58,),                 # Jizzy <- Photo Opportunity
    53: (59,),                 # Mountain Cloud Boys <- Jizzy
    60: (66,),                 # Outrider <- Mike Toreno
    52: (60,),                 # Snail Trail <- Outrider
    61: (52,),                 # Ice Cold Killa <- Snail Trail
    64: (57,),                 # Pier 69 <- The Da Nang Thang
    75: (63,),                 # Monster <- Yay Ka-Boom-Boom
    84: (83,),                 # Fender Ketchup <- Learning to Fly
    89: (88,),                 # Intensive Care <- Don Peyote
    93: (89,),                 # Misappropriation <- Intensive Care
    87: (90,),                 # Fish in a Barrel <- The Meat Business
    95: (90,),                 # Madd Dogg <- The Meat Business
    94: (91,),                 # High Noon <- Freefall
    92: (82, 87, 94, 95),      # Saint Mark's Bistro <- every other LV
    102: (92,),                # A Home in the Hills <- Saint Mark's Bistro
    103: (102,),               # Vertical Bird <- A Home in the Hills
    106: (104,),               # Beat Down on B Dup <- Home Coming
    108: (105,),               # Riot <- Cut Throat Business
}

SET_COUNT_EDGES: dict[int, tuple[int, tuple[int, ...]]] = {}

_BRANCH_BY_NAME = {branch.name: branch for branch in BRANCHES}

def branch_of(mission_id: int) -> str | None:
    for branch in BRANCHES:
        if mission_id in branch.missions:
            return branch.name
    return None

def branch_position(mission_id: int) -> int | None:
    branch = branch_of(mission_id)
    if branch is None:
        return None
    return _BRANCH_BY_NAME[branch].missions.index(mission_id) + 1

def _merge(into: dict[str, int], other: dict[str, int]) -> None:
    for name, value in other.items():
        into[name] = max(into.get(name, 0), value)

_REQUIREMENT_MEMO: dict[int, dict[str, int]] = {}

def mission_requirement(mission_id: int) -> dict[str, int]:
    if mission_id in _REQUIREMENT_MEMO:
        return dict(_REQUIREMENT_MEMO[mission_id])

    branch = branch_of(mission_id)
    if branch is None:
        _REQUIREMENT_MEMO[mission_id] = {}
        return {}

    branch_missions = _BRANCH_BY_NAME[branch].missions
    position = branch_missions.index(mission_id) + 1

    req: dict[str, int] = {branch: position}

    if position > 1:
        _merge(req, mission_requirement(branch_missions[position - 2]))

    for prereq in CROSS_EDGES.get(mission_id, ()):
        _merge(req, mission_requirement(prereq))

    if mission_id in SET_COUNT_EDGES:
        count, members = SET_COUNT_EDGES[mission_id]
        member_branch = branch_of(members[0])
        req[member_branch] = max(req.get(member_branch, 0), count)
        for name, value in mission_requirement(members[0]).items():
            if name != member_branch:
                req[name] = max(req.get(name, 0), value)

    _REQUIREMENT_MEMO[mission_id] = dict(req)
    return dict(req)

def branch_precompleted(start_index: int) -> dict[str, int]:
    return {
        branch.name: sum(1 for m in branch.missions if STORY_INDEX_BY_MISSION_ID[m] < start_index)
        for branch in BRANCHES
    }

def branch_pool_counts(start_index: int, goal_index: int) -> dict[str, int]:
    return {
        branch.name: sum(1 for m in branch.missions
                         if start_index <= STORY_INDEX_BY_MISSION_ID[m] < goal_index)
        for branch in BRANCHES
    }

def effective_requirement(mission_id: int, start_index: int) -> dict[str, int]:
    precompleted = branch_precompleted(start_index)
    effective: dict[str, int] = {}
    for name, count in mission_requirement(mission_id).items():
        remaining = count - precompleted.get(name, 0)
        if remaining > 0:
            effective[name] = remaining
    return effective

def validate() -> None:
    story = set(STORY_MISSION_ORDER)

    seen: dict[int, str] = {}
    for branch in BRANCHES:
        for mission_id in branch.missions:
            assert mission_id in story, f"{branch.name}: {mission_id} is not a story mission"
            assert mission_id not in seen, f"{mission_id} is in both {seen[mission_id]} and {branch.name}"
            seen[mission_id] = branch.name
    for mission_id in FREE_MISSIONS:
        assert mission_id in story, f"free mission {mission_id} is not a story mission"
        assert mission_id not in seen, f"{mission_id} is both free and in {seen[mission_id]}"
        seen[mission_id] = "FREE"

    missing = story - set(seen)
    assert not missing, f"story missions in no branch: {sorted(missing)}"

    for mission_id, prereqs in CROSS_EDGES.items():
        assert mission_id in story, f"cross-edge keyed on non-mission {mission_id}"
        for prereq in prereqs:
            assert prereq in story, f"cross-edge {mission_id} <- {prereq}: {prereq} is not a mission"
    for mission_id, (count, members) in SET_COUNT_EDGES.items():
        assert mission_id in story, f"set-count edge keyed on non-mission {mission_id}"
        assert 1 <= count <= len(members), f"set-count edge {mission_id}: bad count {count}"
        for member in members:
            assert member in story, f"set-count edge {mission_id}: {member} is not a mission"

if __name__ == "__main__":
    validate()
    print(f"OK: {len(BRANCHES)} branches + {len(FREE_MISSIONS)} free mission(s) cover all "
          f"{len(set(STORY_MISSION_ORDER))} story missions.")
