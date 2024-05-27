import math
import time

import clr
import pythonnet

path_to_wbyus_dll = "your_path"
clr.AddReference(path_to_wbyus_dll)

from Wyler.WyBus import WyBus, ScanRange, WyBusValueType
from System import TimeSpan

SAMPLING_TIME_MS = 100
HISTORY_DURATION_MS = 100


class WylerClinotronicPlus:

    def __init__(self, serial_number, device_name, start_ch=1, end_ch=20):
        self.serial_number = serial_number
        self.device_name = device_name

        """WyBus will find all compatible devices and put them into AvailableInterfaces"""
        self.wy_bus = WyBus(True)
        time.sleep(0.666)

        """example device_name: rs485://com6; select first found device"""
        # self.device_name = self.wy_bus.AvailableInterfaces[0].Name

        """ScanRange will scan all channels of the device as one device can communicate trough multiple channels,
        channels do not change. When you find a channel device communicates at you can do start_ch = end_ch to 
        speed up scanning"""
        self.scan_range = ScanRange(start_ch, end_ch, self.device_name)

        """Will make list of available devices from scanned devices"""
        self.wy_bus.ListDevices(self.scan_range)

        """Will select measuring device from which we want start polling, 
        example measuring_device: ClinotronicPlus: Name: B0593, url: rs485://com6:3.1"""
        self.measuring_device = self.wy_bus.GetMeasuringDevice(serial_number)

        """Set sampling rate and memory time span"""
        sampling_time_span = TimeSpan.FromMilliseconds(SAMPLING_TIME_MS)
        memory_time_span = TimeSpan.FromMilliseconds(HISTORY_DURATION_MS)

        """Starts sampling"""
        """measuring_device can be list of devices/channels"""
        """WyBusValueType.Angle | WyBusValueType.Temperature for polling both angle and temperature"""
        self.wy_bus.StartSampling(WyBusValueType.Angle, sampling_time_span, memory_time_span, self.measuring_device)
        """We need to wait atleast twice gate time to prepare device"""
        time.sleep(SAMPLING_TIME_MS*2.5/1000)

    def get_angle_in_deg(self, idx):
        """As we can have multiple channels and devices, dotnet function GetSampledAngles returns list of angles for each channel/device.
        Returns angle in degrees"""
        return math.degrees(self.get_angle_in_rad(idx))

    def get_angle_in_rad(self, idx):
        """As we can have multiple channels and devices, dotnet function GetSampledAngles returns list of angles for each channel/device.
        Returns angle in radians"""
        return self.measuring_device.GetSampledAngles()[idx].Value

    def get_temperature_in_celsius(self, idx):
        """As we can have multiple channels and devices, dotnet function GetSampledTemperatures returns list of angles for each channel/device.
        Returns temperature in Celsius"""
        return self.measuring_device.GetSampledTemperatures()[idx].Value

    def stop_sampling(self):
        self.wy_bus.StopSampling()


wcp = WylerClinotronicPlus('B0593', 'rs485://com6') #  input your own SN and device_name
print(wcp.get_angle_in_deg(0)) #  we expect only one device with one channel
wcp.stop_sampling()
