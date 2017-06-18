""" State Tests"""
import unittest
from unittest import TestCase


class TestVState(TestCase):
    def test_get_dict(self):
        import cassandra_vstate as cvs
        state = cvs.VState()
        my_dict = state.get_dict(1)
        my_dict['00:00:00:00:00:00'] = 2
        state.update_dict(1, my_dict)
        my_dict = state.get_dict(1)
        self.assertDictContainsSubset({'00:00:00:00:00:00': 2}, my_dict)

    def test_state_change_notify(self):
        """ What happens if change occurs during dictionary manipulation?"""
        import cassandra_vstate as cvs
        state1 = cvs.VState()
        # first packet in
        dict_packet_in1 = state1.get_dict(1234)
        # parallel second packet in
        dict_packet_in2 = state1.get_dict(1234)
        # changes
        dict_packet_in1['00:22'] = 1
        dict_packet_in2['00:22'] = 2
        # 2 is faster than one
        state1.update_dict(1234, dict_packet_in2)
        # 1 uses false information
        self.assertDictContainsSubset({'00:22': 2}, dict_packet_in1)


# Running Tests
if __name__ == '__main__':
    unittest.main()
