import unittest
import robot
import sys
from unittest.mock import patch
from io import StringIO

class TestRobot(unittest.TestCase):
    # def test_commands_exist(self):
    #     self.assertTrue(robot.robot_off_button_validation('oFf'.isupper))

    # def test_commands_exist(self):
    #     self.assertTrue(robot.robot_off_button_validation('oFf'.capitalize()))

    # @patch("sys.stdin", StringIO("Of\noff\n"))
    # def test_commands_exist(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = 'off'
    #     self.assertEqual(result,'off')

    # def test_commands_upper(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = 'OFF'
    #     self.assertEqual(result,'OFF')

    # def test_commands_camelcase(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = 'Off'
    #     self.assertEqual(result,'Off')

    # @patch("sys.stdin", StringIO("hel\nhelp\n"))
    # def test_gets_commands_exist(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = 'help'
    #     self.assertEqual(result,'help')

    # def test_validate_commands(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = ['off','help','forward 10'.split()]
    #     self.assertTrue(robot.validate_commands('off',number_steps=None),True)

    # @patch("sys.stdin", StringIO("forwar 10\nforward 10\n"))
    # def test_forward_function_validation(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = ['off','help','forward 10'.split()]
    #     self.assertTrue(robot.robot_forward_command('forward',10),True)

    # @patch("sys.stdin", StringIO("forwar 10\nforward 5\n"))
    # def test_tracking_robot_position(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     result = ['off','help','forward 5'.split()]
    #     self.assertTrue(robot.tracking_robot_position(0,5),True)
    
    # @patch("sys.stdin", StringIO("10,10\n0,10"))
    # def test_tracking_robot_position(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     self.assertTrue(robot.tracking_robot_position(0,10,'forward'),True)

    # @patch("sys.stdin", StringIO("lef,10\nleft,10"))
    # def test_robot_left_command(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     self.assertTrue(robot.robot_turn_left_command('left 10'),True)

    # @patch("sys.stdin", StringIO("10,10\n0,10"))
    # def test_limit_area(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     self.assertFalse(robot.limit_area('Forward 300'),False)

    
    # @patch("sys.stdin", StringIO("sprit,3\nsprint,4"))
    # def test_limit_area(self):
    #     output = StringIO()
    #     sys.stdout = output
    #     sys.stdout = sys.__stdout__
    #     self.assertFalse(robot.sprint('sprint',6),False)

    @patch("sys.stdin", StringIO("forward 10\nback 2"))
    def test_add_commands_history(self):
        robot.history = []
        actual_output = robot.add_commands_history('forward')
        self.assertEqual(actual_output,['forward'])

    # @patch("sys.stdin", StringIO("gdh\nforward\nreplay"))
    # def test_replay_command(self):
    #     actual_output = robot.replay('gdh','forward 10')
    #     self.assertEqual(actual_output[0],True)
    #     self.assertEqual(actual_output[1],'gdh replayed 1 commands')
