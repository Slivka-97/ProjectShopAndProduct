from django.test import TestCase

from store.logic import operation


class TestLog(TestCase):
    def test_plus(self):
        res = operation(1, 2, '+')
        self.assertEqual(3, res)

    def test_minus(self):
        res = operation(5, 2, '-')
        self.assertEqual(3, res)
