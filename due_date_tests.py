from unittest.mock import patch
import unittest
import due_date_calculator as calc

# aznap kész
# 8-nál kevesebb óra, de átlóg másnapra
# másnap ugyanakkor kész
# pár napra rá kész
# átlóg a hétvégén
# átlóg másik hónapra
# átlóg másik évbe
# pár óra, de átforgatja az évet is akár (century?)
#
#


class TestBadDates(unittest.TestCase):

    def test_bad_date_random(self):
        with self.assertRaises(calc.CustomError):
            calc.validate_input("XXXX")

    def test_bad_date_non_existent(self):
        with self.assertRaises(calc.CustomError):
            calc.validate_input("2022.02.29. 13:00")

    @patch('due_date_calculator.get_input_date', return_value='2022.01.29. 13:00')
    def test_bad_date_weekend(self, input):
        with self.assertRaises(calc.CustomError):
            calc.read_date()

    def test_bad_date_weekday_out_of_worktime(self):
        with self.assertRaises(calc.CustomError):
            calc.validate_input("2022.01.27. 17:01")


class TestBadTurnarounds(unittest.TestCase):

    @patch('due_date_calculator.get_input_turnaround', return_value='XXXX')
    def test_bad_turnaround_random(self, input):
        with self.assertRaises(ValueError):
            calc.read_turnaround()

    @patch('due_date_calculator.get_input_turnaround', return_value='10.2')
    def test_bad_turnaround_not_integer(self, input):
        with self.assertRaises(ValueError):
            calc.read_turnaround()

    @patch('due_date_calculator.get_input_turnaround', return_value='-1')
    def test_bad_turnaround_negative(self, input):
        with self.assertRaises(calc.CustomError):
            calc.read_turnaround()


class TestNormalCases(unittest.TestCase):

    @patch('due_date_calculator.get_input_turnaround', return_value='2')
    @patch('due_date_calculator.get_input_date', return_value='2022.01.27 12:00')
    def test_same_day_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.27 Thursday 14:00')


if __name__ == '__main__':
    unittest.main()


# def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
