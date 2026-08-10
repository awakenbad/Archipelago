import unittest

from ..branches import (
    BRANCHES,
    CROSS_EDGES,
    FREE_MISSIONS,
    branch_of,
    branch_position,
    mission_requirement,
    validate,
)

class TestBranchData(unittest.TestCase):
    def test_partition_is_valid(self) -> None:
        validate()

    def test_branch_of(self) -> None:
        self.assertEqual(branch_of(13), "Sweet")
        self.assertEqual(branch_of(93), "C.R.A.S.H.")
        self.assertIsNone(branch_of(FREE_MISSIONS[0]))

    def test_branch_names_are_unique(self) -> None:
        names = [branch.name for branch in BRANCHES]
        self.assertEqual(len(names), len(set(names)))

    def test_free_mission_needs_nothing(self) -> None:
        self.assertEqual(mission_requirement(FREE_MISSIONS[0]), {})

    def test_requirement_includes_own_branch_position(self) -> None:
        for branch in BRANCHES:
            for mission_id in branch.missions:
                with self.subTest(f"{branch.name}:{mission_id}"):
                    self.assertEqual(mission_requirement(mission_id).get(branch.name),
                                     branch_position(mission_id))

    def test_requirement_is_monotonic_along_a_branch(self) -> None:
        for branch in BRANCHES:
            prev: dict = {}
            for mission_id in branch.missions:
                req = mission_requirement(mission_id)
                for name, value in prev.items():
                    with self.subTest(f"{branch.name}:{mission_id} vs prev {name}"):
                        self.assertGreaterEqual(req.get(name, 0), value)
                prev = req

    def test_end_of_the_line_requires_every_branch(self) -> None:
        req = mission_requirement(112)
        self.assertEqual(set(req), {branch.name for branch in BRANCHES})

    def test_cross_edges_do_not_point_within_the_same_branch(self) -> None:
        for mission_id, prereqs in CROSS_EDGES.items():
            branch = branch_of(mission_id)
            for prereq in prereqs:
                with self.subTest(f"{mission_id} <- {prereq}"):
                    self.assertNotEqual(branch, branch_of(prereq),
                                        f"{mission_id} <- {prereq} is within branch {branch}")
