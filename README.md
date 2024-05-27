# wyler-clinotronic-plus
Communication with Wyler angle meter Clinotronic+.
You need to have WyBusCLR.dll

![clinotronic_plus_01](https://github.com/pao3007/wyler-clinotronic-plus/assets/35431691/359254fe-ad00-4837-9601-8c7b3474e2b9)

Create instance of class: 
```python
wcp = WylerClinotronicPlus(serial_number, device_name)
```
serial number on the device, device name consists of communication method (rs485) and COM port (COM6) -> rs485://com6

Read angle in degrees: 
```python
angle_deg = wcp.get_angle_in_deg(index)
```
dotnet library returns list of values, as we can sample data from multiple devices/channels, so we need to specify which value to read, if we have only one device with one channel ```index=0```

radians: 
```python
angle_rad = wcp.get_angle_in_rad(index)
```

Read temperature in Celsius:
```python
temperature = wcp.get_temperature_in_celsius(index)
```

Stop sampling: 
```python
wcp.stop_sampling()
```


