from ryu.app import simple_switch_13


class SimpleSwitch13VState(simple_switch_13):
    """
    This Class implements a simple learning switch, which stores its dictionaries
    inside a virtual state data base.
    """

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13VState, self).__init__(*args, **kwargs)
