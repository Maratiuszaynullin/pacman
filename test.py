import unittest  # import test library
from dynamic_object import *  # import tested module


class UnblindedGhostTest(unittest.TestCase):
    """Tests for Unblinded ghosts."""

    def setUp(self):
        self.results_list = ['up', 'down', 'left', 'right']
        self.ghost_list = [UnblindedGhost(9, 15), UnblindedGhost(9, 0), UnblindedGhost(19, 8), UnblindedGhost(0, 8)]

    def test_ghost_ai_without_walls(self):
        """This function tests how ghost can 'see' pacman.
        When pacman and ghost on the same line, ghost should go to pacman.
        """
        m.MAP = Map('./maps/test_map_0')
        for i in range(len(self.ghost_list)):
            self.ghost = self.ghost_list[i]
            self.assertEqual(self.results_list[i], self.ghost.ghost_ai())

    def test_ghost_ai_with_walls(self):
        """This function tests ghost behavior when there is wall between pacman and ghost.
        When there is wall between pacman and ghost ghost_ai should return 'stop'.
        """
        m.MAP = Map('./maps/test_map_1')
        for i in range(len(self.ghost_list)):
            self.ghost = self.ghost_list[i]
            self.assertEqual('stop', self.ghost.ghost_ai())


if __name__ == '__main__':
    unittest.main()
