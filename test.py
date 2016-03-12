import unittest  # import test library
from dynamic_object import *  # import tested module


class Unblinded_Ghost_Test(unittest.TestCase):
    """Tests for Unblinded ghosts."""

    def setUp(self):
        self.results_list = ['up', 'down', 'left', 'right']
        self.ghost_list = [UnblindedGhost(5,15),UnblindedGhost(5,0),UnblindedGhost(15,8),UnblindedGhost(0,8)]

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

    #def test_ghost_memory(self):
       # """This function tests how ghost remembers pacman movement.
        #Ghost should remember one pacman swerve after pacman disappearance.
        #"""



if __name__ == '__main__':
    unittest.main()