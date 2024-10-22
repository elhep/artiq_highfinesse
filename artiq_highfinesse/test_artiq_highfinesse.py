import sys

from sipyco.test.generic_rpc import GenericRPCCase


class GenericHighfinesseTest:
    def test_set_channel_frequency(self):
        """
        Test setting and getting the frequency for a specific channel.
        """
        frequency = 5e6
        channel = 5
        self.artiq_highfinesse.set_channel_frequency(channel, frequency)
        self.assertEqual(
            frequency, self.artiq_highfinesse.get_channel_frequency(channel)
        )

    def test_set_autocalibration_on(self):
        """
        Test setting and getting the autocalibration mode.
        """
        self.artiq_highfinesse.set_autocalibration_on(True)
        self.assertTrue(self.artiq_highfinesse.get_autocalibration_on())

        self.artiq_highfinesse.set_autocalibration_on(False)
        self.assertFalse(self.artiq_highfinesse.get_autocalibration_on())

    def test_set_channel_exposure(self):
        """
        Test setting and getting the exposure for a specific channel.
        """
        exposure = 50
        channel = 3
        self.artiq_highfinesse.set_channel_exposure(channel, exposure)
        self.assertEqual(exposure, self.artiq_highfinesse.get_channel_exposure(channel))

    def test_set_switch_mode_on(self):
        """
        Test enabling and disabling the switch mode.
        """
        self.artiq_highfinesse.set_switch_mode_on(True)
        self.assertTrue(self.artiq_highfinesse.get_switch_mode_on())

        self.artiq_highfinesse.set_switch_mode_on(False)
        self.assertFalse(self.artiq_highfinesse.get_switch_mode_on())


class TestHighfinesseSim(GenericRPCCase, GenericHighfinesseTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m artiq_highfinesse.aqctl_artiq_highfinesse"
            + " -p 3284 --simulation"
        )
        self.artiq_highfinesse = self.start_server("artiq_highfinesse", command, 3284)
