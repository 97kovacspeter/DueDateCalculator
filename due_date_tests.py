import unittest

# rossz dátum, zagyva
# rossz dátum, nem létező
# rossz dátum, munkaidőn kívül
# jó dátum, rossz turnaround, zagyva
# jó dátum, rossz turnaround, nem int
# jó dátum, rossz turnaround, negatív
# aznap kész
# másnap ugyanakkor kész
# pár napra rá kész
# 8-nál kevesebb óra, de átlóg másnapra
#
#
#
#


class TestDueDateMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
