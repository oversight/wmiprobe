ACCESS_LU = {
    0: 'Unknown media',
    1: 'The media is readable',
    2: 'The media is writable',
    3: 'The media is readable and writable',
    4: '"Write once" media',
    None: None,
}


AVAILABILITY_LU = {
    1: 'Other',
    2: 'Unknown',
    3: 'Running or Full Power',
    4: 'Warning',
    5: 'In Test',
    6: 'Not Applicable',
    7: 'Power Off',
    8: 'Offline',
    9: 'Off Duty',
    10: 'Degraded',
    11: 'Not Installed',
    12: 'Install Error',
    13: ('Power Save - Unknown: The device is known to be in a power save'
         'mode, but its exact status is unknown'),
    14: ('Power Save - Low Power Mode: The device is in a power save state, '
         'but still functioning, and may exhibit degraded performance'),
    15: ('Power Save - Standby: The device is not functioning, but could be '
         'brought to full power quickly'),
    16: 'Power Cycle',
    17: ('Power Save - Warning: The device is in a warning state, but also in '
         'a power save mode'),
    18: 'Paused',
    19: 'Not Ready',
    20: 'Not Configured',
    None: None,
    0: None
}


CONFIG_MAN_ERR_CODE = {
    0: 'This device is working properly',
    1: 'This device is not configured correctly',
    2: 'Windows cannot load the driver for this device',
    3: ('The driver for this device might be corrupted, or your system may be '
        'running low on memory or other resources'),
    4: ('This device is not working properly. One of its drivers or your '
        'registry might be corrupted'),
    5: ('The driver for this device needs a resource that Windows cannot '
        'manage'),
    6: 'The boot configuration for this device conflicts with other devices',
    7: 'Cannot filter',
    8: 'The driver loader for the device is missing',
    9: ('This device is not working properly because the controlling firmware '
        'is reporting the resources for the device incorrectly'),
    10: 'This device cannot start',
    11: 'This device failed',
    12: 'This device cannot find enough free resources that it can use',
    13: 'Windows cannot verify this device\'s resources',
    14: 'This device cannot work properly until you restart your computer',
    15: ('This device is not working properly because there is probably a '
         're-enumeration problem'),
    16: 'Windows cannot identify all the resources this device uses',
    17: 'This device is asking for an unknown resource type',
    18: 'Reinstall the drivers for this device',
    19: 'Failure using the VxD loader',
    20: 'Your registry might be corrupted',
    21: ('System failure. Try changing the driver for this device. If that '
         'does not work, see your hardware documentation. Windows is removing '
         'this device'),
    22: 'This device is disabled',
    23: ('System failure. Try changing the driver for this device. If that '
         'does not work, see your hardware documentation'),
    24: ('This device is not present, is not working properly, or does not '
         'have all of its drivers installed'),
    25: 'Windows is still setting up this device',
    26: 'Windows is still setting up this device',
    27: 'This device does not have a valid log configuration',
    28: 'The drivers for this device are not installed',
    29: ('This device is disabled because the firmware of the device did not '
         'give it the required resources'),
    30: ('This device is using an Interrupt Request resource that another '
         'device is using'),
    31: ('This device is not working properly because Windows cannot load the '
         'drivers required for this device'),
    None: None
}


DRIVE_TYPES = {
    0: 'Unknown',
    1: 'No Root Directory',
    2: 'Removable Disk',
    3: 'Local Disk',
    4: 'Network Drive',
    5: 'Compact Disk',
    6: 'RAM Disk',
    None: None
}


# Unused
POW_MAN_CAP = {
    0: 'Unknown',
    1: 'Not Supported',
    2: 'Disabled',
    3: ('Enabled: The power management features are currently enabled but the '
        'exact feature set is unknown or the information is unavailable'),
    4: ('Power Saving Modes Entered Automatically: The device can change its '
        'power state based on usage or other criteria'),
    5: ('Power State Settable: The SetPowerState method is supported. This '
        'method is found on the parent CIM_LogicalDevice class and can be '
        'implemented. For more information, see Designing Managed Object '
        'Format (MOF) Classes'),
    6: ('Power Cycling Supported: The SetPowerState method can be invoked '
        'with the PowerState parameter set to 5 (Power Cycle)'),
    7: ('Timed Power-On Supported: The SetPowerState method can be invoked '
        'with the PowerState parameter set to 5 (Power Cycle) and Time set to '
        'a specific date and time, or interval, for power-on'),
    None: None
}


STATUS_INFO = {
    1: 'Other',
    2: 'Unknown',
    3: 'Enabled',
    4: 'Disabled',
    5: 'Not Applicable',
    None: None,
    0: None
}
