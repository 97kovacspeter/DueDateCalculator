from unittest.mock import patch
import unittest
import due_date_calculator as calc


class TestBadDates(unittest.TestCase):

    def test_bad_date_random(self):
        with self.assertRaises(calc.CustomError) as CE:
            calc.validate_input("XXXX")
        the_exception = CE.exception
        self.assertEqual(the_exception.msg, "Invalid date exception")

    def test_bad_date_non_existent(self):
        with self.assertRaises(calc.CustomError) as CE:
            calc.validate_input("2022.02.29. 13:00")
        the_exception = CE.exception
        self.assertEqual(the_exception.msg, "Invalid date exception")

    @patch('due_date_calculator.get_input_date', return_value='2022.01.29. 13:00')
    def test_bad_date_weekend(self, input):
        with self.assertRaises(calc.CustomError) as CE:
            calc.read_date()
        the_exception = CE.exception
        self.assertEqual(the_exception.msg, "Weekend exception")

    def test_bad_date_weekday_out_of_worktime(self):
        with self.assertRaises(calc.CustomError) as CE:
            calc.validate_input("2022.01.27. 17:01")
        the_exception = CE.exception
        self.assertEqual(the_exception.msg, "Invalid date exception")


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
        with self.assertRaises(calc.CustomError) as CE:
            calc.read_turnaround()
        the_exception = CE.exception
        self.assertEqual(the_exception.msg, "Negative turnaround exception")


class TestNormalCases(unittest.TestCase):

    @patch('due_date_calculator.get_input_date', return_value='2022.01.27 12:01')
    @patch('due_date_calculator.get_input_turnaround', return_value='2')
    def test_same_day_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.27 Thursday 14:01')

    @patch('due_date_calculator.get_input_date', return_value='2022.01.27 12:02')
    @patch('due_date_calculator.get_input_turnaround', return_value='7')
    def test_next_day_delivery_with_low_hours(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.28 Friday 11:02')

    @patch('due_date_calculator.get_input_date', return_value='2022.01.27 12:03')
    @patch('due_date_calculator.get_input_turnaround', return_value='8')
    def test_next_day_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.28 Friday 12:03')

    @patch('due_date_calculator.get_input_date', return_value='2022.01.25 12:04')
    @patch('due_date_calculator.get_input_turnaround', return_value='16')
    def test_few_days_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.27 Thursday 12:04')

    @patch('due_date_calculator.get_input_date', return_value='2022.01.25 12:05')
    @patch('due_date_calculator.get_input_turnaround', return_value='18')
    def test_few_days_and_hours_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.27 Thursday 14:05')


class TestEdgeCases(unittest.TestCase):

    @patch('due_date_calculator.get_input_date', return_value='2022.01.27 12:06')
    @patch('due_date_calculator.get_input_turnaround', return_value='16')
    def test_next_week_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.31 Monday 12:06')

    @patch('due_date_calculator.get_input_date', return_value='2022.01.27 12:07')
    @patch('due_date_calculator.get_input_turnaround', return_value='24')
    def test_next_month_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.02.01 Tuesday 12:07')

    @patch('due_date_calculator.get_input_date', return_value='2021.12.31 12:08')
    @patch('due_date_calculator.get_input_turnaround', return_value='8')
    def test_next_year_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.03 Monday 12:08')

    @patch('due_date_calculator.get_input_date', return_value='2021.12.27 12:09')
    @patch('due_date_calculator.get_input_turnaround', return_value='48')
    def test_next_year_and_a_day_delivery(self, input, input2):
        self.assertEqual(calc.main(), '2022.01.04 Tuesday 12:09')


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
