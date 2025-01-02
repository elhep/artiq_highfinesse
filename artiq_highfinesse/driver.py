#!/usr/bin/env python3

import asyncio
import logging
import sys

from . import wlmConst, wlmData


class ArtiqHighfinesse:
    """
    This class interfaces with the Highfinesse wavelength meter.
    It provides methods to interact with the device, such as setting/getting channel
    frequency, autocalibration, exposure, and switch mode.
    """

    def __init__(self):
        try:
            wlmData.LoadDLL("/usr/lib/libwlmData.so")
        except Exception as e:
            sys.exit(f"Could not load the library and establish connection, {e}")

    async def set_defaults(self):
        """
        Set default parameters for the device, including result mode, autocalibration
        mode, and autocalibration settings. If setting any of these parameters fails,
        logs an error.
        """
        ret = wlmData.dll.SetResultMode(wlmConst.cReturnFrequency)
        if ret:
            logging.error(f"Setting result mode did not succeed, error code: {ret}")
        ret = wlmData.dll.SetAutoCalMode(1)
        if ret:
            logging.error(f"Setting autocalibration did not succeed, error code: {ret}")
        ret = wlmData.dll.SetAutoCalSetting(wlmConst.cmiAutoCalPeriod, 2, 0, 0)
        if ret:
            logging.error(
                f"Setting autocalibration period did not succeed, error code:" f"{ret}"
            )
        ret = wlmData.dll.SetAutoCalSetting(
            wlmConst.cmiAutoCalUnit, wlmConst.cACMinutes, 0, 0
        )
        if ret:
            logging.error(
                f"Setting autocalibration units did not succeed, error code:" f"{ret}"
            )

    async def ping(self):
        if wlmData.dll.GetWLMCount(0) == 0:
            return False
        else:
            return True

    async def set_autocalibration_on(self, autocalibration_on):
        """
        Enable or disable autocalibration on the device.
        """
        ret = wlmData.dll.SetAutoCalMode(1 if autocalibration_on else 0)
        if ret:
            logging.error(
                f"Changing autocalibration mode did not succeed, error code: {ret}"
            )

    async def get_autocalibration_on(self):
        """
        Get the current autocalibration mode of the device.
        """
        ret = wlmData.dll.GetAutoCalMode(0)
        if ret:
            logging.info("Autocalibration on")
        else:
            logging.info("Autocalibration off")
        return ret

    async def get_channel_frequency(self, channel):
        """
        Get the frequency reading of a specific channel.
        """
        ret = wlmData.dll.GetFrequencyNum(channel, 0)
        if ret <= 0:
            logging.error(f"Frequency readout did not succeed, error code: {ret}")
        else:
            logging.info(f"Frequency value: {ret}")
            return ret

    async def get_channel_exposure(self, channel):
        """
        Get the exposure value of a specific channel.
        """
        ret = wlmData.dll.GetExposureNum(channel, 1, 0)
        if ret <= 0:
            logging.error(f"Exposure readout did not succeed, error code: {ret}")
        else:
            logging.info(f"Exposure value: {ret}")
            return ret

    async def set_channel_exposure(self, channel, exposure):
        """
        Set the exposure value for a specific channel.
        """
        ret = wlmData.dll.SetExposureNum(channel, 1, exposure)
        if ret < 0:
            logging.error(f"Setting exposure did not succeed, error code: {ret}")

    async def set_measurement_on(self, measurement_on):
        """
        Start or stop measurement on the device.
        """
        ret = wlmData.dll.Operation(
            wlmConst.cCtrlStartMeasurement if measurement_on else wlmConst.cStop
        )
        if ret:
            logging.error(
                f"Changing measurement state did not succeed, error code: {ret}"
            )

    async def set_switch_mode_on(self, switch_mode_on):
        """
        Enable or disable the switch mode on the device.
        """
        ret = wlmData.dll.SetSwitcherMode(1 if switch_mode_on else 0)
        if ret:
            logging.error(f"Changing switch mode did not succeed, error code: {ret}")

    async def get_switch_mode_on(self):
        """
        Get the current state of switch mode on the device.
        """
        ret = wlmData.dll.GetSwitcherMode(0)
        if ret:
            logging.info("Switch mode on")
        else:
            logging.info("Switch mode off")
        return ret


class ArtiqHighfinesseSim:
    def __init__(self):
        self.channel_frequency = 8 * [None]
        self.channel_exposure = 8 * [None]
        self.autocalibration_on = False
        self.measurement_on = False
        self.switch_mode_on = False

    def convert_channel(self, channel):
        if not (1 <= channel <= 8):
            raise ValueError("Channel out of range")
        conv_channel = channel - 1
        return conv_channel

    async def ping(self):
        return True

    async def get_channel_frequency(self, channel):
        """
        Simulate reading frequency from a channel.
        """
        logging.warning(
            f"Simulated: Channel frequency readout: "
            f"{self.channel_frequency[self.convert_channel(channel)]}"
        )
        return self.channel_frequency[self.convert_channel(channel)]

    async def set_channel_frequency(self, channel, frequency):
        """
        Simulate setting frequency for a channel.
        """
        logging.warning(
            f"Simulated: Setting channel {channel} frequency to {frequency}"
        )
        self.channel_frequency[self.convert_channel(channel)] = frequency

    async def get_autocalibration_on(self):
        """
        Simulate getting the autocalibration state.
        """
        logging.warning(
            f"Simulated: Autocalibration is "
            f"{'on' if self.autocalibration_on else 'off'}"
        )
        return bool(self.autocalibration_on)

    async def set_autocalibration_on(self, autocalibration_on):
        """
        Simulate setting autocalibration.
        """
        logging.warning(
            f"Simulated: Autocalibration set to {'on' if autocalibration_on else 'off'}"
        )
        self.autocalibration_on = autocalibration_on

    async def set_measurement_on(self, measurement_on):
        """
        Simulate turning measurement on or off.
        """
        logging.warning(
            f"Simulated: Measurement set to {'on' if measurement_on else 'off'}"
        )
        self.measurement_on = measurement_on

    async def set_switch_mode_on(self, switch_mode_on):
        """
        Simulate setting switch mode.
        """
        logging.warning(
            f"Simulated: Switch mode set to {'on' if switch_mode_on else 'off'}"
        )
        self.switch_mode_on = switch_mode_on

    async def get_switch_mode_on(self):
        """
        Simulate getting the switch mode state.
        """
        logging.warning(
            f"Simulated: Switch mode is {'on' if self.switch_mode_on else 'off'}"
        )
        return bool(self.switch_mode_on)

    async def get_channel_exposure(self, channel):
        """
        Simulate getting exposure value for a channel.
        """
        logging.warning(
            f"Simulated: Exposure for channel {channel} is "
            f"{self.channel_exposure[self.convert_channel(channel)]}"
        )
        return self.channel_exposure[self.convert_channel(channel)]

    async def set_channel_exposure(self, channel, exposure):
        """
        Simulate setting the exposure for a channel.
        """
        logging.warning(
            f"Simulated: Setting exposure for channel {channel} to {exposure}"
        )
        self.channel_exposure[self.convert_channel(channel)] = exposure
