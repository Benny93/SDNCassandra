import unittest
from unittest import TestCase


class TestVState(TestCase):
    def test_get_dict(self):
        import cassandra_vstate as vs
        state = vs.VState()
        my_dict = state.get_dict(1)
        my_dict['00:00:00:00:00:00'] = 2
        state.update_dict(1, my_dict)
        my_dict = state.get_dict(1)
        self.assertDictContainsSubset({'00:00:00:00:00:00': 2}, my_dict)


# Running Tests
if __name__ == '__main__':
    unittest.main()
